import argparse
import concurrent.futures
import json
import time
from pathlib import Path

import httpx

DEFAULT_BASE_URL = "http://127.0.0.1:8000"
QUERIES = Path("data/sample_queries.jsonl")

results = {"success": 0, "error": 0, "latencies": []}


def send_request(client: httpx.Client, base_url: str, payload: dict) -> None:
    try:
        start = time.perf_counter()
        r = client.post(f"{base_url}/chat", json=payload)
        latency = (time.perf_counter() - start) * 1000
        results["latencies"].append(latency)
        if r.status_code == 200:
            results["success"] += 1
        else:
            results["error"] += 1
        print(f"[{r.status_code}] {r.json().get('correlation_id')} | {payload['feature']} | {latency:.1f}ms")
    except Exception as e:
        results["error"] += 1
        print(f"Error: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load test for observability lab")
    parser.add_argument("--base-url", type=str, default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--requests", type=int, default=20, help="Number of requests to send")
    parser.add_argument("--count", type=int, default=None, help="Alias for --requests")
    parser.add_argument("--concurrency", type=int, default=4, help="Number of concurrent requests")
    args = parser.parse_args()
    request_count = args.requests if args.count is None else args.count

    lines = [line for line in QUERIES.read_text(encoding="utf-8").splitlines() if line.strip()]
    lines = (lines * ((request_count // len(lines)) + 1))[:request_count]

    print(f"Starting load test: {request_count} requests with concurrency {args.concurrency}")

    with httpx.Client(timeout=30.0) as client:
        if args.concurrency > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
                futures = [
                    executor.submit(send_request, client, args.base_url, json.loads(line))
                    for line in lines
                ]
                concurrent.futures.wait(futures)
        else:
            for line in lines:
                send_request(client, args.base_url, json.loads(line))

    print("\n=== Load Test Summary ===")
    print(f"Total requests: {results['success'] + results['error']}")
    print(f"Success: {results['success']}")
    print(f"Errors: {results['error']}")
    if results["latencies"]:
        avg_latency = sum(results["latencies"]) / len(results["latencies"])
        print(f"Avg latency: {avg_latency:.1f}ms")


if __name__ == "__main__":
    main()
