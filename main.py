import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
 
# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="글로벌 주식 대시보드",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# ── 커스텀 CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
 
/* 전체 배경 */
.stApp {
    background: #0a0e1a;
    color: #e2e8f0;
}
 
/* 사이드바 */
[data-testid="stSidebar"] {
    background: #0f1628 !important;
    border-right: 1px solid #1e2d4a;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #94a3b8;
}
 
/* 헤더 */
.main-header {
    background: linear-gradient(135deg, #0f1628 0%, #1a2340 50%, #0f1628 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 30% 50%, rgba(56,189,248,0.06) 0%, transparent 60%);
    pointer-events: none;
}
.main-header h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #f0f9ff;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.main-header p {
    color: #64748b;
    font-size: 0.9rem;
    margin: 0;
}
 
/* 메트릭 카드 */
.metric-card {
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 16px 20px;
    transition: border-color 0.2s ease;
}
.metric-card:hover { border-color: #2563eb; }
 
.metric-label {
    font-size: 0.72rem;
    color: #64748b;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.35rem;
    font-weight: 600;
    color: #f1f5f9;
}
.metric-delta-pos {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #34d399;
    margin-top: 4px;
}
.metric-delta-neg {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #f87171;
    margin-top: 4px;
}
 
/* 섹션 타이틀 */
.section-title {
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #38bdf8;
    margin: 24px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1e3a5f, transparent);
}
 
/* 수익률 바 */
.return-row {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    gap: 10px;
}
.return-ticker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #94a3b8;
    width: 70px;
    flex-shrink: 0;
}
.return-bar-bg {
    flex: 1;
    height: 6px;
    background: #1e2d4a;
    border-radius: 3px;
    overflow: hidden;
}
.return-bar-pos {
    height: 100%;
    background: linear-gradient(90deg, #10b981, #34d399);
    border-radius: 3px;
}
.return-bar-neg {
    height: 100%;
    background: linear-gradient(90deg, #ef4444, #f87171);
    border-radius: 3px;
}
.return-pct {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    width: 60px;
    text-align: right;
    flex-shrink: 0;
}
 
/* 스트림릿 기본 요소 재정의 */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 500;
    padding: 8px 20px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37,99,235,0.4);
}
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stSlider"] label {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #111827;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1e2d4a;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b;
    border-radius: 7px;
    font-size: 0.85rem;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #1e3a5f !important;
    color: #38bdf8 !important;
}
div[data-testid="metric-container"] {
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 12px 16px;
}
</style>
""", unsafe_allow_html=True)
 
# ── 데이터 정의 ──────────────────────────────────────────────
KOREAN_STOCKS = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "LG에너지솔루션": "373220.KS",
    "삼성바이오로직스": "207940.KS",
    "현대차": "005380.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "POSCO홀딩스": "005490.KS",
    "셀트리온": "068270.KS",
    "기아": "000270.KS",
}
 
US_STOCKS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Meta": "META",
    "Tesla": "TSLA",
    "Berkshire": "BRK-B",
    "TSMC": "TSM",
    "Netflix": "NFLX",
}
 
INDICES = {
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW": "^DJI",
}
 
PERIOD_OPTIONS = {
    "1개월": ("1mo", 30),
    "3개월": ("3mo", 90),
    "6개월": ("6mo", 180),
    "1년": ("1y", 365),
    "2년": ("2y", 730),
    "5년": ("5y", 1825),
}
 
# ── 유틸리티 함수 ────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_price_data(tickers: list, period: str) -> pd.DataFrame:
    """여러 티커의 종가 데이터를 한 번에 가져옵니다."""
    try:
        raw = yf.download(tickers, period=period, auto_adjust=True, progress=False)
        if isinstance(raw.columns, pd.MultiIndex):
            close = raw["Close"]
        else:
            close = raw[["Close"]] if len(tickers) == 1 else raw
        return close.dropna(how="all")
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return pd.DataFrame()
 
@st.cache_data(ttl=300)
def fetch_single_stock(ticker: str, period: str) -> pd.DataFrame:
    """단일 종목 OHLCV 데이터를 가져옵니다."""
    try:
        df = yf.download(ticker, period=period, auto_adjust=True, progress=False)
        return df
    except Exception:
        return pd.DataFrame()
 
def calc_return(series: pd.Series) -> float:
    """시작~끝 수익률(%) 계산"""
    s = series.dropna()
    if len(s) < 2:
        return 0.0
    return float((s.iloc[-1] / s.iloc[0] - 1) * 100)
 
def color_return(val: float) -> str:
    return "#34d399" if val >= 0 else "#f87171"
 
def format_number(n: float) -> str:
    if abs(n) >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if abs(n) >= 1_000:
        return f"{n/1_000:.1f}K"
    return f"{n:.2f}"
 
# ── 사이드바 ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ 설정")
    st.markdown("---")
 
    period_label = st.selectbox("📅 기간", list(PERIOD_OPTIONS.keys()), index=3)
    period_yf, _ = PERIOD_OPTIONS[period_label]
 
    st.markdown("#### 🇰🇷 한국 주식")
    kr_selected = st.multiselect(
        "종목 선택",
        list(KOREAN_STOCKS.keys()),
        default=["삼성전자", "SK하이닉스", "현대차", "NAVER"],
    )
 
    st.markdown("#### 🇺🇸 미국 주식")
    us_selected = st.multiselect(
        "종목 선택",
        list(US_STOCKS.keys()),
        default=["Apple", "NVIDIA", "Microsoft", "Tesla"],
    )
 
    st.markdown("---")
    refresh = st.button("🔄 데이터 새로고침", use_container_width=True)
    if refresh:
        st.cache_data.clear()
        st.rerun()
 
    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.7rem;color:#334155;text-align:center;'>"
        "데이터: Yahoo Finance<br>5분마다 자동 캐시 갱신"
        "</div>",
        unsafe_allow_html=True,
    )
 
# ── 메인 헤더 ────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
    <h1>📈 글로벌 주식 대시보드</h1>
    <p>한국 · 미국 주요 종목 수익률 비교 &nbsp;·&nbsp; 기간: {period_label} &nbsp;·&nbsp; 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</div>
""", unsafe_allow_html=True)
 
# ── 데이터 로드 ──────────────────────────────────────────────
kr_tickers = [KOREAN_STOCKS[n] for n in kr_selected]
us_tickers = [US_STOCKS[n] for n in us_selected]
idx_tickers = list(INDICES.values())
all_tickers = kr_tickers + us_tickers + idx_tickers
 
with st.spinner("시장 데이터를 불러오는 중..."):
    df_all = fetch_price_data(all_tickers, period_yf)
 
if df_all.empty:
    st.error("데이터를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.")
    st.stop()
 
# 이름 역매핑
ticker_to_name = {}
for n, t in {**KOREAN_STOCKS, **US_STOCKS, **INDICES}.items():
    ticker_to_name[t] = n
 
# ── 지수 현황 ────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 주요 지수 현황</div>', unsafe_allow_html=True)
 
idx_cols = st.columns(len(INDICES))
for col, (name, ticker) in zip(idx_cols, INDICES.items()):
    if ticker in df_all.columns:
        s = df_all[ticker].dropna()
        if not s.empty:
            ret = calc_return(s)
            last = s.iloc[-1]
            delta_sign = "▲" if ret >= 0 else "▼"
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{name}</div>
                    <div class="metric-value">{last:,.1f}</div>
                    <div class="{'metric-delta-pos' if ret >= 0 else 'metric-delta-neg'}">
                        {delta_sign} {abs(ret):.2f}% ({period_label})
                    </div>
                </div>
                """, unsafe_allow_html=True)
 
st.markdown("<br>", unsafe_allow_html=True)
 
# ── 탭 구성 ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 수익률 비교", "📈 차트", "🔥 수익률 랭킹", "📋 종목 상세"
])
 
# ═══════════════════════════════════════════════════════════
# TAB 1: 수익률 비교
# ═══════════════════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns(2, gap="large")
 
    # 수익률 계산
    def build_return_dict(selected_names, stock_dict):
        result = {}
        for name in selected_names:
            t = stock_dict[name]
            if t in df_all.columns:
                result[name] = calc_return(df_all[t])
        return result
 
    kr_returns = build_return_dict(kr_selected, KOREAN_STOCKS)
    us_returns = build_return_dict(us_selected, US_STOCKS)
 
    # ── 막대 차트: 한국 ──
    with col_l:
        st.markdown('<div class="section-title">🇰🇷 한국 주식 수익률</div>', unsafe_allow_html=True)
        if kr_returns:
            fig_kr = go.Figure()
            names = list(kr_returns.keys())
            rets = list(kr_returns.values())
            colors = ["#34d399" if r >= 0 else "#f87171" for r in rets]
 
            fig_kr.add_trace(go.Bar(
                x=rets, y=names,
                orientation="h",
                marker=dict(color=colors, line=dict(width=0)),
                text=[f"{r:+.2f}%" for r in rets],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=11, color="#cbd5e1"),
            ))
            fig_kr.update_layout(
                paper_bgcolor="#0a0e1a",
                plot_bgcolor="#111827",
                margin=dict(l=10, r=60, t=10, b=10),
                height=max(280, len(names) * 48),
                xaxis=dict(
                    gridcolor="#1e2d4a", zeroline=True,
                    zerolinecolor="#334155", zerolinewidth=1,
                    tickformat="+.1f", ticksuffix="%",
                    color="#64748b",
                ),
                yaxis=dict(
                    gridcolor="rgba(0,0,0,0)", color="#94a3b8",
                    tickfont=dict(size=12),
                ),
                showlegend=False,
            )
            st.plotly_chart(fig_kr, use_container_width=True)
        else:
            st.info("한국 종목을 선택해주세요.")
 
    # ── 막대 차트: 미국 ──
    with col_r:
        st.markdown('<div class="section-title">🇺🇸 미국 주식 수익률</div>', unsafe_allow_html=True)
        if us_returns:
            fig_us = go.Figure()
            names = list(us_returns.keys())
            rets = list(us_returns.values())
            colors = ["#60a5fa" if r >= 0 else "#f87171" for r in rets]
 
            fig_us.add_trace(go.Bar(
                x=rets, y=names,
                orientation="h",
                marker=dict(color=colors, line=dict(width=0)),
                text=[f"{r:+.2f}%" for r in rets],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=11, color="#cbd5e1"),
            ))
            fig_us.update_layout(
                paper_bgcolor="#0a0e1a",
                plot_bgcolor="#111827",
                margin=dict(l=10, r=60, t=10, b=10),
                height=max(280, len(names) * 48),
                xaxis=dict(
                    gridcolor="#1e2d4a", zeroline=True,
                    zerolinecolor="#334155", zerolinewidth=1,
                    tickformat="+.1f", ticksuffix="%",
                    color="#64748b",
                ),
                yaxis=dict(
                    gridcolor="rgba(0,0,0,0)", color="#94a3b8",
                    tickfont=dict(size=12),
                ),
                showlegend=False,
            )
            st.plotly_chart(fig_us, use_container_width=True)
        else:
            st.info("미국 종목을 선택해주세요.")
 
    # ── 통합 산포도 ──
    st.markdown('<div class="section-title">🌐 한국 vs 미국 수익률 산포도</div>', unsafe_allow_html=True)
    all_names, all_rets, all_markets = [], [], []
    for n, r in kr_returns.items():
        all_names.append(n); all_rets.append(r); all_markets.append("🇰🇷 한국")
    for n, r in us_returns.items():
        all_names.append(n); all_rets.append(r); all_markets.append("🇺🇸 미국")
 
    if all_rets:
        df_scatter = pd.DataFrame({"종목": all_names, "수익률": all_rets, "시장": all_markets})
        fig_sc = px.scatter(
            df_scatter, x="종목", y="수익률", color="시장",
            color_discrete_map={"🇰🇷 한국": "#34d399", "🇺🇸 미국": "#60a5fa"},
            size=[abs(r) + 2 for r in all_rets],
            text="종목",
        )
        fig_sc.add_hline(y=0, line_dash="dot", line_color="#475569", line_width=1)
        fig_sc.update_traces(textposition="top center", textfont_size=10)
        fig_sc.update_layout(
            paper_bgcolor="#0a0e1a", plot_bgcolor="#111827",
            margin=dict(l=10, r=10, t=20, b=10),
            height=360,
            yaxis=dict(
                gridcolor="#1e2d4a", tickformat="+.1f", ticksuffix="%",
                color="#64748b", zeroline=False,
            ),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", color="#64748b"),
            legend=dict(bgcolor="#111827", bordercolor="#1e2d4a", borderwidth=1),
        )
        st.plotly_chart(fig_sc, use_container_width=True)
 
# ═══════════════════════════════════════════════════════════
# TAB 2: 차트
# ═══════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">📈 정규화 주가 비교 (기준: 100)</div>', unsafe_allow_html=True)
 
    # 정규화
    selected_tickers = kr_tickers + us_tickers
    selected_names_all = kr_selected + us_selected
 
    if not selected_tickers:
        st.info("좌측 사이드바에서 종목을 선택해주세요.")
    else:
        avail_cols = [t for t in selected_tickers if t in df_all.columns]
        df_norm = df_all[avail_cols].copy()
        df_norm = df_norm / df_norm.iloc[0] * 100
        df_norm.columns = [ticker_to_name.get(c, c) for c in df_norm.columns]
 
        fig_norm = go.Figure()
        palette_kr = ["#34d399", "#10b981", "#6ee7b7", "#a7f3d0", "#d1fae5",
                      "#059669", "#047857", "#065f46", "#064e3b", "#022c22"]
        palette_us = ["#60a5fa", "#3b82f6", "#93c5fd", "#bfdbfe", "#dbeafe",
                      "#2563eb", "#1d4ed8", "#1e40af", "#1e3a8a", "#172554"]
 
        for i, name in enumerate(df_norm.columns):
            is_kr = i < len(kr_selected)
            color = palette_kr[i % len(palette_kr)] if is_kr else palette_us[(i - len(kr_selected)) % len(palette_us)]
            marker = "🇰🇷" if is_kr else "🇺🇸"
            fig_norm.add_trace(go.Scatter(
                x=df_norm.index, y=df_norm[name],
                name=f"{marker} {name}",
                line=dict(color=color, width=2),
                hovertemplate=f"<b>{name}</b><br>%{{x|%Y-%m-%d}}<br>지수: %{{y:.1f}}<extra></extra>",
            ))
 
        fig_norm.add_hline(y=100, line_dash="dot", line_color="#334155", line_width=1)
        fig_norm.update_layout(
            paper_bgcolor="#0a0e1a", plot_bgcolor="#111827",
            margin=dict(l=10, r=10, t=10, b=10),
            height=460,
            xaxis=dict(gridcolor="#1e2d4a", color="#64748b", showspikes=True, spikecolor="#334155"),
            yaxis=dict(gridcolor="#1e2d4a", color="#64748b", ticksuffix=""),
            legend=dict(
                bgcolor="#111827", bordercolor="#1e2d4a", borderwidth=1,
                font=dict(color="#94a3b8", size=11),
                orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            ),
            hovermode="x unified",
        )
        st.plotly_chart(fig_norm, use_container_width=True)
 
    # ── 개별 캔들 차트 ──
    st.markdown('<div class="section-title">🕯️ 캔들스틱 차트</div>', unsafe_allow_html=True)
 
    all_stock_names = kr_selected + us_selected
    all_stock_tickers = kr_tickers + us_tickers
    name_to_ticker = dict(zip(all_stock_names, all_stock_tickers))
 
    if all_stock_names:
        chosen = st.selectbox("종목 선택", all_stock_names)
        chosen_ticker = name_to_ticker[chosen]
 
        with st.spinner("캔들 데이터 로딩..."):
            df_candle = fetch_single_stock(chosen_ticker, period_yf)
 
        if not df_candle.empty:
            # Flatten MultiIndex columns if necessary
            if isinstance(df_candle.columns, pd.MultiIndex):
                df_candle.columns = [col[0] if isinstance(col, tuple) else col for col in df_candle.columns]
 
            fig_candle = make_subplots(
                rows=2, cols=1, shared_xaxes=True,
                row_heights=[0.75, 0.25], vertical_spacing=0.02,
            )
            fig_candle.add_trace(go.Candlestick(
                x=df_candle.index,
                open=df_candle["Open"], high=df_candle["High"],
                low=df_candle["Low"], close=df_candle["Close"],
                name=chosen,
                increasing=dict(line=dict(color="#34d399"), fillcolor="#34d399"),
                decreasing=dict(line=dict(color="#f87171"), fillcolor="#f87171"),
            ), row=1, col=1)
 
            # 20일 이동평균
            ma20 = df_candle["Close"].rolling(20).mean()
            ma60 = df_candle["Close"].rolling(60).mean()
            fig_candle.add_trace(go.Scatter(
                x=df_candle.index, y=ma20, name="MA20",
                line=dict(color="#fbbf24", width=1.5, dash="dot"),
            ), row=1, col=1)
            fig_candle.add_trace(go.Scatter(
                x=df_candle.index, y=ma60, name="MA60",
                line=dict(color="#a78bfa", width=1.5, dash="dash"),
            ), row=1, col=1)
 
            # 거래량
            vol_colors = []
            closes = df_candle["Close"].values
            opens = df_candle["Open"].values
            for c, o in zip(closes, opens):
                vol_colors.append("#34d399" if c >= o else "#f87171")
 
            if "Volume" in df_candle.columns:
                fig_candle.add_trace(go.Bar(
                    x=df_candle.index, y=df_candle["Volume"],
                    name="거래량", marker=dict(color=vol_colors, opacity=0.7),
                ), row=2, col=1)
 
            fig_candle.update_layout(
                paper_bgcolor="#0a0e1a", plot_bgcolor="#111827",
                margin=dict(l=10, r=10, t=20, b=10),
                height=520,
                xaxis_rangeslider_visible=False,
                legend=dict(bgcolor="#111827", bordercolor="#1e2d4a", font=dict(color="#94a3b8")),
            )
            fig_candle.update_xaxes(gridcolor="#1e2d4a", color="#64748b")
            fig_candle.update_yaxes(gridcolor="#1e2d4a", color="#64748b")
            st.plotly_chart(fig_candle, use_container_width=True)
    else:
        st.info("좌측 사이드바에서 종목을 선택해주세요.")
 
# ═══════════════════════════════════════════════════════════
# TAB 3: 수익률 랭킹
# ═══════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🏆 전체 종목 수익률 랭킹</div>', unsafe_allow_html=True)
 
    ranking_data = []
    for name in kr_selected:
        t = KOREAN_STOCKS[name]
        if t in df_all.columns:
            s = df_all[t].dropna()
            if not s.empty:
                ret = calc_return(s)
                last = s.iloc[-1]
                ranking_data.append({
                    "시장": "🇰🇷 한국",
                    "종목명": name,
                    "현재가": f"{last:,.0f} KRW",
                    "수익률(%)": ret,
                })
    for name in us_selected:
        t = US_STOCKS[name]
        if t in df_all.columns:
            s = df_all[t].dropna()
            if not s.empty:
                ret = calc_return(s)
                last = s.iloc[-1]
                ranking_data.append({
                    "시장": "🇺🇸 미국",
                    "종목명": name,
                    "현재가": f"${last:,.2f}",
                    "수익률(%)": ret,
                })
 
    if ranking_data:
        df_rank = pd.DataFrame(ranking_data).sort_values("수익률(%)", ascending=False).reset_index(drop=True)
        df_rank.index += 1
 
        # 히트맵 스타일 테이블
        fig_heat = go.Figure(data=go.Table(
            columnwidth=[50, 80, 120, 100, 100],
            header=dict(
                values=["순위", "시장", "종목명", "현재가", f"수익률 ({period_label})"],
                fill_color="#0f1628",
                font=dict(color="#38bdf8", size=12, family="Noto Sans KR"),
                align="center",
                line_color="#1e2d4a",
                height=36,
            ),
            cells=dict(
                values=[
                    list(df_rank.index),
                    df_rank["시장"],
                    df_rank["종목명"],
                    df_rank["현재가"],
                    [f"{r:+.2f}%" for r in df_rank["수익률(%)"]],
                ],
                fill_color=[
                    ["#111827"] * len(df_rank),
                    ["#111827"] * len(df_rank),
                    ["#111827"] * len(df_rank),
                    ["#111827"] * len(df_rank),
                    ["#0d2818" if r >= 0 else "#2d0f0f" for r in df_rank["수익률(%)"]],
                ],
                font=dict(
                    color=[
                        ["#94a3b8"] * len(df_rank),
                        ["#e2e8f0"] * len(df_rank),
                        ["#f1f5f9"] * len(df_rank),
                        ["#cbd5e1"] * len(df_rank),
                        ["#34d399" if r >= 0 else "#f87171" for r in df_rank["수익률(%)"]],
                    ],
                    size=12,
                    family="JetBrains Mono, Noto Sans KR",
                ),
                align=["center", "center", "left", "right", "right"],
                line_color="#1e2d4a",
                height=34,
            ),
        ))
        fig_heat.update_layout(
            paper_bgcolor="#0a0e1a",
            margin=dict(l=0, r=0, t=0, b=0),
            height=max(280, len(df_rank) * 36 + 60),
        )
        st.plotly_chart(fig_heat, use_container_width=True)
 
        # 요약 통계
        st.markdown('<div class="section-title">📊 요약 통계</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        kr_rets_only = [r["수익률(%)"] for r in ranking_data if "한국" in r["시장"]]
        us_rets_only = [r["수익률(%)"] for r in ranking_data if "미국" in r["시장"]]
 
        with c1:
            best = df_rank.iloc[0]
            st.metric("🥇 최고 수익", best["종목명"], f"{best['수익률(%)']:+.2f}%")
        with c2:
            worst = df_rank.iloc[-1]
            st.metric("📉 최저 수익", worst["종목명"], f"{worst['수익률(%)']:+.2f}%")
        with c3:
            kr_avg = np.mean(kr_rets_only) if kr_rets_only else 0
            st.metric("🇰🇷 한국 평균", f"{kr_avg:+.2f}%", "")
        with c4:
            us_avg = np.mean(us_rets_only) if us_rets_only else 0
            st.metric("🇺🇸 미국 평균", f"{us_avg:+.2f}%", "")
 
# ═══════════════════════════════════════════════════════════
# TAB 4: 종목 상세
# ═══════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">🔍 종목 상세 정보</div>', unsafe_allow_html=True)
 
    all_names_map = {**{n: t for n, t in KOREAN_STOCKS.items() if n in kr_selected},
                     **{n: t for n, t in US_STOCKS.items() if n in us_selected}}
 
    if not all_names_map:
        st.info("좌측 사이드바에서 종목을 선택해주세요.")
    else:
        detail_name = st.selectbox("종목 선택", list(all_names_map.keys()), key="detail_select")
        detail_ticker = all_names_map[detail_name]
 
        with st.spinner(f"{detail_name} 정보 로딩..."):
            info_obj = yf.Ticker(detail_ticker).info
 
        # 기본 정보 카드
        c1, c2, c3, c4 = st.columns(4)
        fields = [
            ("현재가", info_obj.get("currentPrice") or info_obj.get("regularMarketPrice")),
            ("52주 최고", info_obj.get("fiftyTwoWeekHigh")),
            ("52주 최저", info_obj.get("fiftyTwoWeekLow")),
            ("시가총액", info_obj.get("marketCap")),
        ]
        cols = [c1, c2, c3, c4]
        for col, (label, val) in zip(cols, fields):
            display = "N/A"
            if val is not None:
                if label == "시가총액":
                    display = format_number(val)
                else:
                    display = f"{val:,.2f}"
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{display}</div>
                </div>
                """, unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
        c5, c6, c7, c8 = st.columns(4)
        fields2 = [
            ("PER", info_obj.get("trailingPE")),
            ("PBR", info_obj.get("priceToBook")),
            ("배당수익률", info_obj.get("dividendYield")),
            ("베타", info_obj.get("beta")),
        ]
        for col, (label, val) in zip([c5, c6, c7, c8], fields2):
            if val is not None:
                if label == "배당수익률":
                    display = f"{val*100:.2f}%"
                else:
                    display = f"{val:.2f}"
            else:
                display = "N/A"
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{display}</div>
                </div>
                """, unsafe_allow_html=True)
 
        # 기업 요약
        summary = info_obj.get("longBusinessSummary", "")
        if summary:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📝 기업 개요 보기"):
                st.markdown(f"<p style='color:#94a3b8;font-size:0.88rem;line-height:1.7;'>{summary[:800]}...</p>",
                            unsafe_allow_html=True)
 
        # 수익률 구간별 비교
        st.markdown('<div class="section-title">📅 기간별 수익률</div>', unsafe_allow_html=True)
        period_rets = {}
        for plabel, (pyf, _) in PERIOD_OPTIONS.items():
            s_data = fetch_price_data([detail_ticker], pyf)
            if not s_data.empty and detail_ticker in s_data.columns:
                period_rets[plabel] = calc_return(s_data[detail_ticker])
            elif not s_data.empty and len(s_data.columns) == 1:
                period_rets[plabel] = calc_return(s_data.iloc[:, 0])
 
        if period_rets:
            fig_pr = go.Figure()
            labels = list(period_rets.keys())
            values = list(period_rets.values())
            bar_colors = ["#34d399" if v >= 0 else "#f87171" for v in values]
            fig_pr.add_trace(go.Bar(
                x=labels, y=values,
                marker=dict(color=bar_colors, line=dict(width=0)),
                text=[f"{v:+.2f}%" for v in values],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=11, color="#cbd5e1"),
            ))
            fig_pr.add_hline(y=0, line_color="#334155", line_width=1)
            fig_pr.update_layout(
                paper_bgcolor="#0a0e1a", plot_bgcolor="#111827",
                margin=dict(l=10, r=10, t=20, b=10),
                height=280,
                xaxis=dict(gridcolor="rgba(0,0,0,0)", color="#64748b"),
                yaxis=dict(gridcolor="#1e2d4a", tickformat="+.1f", ticksuffix="%", color="#64748b"),
                showlegend=False,
            )
            st.plotly_chart(fig_pr, use_container_width=True)
 
# ── 푸터 ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#334155;font-size:0.75rem;padding:8px 0;'>"
    "📊 글로벌 주식 대시보드 · 데이터 제공: Yahoo Finance (yfinance) · "
    "투자 참고용이며 투자 권유가 아닙니다."
    "</div>",
    unsafe_allow_html=True,
)
