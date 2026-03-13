import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Format Selector · Buzzoola",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── STYLES ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #F7F7F5;
    border-right: 1px solid #E8E8E3;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

/* Main */
.main .block-container { padding: 1.5rem 2rem; max-width: 1400px; }

/* Header */
.page-header {
    display: flex; align-items: baseline; gap: 12px;
    margin-bottom: 1.5rem; padding-bottom: 1rem;
    border-bottom: 1px solid #E8E8E3;
}
.page-header h1 { font-size: 1.35rem; font-weight: 600; color: #1A1A1A; margin: 0; }
.page-header span { font-size: 0.8rem; color: #999; font-family: 'DM Mono', monospace; }

/* Section labels */
.section-label {
    font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #999; margin-bottom: 0.6rem; margin-top: 1.2rem;
}

/* KPI cards */
.kpi-row { display: flex; gap: 12px; margin-bottom: 1.2rem; }
.kpi-card {
    flex: 1; background: white; border: 1px solid #E8E8E3;
    border-radius: 10px; padding: 14px 16px;
}
.kpi-label { font-size: 0.7rem; color: #888; font-weight: 500; margin-bottom: 4px; }
.kpi-value { font-size: 1.45rem; font-weight: 600; color: #1A1A1A; font-family: 'DM Mono', monospace; }
.kpi-sub { font-size: 0.7rem; color: #AAA; margin-top: 2px; }

/* Score badge */
.score-pill {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600; font-family: 'DM Mono', monospace;
}
.score-high { background: #EDFAF3; color: #1A7A4A; }
.score-mid  { background: #FFF8EC; color: #B45309; }
.score-low  { background: #FEF2F2; color: #B91C1C; }

/* Table */
.format-table { width: 100%; border-collapse: collapse; font-size: 0.83rem; }
.format-table th {
    text-align: left; padding: 8px 12px;
    background: #F7F7F5; border-bottom: 2px solid #E8E8E3;
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.06em;
    text-transform: uppercase; color: #888; white-space: nowrap;
}
.format-table td {
    padding: 10px 12px; border-bottom: 1px solid #F0F0EC;
    vertical-align: top; color: #2A2A2A;
}
.format-table tr:hover td { background: #FAFAF8; cursor: pointer; }
.format-name { font-weight: 500; color: #1A1A1A; }
.format-id { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #AAA; }
.tag {
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 0.67rem; font-weight: 500; margin: 1px 2px 1px 0;
    background: #F0F0EC; color: #555;
}
.tag-video { background: #EEF2FF; color: #4338CA; }
.tag-banner { background: #F0FDF4; color: #166534; }
.tag-cpm { background: #FFF7ED; color: #C2410C; }
.tag-cpc { background: #EFF6FF; color: #1D4ED8; }

/* Metric bar */
.metric-bar-wrap { display: flex; align-items: center; gap: 8px; }
.metric-bar-bg { height: 5px; background: #EEE; border-radius: 3px; flex: 1; min-width: 60px; }
.metric-bar-fill { height: 5px; border-radius: 3px; background: #4F46E5; }
.metric-val { font-family: 'DM Mono', monospace; font-size: 0.78rem; color: #333; min-width: 44px; text-align: right; }

/* Modal overlay */
.card-overlay {
    background: white; border: 1px solid #E8E8E3; border-radius: 12px;
    padding: 20px; margin-top: 12px;
}
.card-title { font-size: 1.1rem; font-weight: 600; color: #1A1A1A; margin-bottom: 4px; }
.card-id { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #AAA; margin-bottom: 12px; }
.card-desc { font-size: 0.82rem; color: #555; line-height: 1.6; margin-bottom: 14px; padding: 10px 12px; background: #FAFAF8; border-radius: 8px; }
.card-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px; }
.card-metric { background: #F7F7F5; border-radius: 8px; padding: 10px 12px; }
.card-metric-label { font-size: 0.65rem; color: #999; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.card-metric-value { font-size: 1rem; font-weight: 600; color: #1A1A1A; font-family: 'DM Mono', monospace; }
.card-section { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #AAA; margin: 10px 0 6px; }
.tags-row { display: flex; flex-wrap: wrap; gap: 4px; }
.info-row { display: flex; gap: 8px; margin-bottom: 6px; font-size: 0.8rem; }
.info-label { color: #888; min-width: 130px; }
.info-val { color: #1A1A1A; font-weight: 500; }

/* Scoring panel */
.weight-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.weight-label { font-size: 0.78rem; color: #444; min-width: 100px; }
.weight-total { font-family: 'DM Mono', monospace; font-size: 0.9rem; font-weight: 600; }
.weight-ok { color: #1A7A4A; }
.weight-bad { color: #B91C1C; }

/* Divider */
hr.light { border: none; border-top: 1px solid #E8E8E3; margin: 1rem 0; }

/* Streamlit overrides */
div[data-testid="stSlider"] label { font-size: 0.78rem !important; color: #555 !important; }
div[data-testid="stMultiSelect"] label { font-size: 0.78rem !important; color: #555 !important; }
div[data-testid="stSelectbox"] label { font-size: 0.78rem !important; color: #555 !important; }
.stButton > button {
    background: #1A1A1A; color: white; border: none; border-radius: 8px;
    font-family: 'DM Sans'; font-size: 0.8rem; font-weight: 500;
    padding: 6px 14px; transition: opacity 0.15s;
}
.stButton > button:hover { opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("DataLens_-_formats.csv")
    di = pd.read_csv("DataLens_-_dict_items.csv")
    fi = pd.read_excel("DataLens.xlsx", sheet_name="format_items")

    # Join format_items with dict_items to get item names
    merged = fi.merge(di[["dict_id", "item_id", "item_name"]], on=["dict_id", "item_id"], how="left")
    pivot = merged.groupby(["format_id", "dict_id"])["item_name"].apply(list).unstack("dict_id").reset_index()

    df = df.merge(pivot, on="format_id", how="left")
    return df, di

df, di = load_data()

def fmt_pct(v):
    if pd.isna(v): return "—"
    return f"{v*100:.1f}%"

def fmt_money(v):
    if pd.isna(v): return "—"
    return f"{int(v):,} ₽".replace(",", " ")

def fmt_reach(v):
    if pd.isna(v): return "—"
    m = v / 1_000_000
    if m >= 1: return f"{m:.1f}M"
    return f"{int(v):,}".replace(",", " ")

# ─── eCPM CALCULATION ─────────────────────────────────────────────────────────
def calc_ecpm(row):
    """Convert any buy model to eCPM, then apply discount."""
    model = row.get("buy_model", "CPM")
    ctr = row.get("ctr_avg", np.nan)
    discount = row.get("discount", 0) or 0

    if model == "CPM":
        raw = row.get("cpm_avg", np.nan)
    elif model == "CPC":
        cpc = row.get("cpc_avg", np.nan)
        if pd.isna(cpc) or pd.isna(ctr) or ctr == 0:
            raw = np.nan
        else:
            raw = cpc * ctr * 1000  # CPC * CTR * 1000 = eCPM
    elif model == "CPV":
        cpv = row.get("cpv_avg", np.nan)
        vtr = row.get("vtr_avg", np.nan)
        if pd.isna(cpv) or pd.isna(vtr) or vtr == 0:
            raw = np.nan
        else:
            raw = cpv * vtr * 1000
    else:
        raw = row.get("cpm_avg", np.nan)

    if pd.isna(raw):
        return np.nan
    return raw * (1 - discount)

df["ecpm_effective"] = df.apply(calc_ecpm, axis=1)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-label">Тип формата</div>', unsafe_allow_html=True)
    format_types = st.multiselect(
        "format_type", options=["Видео", "Баннер"], default=["Видео", "Баннер"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label">Устройство</div>', unsafe_allow_html=True)
    devices = st.multiselect(
        "device", options=["Desktop", "Mobile Web", "In-App", "Smart TV"],
        default=["Desktop", "Mobile Web", "In-App", "Smart TV"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label">Модель закупки</div>', unsafe_allow_html=True)
    buy_models = st.multiselect(
        "buy_model", options=["CPM", "CPC"], default=["CPM", "CPC"],
        label_visibility="collapsed"
    )

    st.markdown('<hr class="light">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Пороговые значения</div>', unsafe_allow_html=True)

    max_ecpm = st.slider("Макс. eCPM (после скидки), ₽", 0, 1000, 1000, step=10)
    min_ctr = st.slider("Мин. CTR, %", 0.0, 5.0, 0.0, step=0.1)
    min_reach = st.slider("Мин. охват, млн", 0.0, 80.0, 0.0, step=1.0)
    min_viewability = st.slider("Мин. Viewability, %", 0, 100, 0, step=5)
    min_vtr = st.slider("Мин. VTR, %", 0.0, 100.0, 0.0, step=5.0)

    st.markdown('<hr class="light">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Скоринг — веса (сумма = 100)</div>', unsafe_allow_html=True)

    w_reach = st.slider("Охват", 0, 100, 20, step=5)
    w_ecpm  = st.slider("eCPM (чем ниже — тем лучше)", 0, 100, 20, step=5)
    w_ctr   = st.slider("CTR", 0, 100, 20, step=5)
    w_vtr   = st.slider("VTR", 0, 100, 15, step=5)
    w_view  = st.slider("Viewability", 0, 100, 15, step=5)
    w_comm  = st.slider("Комиссия (чем ниже — тем лучше)", 0, 100, 10, step=5)

    total_w = w_reach + w_ecpm + w_ctr + w_vtr + w_view + w_comm
    color = "weight-ok" if total_w == 100 else "weight-bad"
    st.markdown(f'<div class="weight-total {color}">Итого: {total_w} / 100</div>', unsafe_allow_html=True)

    normalize = st.checkbox("Нормализовать веса автоматически", value=True)

    st.markdown('<hr class="light">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Сезонность</div>', unsafe_allow_html=True)
    months = ["Январь","Февраль","Март","Апрель","Май","Июнь",
              "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
    coeff_map = {
        "Январь":0.8,"Февраль":1.0,"Март":1.2,"Апрель":1.2,"Май":1.0,
        "Июнь":1.0,"Июль":1.0,"Август":1.0,"Сентябрь":1.25,
        "Октябрь":1.25,"Ноябрь":1.25,"Декабрь":1.25
    }
    selected_month = st.selectbox("Месяц размещения", months, index=2, label_visibility="collapsed")
    season_coeff = coeff_map[selected_month]
    st.markdown(f'<span style="font-size:0.75rem;color:#888;">Коэффициент сезонности: <b>{season_coeff}x</b></span>', unsafe_allow_html=True)

# ─── FILTERING ────────────────────────────────────────────────────────────────
def has_item(cell, items):
    if not isinstance(cell, list): return False
    return any(i in cell for i in items)

flt = df.copy()

if format_types:
    flt = flt[flt["format_type"].apply(lambda x: has_item(x, format_types))]
if devices:
    flt = flt[flt["device"].apply(lambda x: has_item(x, devices))]
if buy_models:
    flt = flt[flt["buy_model"].isin(buy_models)]

# Threshold filters
flt = flt[flt["ecpm_effective"].fillna(9999) <= max_ecpm]
if min_ctr > 0:
    flt = flt[flt["ctr_avg"].fillna(0) >= min_ctr / 100]
if min_reach > 0:
    flt = flt[flt["max_reach"].fillna(0) >= min_reach * 1_000_000]
if min_viewability > 0:
    flt = flt[flt["viewability_avg"].fillna(0) >= min_viewability / 100]
if min_vtr > 0:
    flt = flt[flt["vtr_avg"].fillna(0) >= min_vtr / 100]

# ─── SCORING ──────────────────────────────────────────────────────────────────
weights = {"reach": w_reach, "ecpm": w_ecpm, "ctr": w_ctr,
           "vtr": w_vtr, "view": w_view, "comm": w_comm}
total_w = sum(weights.values())

if normalize and total_w > 0:
    weights = {k: v / total_w for k, v in weights.items()}
else:
    weights = {k: v / 100 for k, v in weights.items()}

def normalize_col(series, invert=False):
    mn, mx = series.min(), series.max()
    if mx == mn: return pd.Series([0.5] * len(series), index=series.index)
    norm = (series - mn) / (mx - mn)
    return 1 - norm if invert else norm

if len(flt) > 0:
    # eCPM adjusted for seasonality
    flt = flt.copy()
    flt["ecpm_seasonal"] = flt["ecpm_effective"] * season_coeff

    s_reach = normalize_col(flt["max_reach"].fillna(0))
    s_ecpm  = normalize_col(flt["ecpm_seasonal"].fillna(flt["ecpm_seasonal"].max() * 2), invert=True)
    s_ctr   = normalize_col(flt["ctr_avg"].fillna(0))
    s_vtr   = normalize_col(flt["vtr_avg"].fillna(0))
    s_view  = normalize_col(flt["viewability_avg"].fillna(0))
    s_comm  = normalize_col(flt["commission"].fillna(flt["commission"].max()), invert=True)

    flt["score"] = (
        s_reach * weights["reach"] +
        s_ecpm  * weights["ecpm"] +
        s_ctr   * weights["ctr"] +
        s_vtr   * weights["vtr"] +
        s_view  * weights["view"] +
        s_comm  * weights["comm"]
    ) * 100

    flt = flt.sort_values("score", ascending=False).reset_index(drop=True)

# ─── KPI ROW ──────────────────────────────────────────────────────────────────
st.markdown('<div class="page-header"><h1>Format Selector</h1><span>Buzzoola · Анализ рекламных форматов</span></div>', unsafe_allow_html=True)

top = flt.iloc[0] if len(flt) > 0 else None

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Форматов после фильтров</div>
        <div class="kpi-value">{len(flt)}</div>
        <div class="kpi-sub">из {len(df)} всего</div>
    </div>""", unsafe_allow_html=True)
with col2:
    best_name = top["format_name"] if top is not None else "—"
    best_score = f'{top["score"]:.0f}' if top is not None else "—"
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Лучший формат</div>
        <div class="kpi-value" style="font-size:1rem;">{best_name}</div>
        <div class="kpi-sub">Score: {best_score}</div>
    </div>""", unsafe_allow_html=True)
with col3:
    avg_ecpm = flt["ecpm_seasonal"].mean() if len(flt) > 0 else np.nan
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Средний eCPM (с сезонностью)</div>
        <div class="kpi-value">{fmt_money(avg_ecpm)}</div>
        <div class="kpi-sub">Месяц: {selected_month} ({season_coeff}x)</div>
    </div>""", unsafe_allow_html=True)
with col4:
    max_reach_val = flt["max_reach"].max() if len(flt) > 0 else np.nan
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Макс. охват</div>
        <div class="kpi-value">{fmt_reach(max_reach_val)}</div>
        <div class="kpi-sub">среди отфильтрованных</div>
    </div>""", unsafe_allow_html=True)

# ─── TABLE ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Форматы</div>', unsafe_allow_html=True)

if len(flt) == 0:
    st.info("Нет форматов, соответствующих выбранным фильтрам.")
else:
    # Score color
    def score_badge(s):
        if pd.isna(s): return ""
        cls = "score-high" if s >= 65 else ("score-mid" if s >= 40 else "score-low")
        return f'<span class="score-pill {cls}">▲ {s:.0f}</span>'

    def type_tag(cell):
        if not isinstance(cell, list): return ""
        tags = []
        for t in cell:
            cls = "tag-video" if t == "Видео" else "tag-banner"
            tags.append(f'<span class="tag {cls}">{t}</span>')
        return "".join(tags)

    def model_tag(v):
        cls = "tag-cpm" if v == "CPM" else "tag-cpc"
        return f'<span class="tag {cls}">{v}</span>'

    def device_tags(cell):
        if not isinstance(cell, list): return ""
        return "".join(f'<span class="tag">{d}</span>' for d in cell)

    def metric_bar(value, max_val, display):
        if pd.isna(value) or pd.isna(max_val) or max_val == 0:
            return f'<span style="color:#CCC;font-size:0.75rem;">—</span>'
        pct = min(value / max_val * 100, 100)
        return f'''<div class="metric-bar-wrap">
            <div class="metric-bar-bg"><div class="metric-bar-fill" style="width:{pct}%"></div></div>
            <span class="metric-val">{display}</span>
        </div>'''

    max_reach_all = df["max_reach"].max()
    max_ecpm_all = df["ecpm_effective"].max()

    rows_html = ""
    for _, row in flt.iterrows():
        ecpm_s = row.get("ecpm_seasonal", np.nan)
        rows_html += f"""<tr>
            <td>
                <div class="format-name">{row['format_name']}</div>
                <div class="format-id">{row['format_id']}</div>
            </td>
            <td>{type_tag(row.get('format_type', []))}</td>
            <td>{model_tag(row['buy_model'])}</td>
            <td>{device_tags(row.get('device', []))}</td>
            <td>{metric_bar(row.get('max_reach'), max_reach_all, fmt_reach(row.get('max_reach')))}</td>
            <td>{metric_bar(row.get('ctr_avg'), 0.03, fmt_pct(row.get('ctr_avg')))}</td>
            <td>{metric_bar(row.get('viewability_avg'), 1.0, fmt_pct(row.get('viewability_avg')))}</td>
            <td style="font-family:'DM Mono',monospace;font-size:0.8rem;">{fmt_money(ecpm_s)}</td>
            <td>{score_badge(row.get('score', np.nan))}</td>
        </tr>"""

    st.markdown(f"""
    <table class="format-table">
        <thead><tr>
            <th>Формат</th><th>Тип</th><th>Модель</th><th>Устройство</th>
            <th>Охват</th><th>CTR</th><th>Viewability</th>
            <th>eCPM (сезон.)</th><th>Score</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

    # ─── FORMAT CARD ──────────────────────────────────────────────────────────
    st.markdown('<hr class="light">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Карточка формата</div>', unsafe_allow_html=True)

    format_names = flt["format_name"].tolist()
    selected_fmt = st.selectbox("Выберите формат для подробной информации",
                                 format_names, label_visibility="collapsed")

    row = flt[flt["format_name"] == selected_fmt].iloc[0]

    def tags_html(cell):
        if not isinstance(cell, list): return '<span style="color:#CCC;font-size:0.75rem;">—</span>'
        return "".join(f'<span class="tag">{t}</span>' for t in cell)

    def bool_icon(v):
        if v is True or v == "TRUE": return "✓"
        if v is False or v == "FALSE": return "—"
        return str(v) if not pd.isna(v) else "—"

    ecpm_eff = row.get("ecpm_effective", np.nan)
    ecpm_sea = row.get("ecpm_seasonal", np.nan)

    links = []
    for label, key in [("Пример", "example_url"), ("Техтребования", "technical_requirements_url"),
                        ("Медиакит", "mediakit_url"), ("Кейсы", "cases_url")]:
        val = row.get(key)
        if isinstance(val, str) and val.startswith("http"):
            links.append(f'<a href="{val}" target="_blank" style="font-size:0.78rem;color:#4F46E5;text-decoration:none;margin-right:12px;">{label} ↗</a>')

    st.markdown(f"""
    <div class="card-overlay">
        <div class="card-title">{row['format_name']}</div>
        <div class="card-id">{row['format_id']} · {row['buy_model']} · {row.get('platform','')}</div>
        <div class="card-desc">{row.get('description','—')}</div>

        <div class="card-grid">
            <div class="card-metric">
                <div class="card-metric-label">eCPM (факт)</div>
                <div class="card-metric-value">{fmt_money(ecpm_eff)}</div>
            </div>
            <div class="card-metric">
                <div class="card-metric-label">eCPM (сезон. {season_coeff}x)</div>
                <div class="card-metric-value">{fmt_money(ecpm_sea)}</div>
            </div>
            <div class="card-metric">
                <div class="card-metric-label">Скидка</div>
                <div class="card-metric-value">{fmt_pct(row.get('discount'))}</div>
            </div>
            <div class="card-metric">
                <div class="card-metric-label">Охват (max)</div>
                <div class="card-metric-value">{fmt_reach(row.get('max_reach'))}</div>
            </div>
            <div class="card-metric">
                <div class="card-metric-label">CTR (avg)</div>
                <div class="card-metric-value">{fmt_pct(row.get('ctr_avg'))}</div>
            </div>
            <div class="card-metric">
                <div class="card-metric-label">VTR (avg)</div>
                <div class="card-metric-value">{fmt_pct(row.get('vtr_avg'))}</div>
            </div>
            <div class="card-metric">
                <div class="card-metric-label">Viewability (avg)</div>
                <div class="card-metric-value">{fmt_pct(row.get('viewability_avg'))}</div>
            </div>
            <div class="card-metric">
                <div class="card-metric-label">Комиссия</div>
                <div class="card-metric-value">{fmt_pct(row.get('commission'))}</div>
            </div>
            <div class="card-metric">
                <div class="card-metric-label">Мин. бюджет</div>
                <div class="card-metric-value">{fmt_money(row.get('min_budget'))}</div>
            </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
                <div class="card-section">Ценовой диапазон</div>
                <div class="info-row">
                    <span class="info-label">CPM min/avg/max</span>
                    <span class="info-val">{fmt_money(row.get('cpm_min'))} / {fmt_money(row.get('cpm_avg'))} / {fmt_money(row.get('cpm_max'))}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">CPC min/avg/max</span>
                    <span class="info-val">{fmt_money(row.get('cpc_min'))} / {fmt_money(row.get('cpc_avg'))} / {fmt_money(row.get('cpc_max'))}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">CTR min/max</span>
                    <span class="info-val">{fmt_pct(row.get('ctr_min'))} / {fmt_pct(row.get('ctr_max'))}</span>
                </div>

                <div class="card-section">Верификация</div>
                <div class="info-row">
                    <span class="info-label">Pixel</span>
                    <span class="info-val">{bool_icon(row.get('verification_pixel'))}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">JS-тег</span>
                    <span class="info-val">{bool_icon(row.get('verification_js'))}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Условия</span>
                    <span class="info-val" style="font-size:0.75rem;color:#666;">{row.get('verification_terms','—') if not pd.isna(row.get('verification_terms','—')) else '—'}</span>
                </div>

                <div class="card-section">Дополнительно</div>
                <div class="info-row">
                    <span class="info-label">BLS</span>
                    <span class="info-val">{bool_icon(row.get('bls'))}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Sales Lift</span>
                    <span class="info-val">{bool_icon(row.get('sales_lift'))}</span>
                </div>
            </div>
            <div>
                <div class="card-section">Плейсмент</div>
                <div class="tags-row">{tags_html(row.get('placement'))}</div>

                <div class="card-section">Устройства</div>
                <div class="tags-row">{tags_html(row.get('device'))}</div>

                <div class="card-section">Отображение</div>
                <div class="tags-row">{tags_html(row.get('display'))}</div>

                <div class="card-section">DMP</div>
                <div class="tags-row">{tags_html(row.get('dmp'))}</div>

                <div class="card-section">Производство</div>
                <div class="tags-row">{tags_html(row.get('production'))}</div>
            </div>
        </div>

        <div class="card-section">Таргетинг</div>
        <div class="tags-row">{tags_html(row.get('targeting'))}</div>

        <div class="card-section">Наценки за таргетинг</div>
        <div class="tags-row">{tags_html(row.get('targeting_markup'))}</div>

        {'<div class="card-section">Ссылки</div><div>' + "".join(links) + "</div>" if links else ""}
    </div>
    """, unsafe_allow_html=True)

    # BLS / Sales Lift terms
    if isinstance(row.get("bls_terms"), str):
        with st.expander("📋 Условия BLS"):
            st.markdown(f'<div style="font-size:0.82rem;color:#444;line-height:1.6;">{row["bls_terms"]}</div>', unsafe_allow_html=True)
    if isinstance(row.get("sales_lift_terms"), str):
        with st.expander("📋 Условия Sales Lift"):
            st.markdown(f'<div style="font-size:0.82rem;color:#444;line-height:1.6;">{row["sales_lift_terms"]}</div>', unsafe_allow_html=True)
    if isinstance(row.get("seasonality_terms"), str):
        with st.expander("📋 Условия сезонности"):
            st.markdown(f'<div style="font-size:0.82rem;color:#444;line-height:1.6;">{row["seasonality_terms"]}</div>', unsafe_allow_html=True)
