import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Bảng điều khiển quan sát", layout="wide")
st.title("BẢNG ĐIỀU KHIỂN QUAN SÁT HỆ THỐNG")

# Load metrics data (assume exported as JSONL or JSON)
def load_metrics(path):
    records = []
    if Path(path).exists():
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
    return pd.DataFrame(records)

# You can change this path to your exported metrics/logs
metrics_path = "data/logs.jsonl"
df = load_metrics(metrics_path)

if df.empty:
    st.warning("Không tìm thấy dữ liệu metrics. Vui lòng xuất dữ liệu ra data/logs.jsonl.")
    st.stop()


# Chia UI thành 3 cột hàng ngang, mỗi cột 2 panel
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Số lượng yêu cầu theo tính năng")
    feat_count = df['feature'].value_counts().reset_index()
    feat_count.columns = ['Feature', 'Count']
    st.bar_chart(feat_count.set_index('Feature'))

    st.subheader("Độ trễ trung bình (ms) theo tính năng")
    if 'latency_ms' in df.columns:
        avg_latency = df.groupby('feature')['latency_ms'].mean()
        st.bar_chart(avg_latency)
    else:
        st.info("Không có dữ liệu độ trễ (latency_ms).")

with col2:
    st.subheader("Chi phí (USD) theo thời gian")
    if 'cost_usd' in df.columns and 'ts' in df.columns:
        df['ts'] = pd.to_datetime(df['ts'])
        cost_time = df.groupby(pd.Grouper(key='ts', freq='1min'))['cost_usd'].sum()
        st.line_chart(cost_time)
    else:
        st.info("Không có dữ liệu chi phí hoặc thời gian.")

    st.subheader("Sử dụng token (vào/ra)")
    if 'tokens_in' in df.columns and 'tokens_out' in df.columns:
        st.area_chart(df[['tokens_in', 'tokens_out']])
    else:
        st.info("Không có dữ liệu token.")

with col3:
    st.subheader("Phân phối điểm chất lượng")
    if 'quality_score' in df.columns:
        st.histogram(df['quality_score'], bins=10)
    else:
        st.info("Không có dữ liệu điểm chất lượng.")

    st.subheader("Các loại lỗi")
    if 'error_type' in df.columns:
        err_count = df['error_type'].value_counts().reset_index()
        err_count.columns = ['Error Type', 'Count']
        st.bar_chart(err_count.set_index('Error Type'))
    else:
        st.info("Không có dữ liệu lỗi.")
