from __future__ import annotations

import time
from dataclasses import dataclass

from . import metrics
import os
from dotenv import load_dotenv
import openai
from .mock_rag import retrieve
from .pii import hash_user_id, summarize_text
from langfuse import observe, get_client   # ✅ Import trực tiếp từ langfuse v4


@dataclass
class AgentResult:
    answer: str
    latency_ms: int
    tokens_in: int
    tokens_out: int
    cost_usd: float
    quality_score: float


class LabAgent:
    def __init__(self, model: str = None) -> None:
        load_dotenv()
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.langfuse = get_client()       # ✅ Dùng get_client() thay vì langfuse_context

    @observe()                             # ✅ observe() vẫn dùng được trong v4
    def run(self, user_id: str, feature: str, session_id: str, message: str) -> AgentResult:

        # ✅ Cập nhật trace dùng get_client() thay vì langfuse_context
        # if self.langfuse:
        #     self.langfuse.update_current_trace(
        #         user_id=hash_user_id(user_id),
        #         session_id=session_id,
        #         tags=["lab", feature, self.model],
        #     )

        started = time.perf_counter()
        docs = retrieve(message)
        prompt = f"Feature={feature}\nDocs={docs}\nQuestion={message}"

        client = openai.OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        quality_score = self._heuristic_quality(message, answer, docs)
        latency_ms = int((time.perf_counter() - started) * 1000)
        cost_usd = self._estimate_cost(input_tokens, output_tokens)

        # ✅ update_current_observation vẫn dùng được qua get_client()
        # if self.langfuse:
        #     self.langfuse.update_current_observation(
        #         metadata={"doc_count": len(docs), "query_preview": summarize_text(message)},
        #         usage_details={"input": input_tokens, "output": output_tokens},
        #     )
        #     self.langfuse.flush()          # ✅ Flush để đảm bảo gửi lên

        metrics.record_request(
            latency_ms=latency_ms,
            cost_usd=cost_usd,
            tokens_in=input_tokens,
            tokens_out=output_tokens,
            quality_score=quality_score,
        )

        return AgentResult(
            answer=answer,
            latency_ms=latency_ms,
            tokens_in=input_tokens,
            tokens_out=output_tokens,
            cost_usd=cost_usd,
            quality_score=quality_score,
        )

    def _estimate_cost(self, tokens_in: int, tokens_out: int) -> float:
        input_cost = (tokens_in / 1_000_000) * 3
        output_cost = (tokens_out / 1_000_000) * 15
        return round(input_cost + output_cost, 6)

    def _heuristic_quality(self, question: str, answer: str, docs: list[str]) -> float:
        score = 0.5
        if docs:
            score += 0.2
        if len(answer) > 40:
            score += 0.1
        if question.lower().split()[0:1] and any(token in answer.lower() for token in question.lower().split()[:3]):
            score += 0.1
        if "[REDACTED" in answer:
            score -= 0.2
        return round(max(0.0, min(1.0, score)), 2)
