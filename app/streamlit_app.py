from __future__ import annotations

import os
import pandas as pd
import streamlit as st

# ═══════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Authentication Orchestrator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════
# PREMIUM CSS — dark fintech theme
# ═══════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
}

/* ── App background ── */
.stApp {
    background-color: #111d2e;
    color: #dce8f8;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #152030 !important;
    border-right: 1px solid #223348 !important;
}
section[data-testid="stSidebar"] * {
    color: #a8c0d8 !important;
}
section[data-testid="stSidebar"] label {
    font-size: 10px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #6888a8 !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #1a2d42 !important;
    border: 1px solid #2a3f58 !important;
    color: #a8c0d8 !important;
}

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: #182840 !important;
    border: 1px solid #223348 !important;
    border-radius: 8px !important;
    padding: 20px 24px !important;
}
div[data-testid="metric-container"] label {
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #6888a8 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 26px !important;
    font-weight: 600 !important;
    color: #dce8f8 !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border: 1px solid #223348 !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
.stDataFrame thead tr th {
    background: #182840 !important;
    color: #6888a8 !important;
    font-size: 10px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid #223348 !important;
}
.stDataFrame tbody tr:hover {
    background: #111d30 !important;
}

/* ── Charts ── */
.stBarChart { border: 1px solid #223348 !important; border-radius: 8px !important; }

/* ── Hide default elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 2rem !important; }

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #111d2e; }
::-webkit-scrollbar-thumb { background: #223348; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════

CSV_PATH = "outputs/authentication_decisions.csv"

if not os.path.exists(CSV_PATH):
    st.markdown("""
    <div style="
        margin: 4rem auto;
        max-width: 480px;
        background: #182840;
        border: 1px solid #2a4a70;
        border-left: 3px solid #0070f3;
        border-radius: 8px;
        padding: 24px 28px;
        font-family: 'IBM Plex Mono', monospace;
    ">
        <div style="font-size:11px;letter-spacing:2px;color:#0070f3;margin-bottom:10px;font-weight:600">
            DATA NOT FOUND
        </div>
        <div style="font-size:13px;color:#94aac8;line-height:1.7">
            No authentication data available.<br>
            Run <span style="color:#00d4ff;background:#162538;padding:1px 6px;border-radius:3px">python main.py</span> to generate the dataset.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = pd.read_csv(CSV_PATH)

# ═══════════════════════════════════════════════════════════
# STRATEGY COLOR MAP
# ═══════════════════════════════════════════════════════════

STRATEGY_COLORS = {
    "frictionless":   {"color": "#00d4a0", "bg": "rgba(0,212,160,0.08)",  "border": "rgba(0,212,160,0.25)"},
    "passkey":        {"color": "#0070f3", "bg": "rgba(0,112,243,0.08)",  "border": "rgba(0,112,243,0.25)"},
    "otp_push":       {"color": "#7c6af7", "bg": "rgba(124,106,247,0.08)","border": "rgba(124,106,247,0.25)"},
    "challenge_3ds":  {"color": "#f0a000", "bg": "rgba(240,160,0,0.08)",  "border": "rgba(240,160,0,0.25)"},
    "block":          {"color": "#e84040", "bg": "rgba(232,64,64,0.08)",  "border": "rgba(232,64,64,0.25)"},
}

def strategy_style(s: str) -> dict:
    return STRATEGY_COLORS.get(str(s).lower(), {"color": "#94aac8", "bg": "rgba(148,170,200,0.08)", "border": "rgba(148,170,200,0.25)"})

def risk_color(val: float) -> str:
    if val >= 70: return "#e84040"
    if val >= 40: return "#f0a000"
    return "#00d4a0"

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="padding: 20px 4px 24px 4px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <div style="width:28px;height:28px;background:#0070f3;border-radius:6px;
                        display:flex;align-items:center;justify-content:center;">
                <span style="font-size:14px;color:white;font-weight:800">P</span>
            </div>
            <div>
                <div style="font-size:13px;font-weight:700;color:#e2e8f4;letter-spacing:0.3px">
                    Authentication
                </div>
                <div style="font-size:10px;color:#6888a8;letter-spacing:1px;text-transform:uppercase">
                    Orchestrator
                </div>
            </div>
        </div>
        <div style="height:1px;background:linear-gradient(90deg,#0070f3,transparent);
                    margin:16px 0 24px 0;"></div>
    </div>
    """, unsafe_allow_html=True)

    merchant_category = st.selectbox(
        "Merchant category",
        ["All"] + sorted(df["merchant_category"].unique().tolist())
    )
    device_type = st.selectbox(
        "Device type",
        ["All"] + sorted(df["device_type"].unique().tolist())
    )
    strategy = st.selectbox(
        "Recommended strategy",
        ["All"] + sorted(df["recommended_strategy"].unique().tolist())
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Strategy legend
    st.markdown("""
    <div style="padding:14px;background:#122030;border-radius:8px;border:1px solid #223348;">
        <div style="font-size:9px;letter-spacing:1.5px;color:#4a6a88;font-weight:600;
                    text-transform:uppercase;margin-bottom:10px;">STRATEGIES</div>
    """, unsafe_allow_html=True)

    for key, meta in STRATEGY_COLORS.items():
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">
            <div style="width:8px;height:8px;border-radius:2px;background:{meta['color']};
                        flex-shrink:0;"></div>
            <span style="font-size:11px;color:#6888a8;font-family:'IBM Plex Mono',monospace;">
                {key}
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# FILTER
# ═══════════════════════════════════════════════════════════

filtered = df.copy()
if merchant_category != "All":
    filtered = filtered[filtered["merchant_category"] == merchant_category]
if device_type != "All":
    filtered = filtered[filtered["device_type"] == device_type]
if strategy != "All":
    filtered = filtered[filtered["recommended_strategy"] == strategy]

# ═══════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════

st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:flex-end;
            margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid #223348;">
    <div>
        <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;
                    color:#0070f3;font-weight:600;margin-bottom:6px;">
            ML UPLIFT
        </div>
        <div style="font-size:24px;font-weight:700;color:#e2e8f4;letter-spacing:-0.5px;
                    font-family:'IBM Plex Sans',sans-serif;">
            Authentication Orchestrator
        </div>
        <div style="font-size:12px;color:#6888a8;margin-top:4px;">
            ML-driven routing — approval · friction · risk · conversion
        </div>
    </div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;
                color:#6888a8;text-align:right;">
        <div style="color:#00d4a0;font-size:10px;margin-bottom:3px;">● LIVE</div>
        <div>{} transactions</div>
    </div>
</div>
""".format(len(filtered)), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# KPI METRICS
# ═══════════════════════════════════════════════════════════

m1, m2, m3, m4, m5 = st.columns(5)

avg_approval = round(filtered["pred_approval_proba"].mean(), 1) if len(filtered) else 0
avg_abandon  = round(filtered["pred_abandon_proba"].mean(), 1)  if len(filtered) else 0
avg_fraud    = round(filtered["pred_fraud_proba"].mean(), 1)    if len(filtered) else 0
frictionless_rate = round(
    (filtered["recommended_strategy"] == "frictionless").mean() * 100, 1
) if len(filtered) else 0
high_risk_count = int(
    ((filtered["pred_fraud_proba"] >= 50) | (filtered["pred_abandon_proba"] >= 50)).sum()
) if len(filtered) else 0

m1.metric("Transactions", f"{len(filtered):,}")
m2.metric("Avg approval", f"{avg_approval}%")
m3.metric("Avg abandon risk", f"{avg_abandon}%")
m4.metric("Avg fraud risk", f"{avg_fraud}%")
m5.metric("Frictionless rate", f"{frictionless_rate}%")

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# STRATEGY DISTRIBUTION + HIGH RISK SUMMARY
# ═══════════════════════════════════════════════════════════

col_left, col_right = st.columns([1.6, 1])

with col_left:
    st.markdown("""
    <div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;
                color:#6888a8;font-weight:600;margin-bottom:12px;">
        RECOMMENDED STRATEGY DISTRIBUTION
    </div>
    """, unsafe_allow_html=True)

    strategy_counts = filtered["recommended_strategy"].value_counts()
    total = strategy_counts.sum()

    for strat, count in strategy_counts.items():
        meta = strategy_style(strat)
        pct  = round(count / total * 100, 1) if total else 0
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:9px;">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;
                        color:{meta['color']};width:130px;flex-shrink:0;">
                {strat}
            </div>
            <div style="flex:1;height:7px;background:#182840;border-radius:3px;overflow:hidden;">
                <div style="width:{pct}%;height:100%;background:{meta['color']};
                            border-radius:3px;transition:width 0.5s ease;
                            opacity:0.85;"></div>
            </div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;
                        color:#6888a8;width:60px;text-align:right;flex-shrink:0;">
                {count:,} &nbsp;<span style="color:#4a6a88">{pct}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;
                color:#6888a8;font-weight:600;margin-bottom:12px;">
        RISK SUMMARY
    </div>
    """, unsafe_allow_html=True)

    risk_items = [
        ("High fraud risk",   int((filtered["pred_fraud_proba"]   >= 70).sum()), "#e84040"),
        ("High abandon risk", int((filtered["pred_abandon_proba"] >= 50).sum()), "#f0a000"),
        ("Blocked",           int((filtered["recommended_strategy"] == "block").sum()), "#e84040"),
        ("Frictionless",      int((filtered["recommended_strategy"] == "frictionless").sum()), "#00d4a0"),
        ("Passkey available", int(filtered["passkey_available"].sum()) if "passkey_available" in filtered.columns else 0, "#0070f3"),
    ]
    for label, val, color in risk_items:
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:8px 12px;margin-bottom:5px;border-radius:6px;
                    background:#182840;border:1px solid #223348;">
            <span style="font-size:12px;color:#6888a8;">{label}</span>
            <span style="font-family:'IBM Plex Mono',monospace;font-size:13px;
                         font-weight:600;color:{color};">{val:,}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TABLES
# ═══════════════════════════════════════════════════════════

cols_display = [
    "transaction_id", "amount_eur", "merchant_category", "device_type",
    "tokenized", "passkey_available",
    "pred_approval_proba", "pred_abandon_proba", "pred_fraud_proba",
    "recommended_strategy", "business_value_score", "decision_reason",
]
available_cols = [c for c in cols_display if c in filtered.columns]

tab1, tab2 = st.tabs(["  Top business value  ", "  High friction · High risk  "])

with tab1:
    st.markdown("""
    <div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;
                color:#6888a8;font-weight:600;padding:12px 0 10px 0;">
        TOP TRANSACTIONS BY BUSINESS VALUE SCORE
    </div>
    """, unsafe_allow_html=True)

    top_df = filtered.sort_values("business_value_score", ascending=False)[available_cols].head(40)

    st.dataframe(
        top_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "pred_approval_proba": st.column_config.ProgressColumn(
                "Approval %", min_value=0, max_value=100, format="%.1f%%"
            ),
            "pred_abandon_proba": st.column_config.ProgressColumn(
                "Abandon %", min_value=0, max_value=100, format="%.1f%%"
            ),
            "pred_fraud_proba": st.column_config.ProgressColumn(
                "Fraud %", min_value=0, max_value=100, format="%.1f%%"
            ),
            "business_value_score": st.column_config.NumberColumn(
                "BV Score", format="%.3f"
            ),
            "amount_eur": st.column_config.NumberColumn(
                "Amount (€)", format="€%.2f"
            ),
        }
    )

with tab2:
    st.markdown("""
    <div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;
                color:#e84040;font-weight:600;padding:12px 0 10px 0;">
        HIGH FRICTION / HIGH RISK — REQUIRES ATTENTION
    </div>
    """, unsafe_allow_html=True)

    risk_view = filtered[
        (filtered["pred_abandon_proba"] >= 50) | (filtered["pred_fraud_proba"] >= 50)
    ].sort_values(["pred_fraud_proba", "pred_abandon_proba"], ascending=False)

    if risk_view.empty:
        st.markdown("""
        <div style="padding:20px;text-align:center;color:#4a6a88;
                    font-family:'IBM Plex Mono',monospace;font-size:12px;">
            No high-risk transactions with current filters.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.dataframe(
            risk_view[available_cols].head(40),
            use_container_width=True,
            hide_index=True,
            column_config={
                "pred_approval_proba": st.column_config.ProgressColumn(
                    "Approval %", min_value=0, max_value=100, format="%.1f%%"
                ),
                "pred_abandon_proba": st.column_config.ProgressColumn(
                    "Abandon %", min_value=0, max_value=100, format="%.1f%%"
                ),
                "pred_fraud_proba": st.column_config.ProgressColumn(
                    "Fraud %", min_value=0, max_value=100, format="%.1f%%"
                ),
                "business_value_score": st.column_config.NumberColumn(
                    "BV Score", format="%.3f"
                ),
                "amount_eur": st.column_config.NumberColumn(
                    "Amount (€)", format="€%.2f"
                ),
            }
        )

# ═══════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════

st.markdown("""
<div style="margin-top:40px;padding:14px 0;border-top:1px solid #223348;
            display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#4a6a88;">
        Uplift · Authentication Orchestrator
    </span>
    <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#4a6a88;">
        Synthetic data · Product demo
    </span>
</div>
""", unsafe_allow_html=True)
