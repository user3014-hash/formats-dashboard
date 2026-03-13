import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Format Selector",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PALETTE ──────────────────────────────────────────────────────────────────
# White: #FFFFFF  |  Mint: #C0FFD9  |  Blue: #3E20FF  |  Indigo: #725BFF
# Bg: #F8F2FF  |  Dark: #070037
# Accent text on dark bg: white. Muted: mix of dark+indigo at low opacity.

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap');

:root {
    --white:   #FFFFFF;
    --mint:    #C0FFD9;
    --blue:    #3E20FF;
    --indigo:  #725BFF;
    --bg:      #F8F2FF;
    --dark:    #070037;
    --muted:   #6B5C9E;
    --border:  #DDD5F0;
    --row-hover: #EDE5FF;
    --tag-bg:  #EDE5FF;
    --tag-video-bg: #D6FFEC;
    --tag-video-c:  #0A5C38;
    --tag-cpc-bg:   #D6E4FF;
    --tag-cpc-c:    #1A3A9C;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--dark);
}

section[data-testid="stSidebar"] {
    background: var(--white);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }
section[data-testid="stSidebar"] > div { padding: 0 1rem; }

.main { background: var(--bg); }
.main .block-container { padding: 1.5rem 2rem; max-width: 1500px; }

/* Page header */
.page-header {
    display: flex; align-items: baseline; gap: 12px;
    margin-bottom: 1.4rem; padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.page-header h1 { font-size: 1.25rem; font-weight: 600; color: var(--dark); margin: 0; }
.page-header span {
    font-size: 0.76rem; color: var(--muted);
    font-family: 'DM Mono', monospace;
}

/* Section labels */
.section-label {
    font-size: 0.61rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--muted);
    margin-bottom: 0.45rem; margin-top: 1rem;
}
.section-label-main {
    font-size: 0.61rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--muted);
    margin-bottom: 0.6rem; margin-top: 1.4rem;
}

/* KPI cards — equal height via flexbox column */
.kpi-row { display: flex; gap: 12px; align-items: stretch; }
.kpi-card {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 16px;
    display: flex; flex-direction: column; justify-content: space-between;
    animation: fadeUp 0.35s ease both;
}
.kpi-label { font-size: 0.68rem; color: var(--muted); font-weight: 500; margin-bottom: 6px; }
.kpi-value {
    font-size: 1.4rem; font-weight: 600; color: var(--dark);
    font-family: 'DM Mono', monospace; line-height: 1.2;
}
.kpi-value-sm {
    font-size: 0.98rem; font-weight: 600; color: var(--dark); line-height: 1.3;
}
.kpi-sub { font-size: 0.67rem; color: var(--muted); margin-top: 4px; }

/* Score badge */
.score-pill {
    display: inline-flex; align-items: center;
    padding: 2px 9px; border-radius: 20px;
    font-size: 0.71rem; font-weight: 600; font-family: 'DM Mono', monospace;
}
.score-high { background: var(--mint); color: #0A5C38; }
.score-mid  { background: var(--bg); color: var(--indigo); border: 1px solid var(--border); }
.score-low  { background: #EDE5FF; color: var(--muted); border: 1px solid var(--border); }

/* Table */
.fmt-table-wrap {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 10px; overflow: hidden;
    animation: fadeUp 0.4s ease both;
}
.format-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.format-table th {
    text-align: left; padding: 9px 14px;
    background: var(--bg); border-bottom: 1px solid var(--border);
    font-size: 0.63rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--muted); white-space: nowrap;
}
.format-table td {
    padding: 11px 14px; border-bottom: 1px solid #EDE5FF;
    vertical-align: middle; color: var(--dark);
}
.format-table tr:last-child td { border-bottom: none; }
.format-table tbody tr {
    cursor: pointer;
    transition: background 0.12s ease;
}
.format-table tbody tr:hover td { background: var(--row-hover); }
.format-table tbody tr.selected td { background: #E2D9FF; }
.format-name { font-weight: 500; color: var(--dark); }
.format-id {
    font-family: 'DM Mono', monospace; font-size: 0.67rem;
    color: var(--muted); margin-top: 2px;
}

/* Tags */
.tag {
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 0.66rem; font-weight: 500; margin: 1px 2px 1px 0;
    background: var(--tag-bg); color: var(--dark);
}
.tag-video  { background: var(--tag-video-bg); color: var(--tag-video-c); }
.tag-banner { background: #EDE5FF; color: var(--indigo); }
.tag-cpm    { background: var(--bg); color: var(--dark); border: 1px solid var(--border); }
.tag-cpc    { background: var(--tag-cpc-bg); color: var(--tag-cpc-c); }

/* Metric bar */
.metric-bar-wrap { display: flex; align-items: center; gap: 7px; }
.metric-bar-bg { height: 4px; background: var(--border); border-radius: 3px; flex: 1; min-width: 50px; }
.metric-bar-fill { height: 4px; border-radius: 3px; background: var(--blue); }
.metric-val {
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
    color: var(--dark); min-width: 44px; text-align: right;
}

/* Divider */
hr.light { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }

/* Card overlay */
.card-overlay {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 12px; padding: 22px; margin-top: 12px;
    animation: fadeUp 0.3s ease both;
}
.card-title { font-size: 1.05rem; font-weight: 600; color: var(--dark); margin-bottom: 3px; }
.card-id {
    font-family: 'DM Mono', monospace; font-size: 0.69rem;
    color: var(--muted); margin-bottom: 12px;
}
.card-desc {
    font-size: 0.81rem; color: var(--dark); line-height: 1.65;
    margin-bottom: 14px; padding: 10px 14px;
    background: var(--bg); border-radius: 8px;
}
.card-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 9px; margin-bottom: 14px;
}
.card-metric { background: var(--bg); border-radius: 8px; padding: 10px 12px; }
.card-metric-label {
    font-size: 0.62rem; color: var(--muted); font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 4px;
}
.card-metric-value {
    font-size: 1rem; font-weight: 600; color: var(--dark);
    font-family: 'DM Mono', monospace;
}
.card-section {
    font-size: 0.62rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--muted); margin: 12px 0 6px;
}
.tags-row { display: flex; flex-wrap: wrap; gap: 4px; }
.info-row { display: flex; gap: 8px; margin-bottom: 6px; font-size: 0.8rem; }
.info-label { color: var(--muted); min-width: 160px; flex-shrink: 0; }
.info-val { color: var(--dark); font-weight: 500; }
.bool-yes { color: var(--blue); font-weight: 700; }
.bool-no  { color: #CCC; }

/* Scoring */
.weight-total-wrap {
    display: inline-block;
    font-size: 0.76rem; font-weight: 600;
    font-family: 'DM Mono', monospace;
    padding: 3px 10px; border-radius: 6px; margin-top: 4px;
}
.weight-ok  { background: var(--mint); color: #0A5C38; }
.weight-bad { background: #EDE5FF; color: var(--indigo); }

/* Animations */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* No results */
.no-results {
    text-align: center; padding: 40px 20px; color: var(--muted);
    font-size: 0.88rem; background: var(--white);
    border: 1px solid var(--border); border-radius: 10px;
}

/* Streamlit overrides */
div[data-testid="stSlider"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stCheckbox"] label {
    font-size: 0.77rem !important; color: var(--dark) !important;
}
div[data-testid="stCheckbox"] { margin-top: 0.15rem; }
/* Fix toggle spacing */
div[data-testid="stToggle"] { margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    def p(name): return os.path.join(base, name)

    def read_csv(a, b):
        for name in [a, b]:
            fp = p(name)
            if os.path.exists(fp):
                return pd.read_csv(fp)
        raise FileNotFoundError(f"Файл не найден: {a} или {b}")

    df = read_csv("DataLens_-_formats.csv", "DataLens - formats.csv")
    di = read_csv("DataLens_-_dict_items.csv", "DataLens - dict_items.csv")

    fi = None
    for name in ["DataLens_-_format_items.csv", "DataLens - format_items.csv"]:
        if os.path.exists(p(name)):
            fi = pd.read_csv(p(name)); break
    if fi is None:
        for name in ["DataLens.xlsx"]:
            if os.path.exists(p(name)):
                fi = pd.read_excel(p(name), sheet_name="format_items"); break
    if fi is None:
        raise FileNotFoundError("Не найден файл format_items")

    merged = fi.merge(di[["dict_id", "item_id", "item_name"]], on=["dict_id", "item_id"], how="left")
    pivot = merged.groupby(["format_id", "dict_id"])["item_name"].apply(list).unstack("dict_id").reset_index()
    df = df.merge(pivot, on="format_id", how="left")
    return df, di

df, di = load_data()

# ─── SEASONALITY ──────────────────────────────────────────────────────────────
BASE_SEASON_MAP = {
    "Январь":0.80,"Февраль":1.00,"Март":1.20,"Апрель":1.20,"Май":1.00,
    "Июнь":1.00,"Июль":1.00,"Август":1.00,"Сентябрь":1.25,
    "Октябрь":1.25,"Ноябрь":1.25,"Декабрь":1.25
}
def get_season_coeff(platform, month):
    if str(platform) in {"Buzzoola"}:
        return BASE_SEASON_MAP.get(month, 1.0)
    return 1.0

# ─── FORMATTERS ───────────────────────────────────────────────────────────────
def fmt_pct(v):
    """Format as %, using comma as decimal separator, no trailing zeros."""
    if pd.isna(v): return "—"
    pct = v * 100
    rounded = round(pct, 1)
    if rounded == int(rounded):
        return f"{int(rounded)}%"
    # Use comma as decimal separator
    return f"{rounded:.1f}%".replace(".", ",")

def fmt_money(v):
    """Format as ₽ with narrow space separator, no decimals."""
    if pd.isna(v): return "—"
    iv = int(round(v))
    s = f"{iv:,}".replace(",", "\u202f")
    return f"{s} ₽"

def fmt_reach(v):
    if pd.isna(v): return "—"
    m = v / 1_000_000
    if m >= 1:
        return f"{int(m)}M" if m == int(m) else f"{m:.1f}M".replace(".", ",")
    return f"{int(v):,}".replace(",", "\u202f")

def bool_icon(v):
    try:
        if pd.isna(v):
            return '<span class="bool-no">—</span>'
    except Exception:
        pass
    if str(v).upper() in ("TRUE", "1"):
        return '<span class="bool-yes">✓</span>'
    return '<span class="bool-no">—</span>'

def safe_str(v):
    try:
        if pd.isna(v): return "—"
    except Exception:
        pass
    s = str(v).strip()
    return s if s else "—"

# ─── eCPM CALCULATION ─────────────────────────────────────────────────────────
def calc_ecpm(row):
    model = str(row.get("buy_model", "CPM")).strip().upper()
    ctr = row.get("ctr_avg", np.nan)
    discount = float(row.get("discount", 0) or 0)
    if model == "CPM":
        raw = row.get("cpm_avg", np.nan)
    elif model == "CPC":
        cpc = row.get("cpc_avg", np.nan)
        raw = cpc * ctr * 1000 if not (pd.isna(cpc) or pd.isna(ctr) or ctr == 0) else np.nan
    elif model == "CPV":
        cpv = row.get("cpv_avg", np.nan)
        vtr = row.get("vtr_avg", np.nan)
        raw = cpv * vtr * 1000 if not (pd.isna(cpv) or pd.isna(vtr) or vtr == 0) else np.nan
    else:
        raw = row.get("cpm_avg", np.nan)
    if pd.isna(raw): return np.nan
    return raw * (1 - discount)

df["ecpm_effective"] = df.apply(calc_ecpm, axis=1)

# ─── DICT OPTIONS ─────────────────────────────────────────────────────────────
def dict_opts(dict_id):
    return di[di["dict_id"] == dict_id]["item_name"].dropna().tolist()

all_targeting   = dict_opts("targeting")
all_dmp         = dict_opts("dmp")
all_display     = dict_opts("display")       # banner: Статичный, Анимационный, Интерактивный
all_placement   = dict_opts("placement")     # video: In-stream, Out-stream, Smart TV
all_instream    = dict_opts("instream_pos")  # video: Pre-roll

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-label">Тип формата</div>', unsafe_allow_html=True)
    format_types = st.multiselect("Тип", ["Видео", "Баннер"], default=["Видео", "Баннер"],
                                   placeholder="Все типы",
                                   label_visibility="collapsed")

    st.markdown('<div class="section-label">Устройство</div>', unsafe_allow_html=True)
    devices = st.multiselect("Устройство",
                              ["Desktop", "Mobile Web", "In-App", "Smart TV"],
                              default=["Desktop", "Mobile Web", "In-App", "Smart TV"],
                              placeholder="Все устройства",
                              label_visibility="collapsed")

    st.markdown('<div class="section-label">Модель закупки</div>', unsafe_allow_html=True)
    buy_models = st.multiselect("Модель", ["CPM", "CPC"], default=["CPM", "CPC"],
                                 placeholder="Все модели",
                                 label_visibility="collapsed")

    # — Conditional filters by format type —
    show_banner_filters = not format_types or "Баннер" in format_types
    show_video_filters  = not format_types or "Видео"  in format_types

    if show_banner_filters:
        st.markdown('<div class="section-label">Баннер — отображение</div>', unsafe_allow_html=True)
        filter_display = st.multiselect("Отображение", all_display, default=[],
                                         placeholder="Все варианты",
                                         label_visibility="collapsed")
    else:
        filter_display = []

    if show_video_filters:
        st.markdown('<div class="section-label">Видео — плейсмент</div>', unsafe_allow_html=True)
        filter_placement = st.multiselect("Плейсмент", all_placement, default=[],
                                           placeholder="Все плейсменты",
                                           label_visibility="collapsed")
        st.markdown('<div class="section-label">Видео — позиция</div>', unsafe_allow_html=True)
        filter_instream = st.multiselect("Позиция", all_instream, default=[],
                                          placeholder="Все позиции",
                                          label_visibility="collapsed")
    else:
        filter_placement = []
        filter_instream  = []

    st.markdown('<div class="section-label">Таргетинги</div>', unsafe_allow_html=True)
    filter_targeting = st.multiselect("Таргетинги", all_targeting, default=[],
                                       placeholder="Все таргетинги",
                                       label_visibility="collapsed")

    st.markdown('<div class="section-label">DMP</div>', unsafe_allow_html=True)
    filter_dmp = st.multiselect("DMP", all_dmp, default=[],
                                 placeholder="Все DMP",
                                 label_visibility="collapsed")

    st.markdown('<div class="section-label">Дополнительно</div>', unsafe_allow_html=True)
    req_pixel     = st.checkbox("Верификация пикселем")
    req_js        = st.checkbox("Верификация JS-тегом")
    req_brandlift = st.checkbox("Brand Lift")
    req_saleslift = st.checkbox("Sales Lift")

    st.markdown('<hr class="light">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Пороговые значения</div>', unsafe_allow_html=True)
    max_ecpm_thresh = st.slider("Макс. eCPM (после скидки), ₽", 0, 1000, 1000, step=10)
    min_ctr   = st.slider("Мин. CTR, %",         0.0,  5.0, 0.0, step=0.1)
    min_reach = st.slider("Мин. охват, млн",      0.0, 80.0, 0.0, step=1.0)
    min_view  = st.slider("Мин. Viewability, %",  0,   100,  0,   step=5)
    min_vtr   = st.slider("Мин. VTR, %",          0.0, 100.0,0.0, step=5.0)

    st.markdown('<hr class="light">', unsafe_allow_html=True)
    scoring_on = st.toggle("Включить скоринг", value=False)

    if scoring_on:
        st.markdown('<div class="section-label">Веса (сумма = 100)</div>', unsafe_allow_html=True)
        w_reach = st.slider("Охват",               0, 100, 20, step=5)
        w_ecpm  = st.slider("eCPM (ниже — лучше)", 0, 100, 20, step=5)
        w_ctr   = st.slider("CTR",                 0, 100, 20, step=5)
        w_vtr   = st.slider("VTR",                 0, 100, 15, step=5)
        w_view  = st.slider("Viewability",         0, 100, 15, step=5)
        w_comm  = st.slider("Комиссия (ниже — лучше)", 0, 100, 10, step=5)
        total_w = w_reach + w_ecpm + w_ctr + w_vtr + w_view + w_comm
        cls = "weight-ok" if total_w == 100 else "weight-bad"
        st.markdown(
            f'<div class="weight-total-wrap {cls}">Сумма: {total_w} / 100</div>',
            unsafe_allow_html=True
        )
        normalize = st.checkbox("Нормализовать веса", value=True)
    else:
        w_reach = w_ecpm = w_ctr = w_vtr = w_view = w_comm = 0
        total_w = 0; normalize = False

    st.markdown('<hr class="light">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Сезонность</div>', unsafe_allow_html=True)
    months = ["Январь","Февраль","Март","Апрель","Май","Июнь",
              "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
    selected_month = st.selectbox("Месяц", months,
                                   index=months.index("Март"),
                                   label_visibility="collapsed")

# ─── FILTERING ────────────────────────────────────────────────────────────────
def has_item(cell, items):
    if not isinstance(cell, list): return False
    return any(i in cell for i in items)

def has_all_items(cell, items):
    if not items: return True
    if not isinstance(cell, list): return False
    return all(i in cell for i in items)

flt = df.copy()
if format_types:
    flt = flt[flt["format_type"].apply(lambda x: has_item(x, format_types))]
if devices:
    flt = flt[flt["device"].apply(lambda x: has_item(x, devices))]
if buy_models:
    flt = flt[flt["buy_model"].isin(buy_models)]
if filter_display:
    flt = flt[flt["display"].apply(lambda x: has_all_items(x, filter_display))]
if filter_placement:
    flt = flt[flt["placement"].apply(lambda x: has_all_items(x, filter_placement))]
if filter_instream:
    flt = flt[flt["instream_pos"].apply(lambda x: has_all_items(x, filter_instream))]
if filter_targeting:
    flt = flt[flt["targeting"].apply(lambda x: has_all_items(x, filter_targeting))]
if filter_dmp:
    flt = flt[flt["dmp"].apply(lambda x: has_all_items(x, filter_dmp))]
if req_pixel:
    flt = flt[flt["verification_pixel"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
if req_js:
    flt = flt[flt["verification_js"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
if req_brandlift:
    flt = flt[flt["bls"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
if req_saleslift:
    flt = flt[flt["sales_lift"].apply(lambda v: str(v).upper() in ("TRUE","1"))]

flt = flt[flt["ecpm_effective"].fillna(9999) <= max_ecpm_thresh]
if min_ctr > 0:
    flt = flt[flt["ctr_avg"].fillna(0) >= min_ctr / 100]
if min_reach > 0:
    flt = flt[flt["max_reach"].fillna(0) >= min_reach * 1_000_000]
if min_view > 0:
    flt = flt[flt["viewability_avg"].fillna(0) >= min_view / 100]
if min_vtr > 0:
    flt = flt[flt["vtr_avg"].fillna(0) >= min_vtr / 100]

# ─── SEASONAL eCPM ────────────────────────────────────────────────────────────
flt = flt.copy()
flt["season_coeff"] = flt["platform"].apply(lambda p: get_season_coeff(p, selected_month))
flt["ecpm_seasonal"] = flt["ecpm_effective"] * flt["season_coeff"]

# ─── SCORING ──────────────────────────────────────────────────────────────────
def normalize_col(series, invert=False):
    mn, mx = series.min(), series.max()
    if mx == mn: return pd.Series([0.5] * len(series), index=series.index)
    norm = (series - mn) / (mx - mn)
    return 1 - norm if invert else norm

if scoring_on and len(flt) > 0:
    weights = {"reach": w_reach, "ecpm": w_ecpm, "ctr": w_ctr,
               "vtr": w_vtr, "view": w_view, "comm": w_comm}
    tw = sum(weights.values())
    if normalize and tw > 0:
        weights = {k: v / tw for k, v in weights.items()}
    else:
        weights = {k: v / 100 for k, v in weights.items()}

    ev = flt["ecpm_seasonal"].max() * 2 if flt["ecpm_seasonal"].notna().any() else 9999
    cv = flt["commission"].max() if flt["commission"].notna().any() else 1

    s_reach = normalize_col(flt["max_reach"].fillna(0))
    s_ecpm  = normalize_col(flt["ecpm_seasonal"].fillna(ev), invert=True)
    s_ctr   = normalize_col(flt["ctr_avg"].fillna(0))
    s_vtr   = normalize_col(flt["vtr_avg"].fillna(0))
    s_view  = normalize_col(flt["viewability_avg"].fillna(0))
    s_comm  = normalize_col(flt["commission"].fillna(cv), invert=True)

    flt["score"] = (
        s_reach * weights["reach"] + s_ecpm * weights["ecpm"] +
        s_ctr   * weights["ctr"]   + s_vtr  * weights["vtr"] +
        s_view  * weights["view"]  + s_comm * weights["comm"]
    ) * 100
    flt = flt.sort_values("score", ascending=False).reset_index(drop=True)
else:
    flt["score"] = np.nan
    flt = flt.sort_values("ecpm_seasonal", ascending=True, na_position="last").reset_index(drop=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
# Platform label: later will list all loaded platforms
platforms = sorted(df["platform"].dropna().unique().tolist())
platform_label = " · ".join(platforms) if platforms else "—"

st.markdown(
    f'<div class="page-header">'
    f'<h1>Format Selector</h1>'
    f'<span>{platform_label} · Анализ рекламных форматов</span>'
    f'</div>',
    unsafe_allow_html=True
)

# ─── KPI ROW ─────────────────────────────────────────────────────────────────
top = flt.iloc[0] if len(flt) > 0 else None
avg_ecpm = flt["ecpm_seasonal"].mean() if len(flt) > 0 else np.nan
sc_shown = flt["season_coeff"].iloc[0] if len(flt) > 0 else 1.0
max_reach_val = flt["max_reach"].max() if len(flt) > 0 else np.nan

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="kpi-card">
        <div>
            <div class="kpi-label">Форматов после фильтров</div>
            <div class="kpi-value">{len(flt)}</div>
        </div>
        <div class="kpi-sub">из {len(df)} доступных</div>
    </div>""", unsafe_allow_html=True)
with c2:
    if top is not None:
        lbl = "Лучший по скорингу" if scoring_on else "Самый дешевый eCPM"
        sub = f'Скор: {top["score"]:.0f}' if (scoring_on and not pd.isna(top.get("score", np.nan))) else top["buy_model"]
        st.markdown(f"""<div class="kpi-card">
            <div>
                <div class="kpi-label">{lbl}</div>
                <div class="kpi-value-sm">{top['format_name']}</div>
            </div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="kpi-card"><div class="kpi-label">Лучший формат</div><div class="kpi-value">—</div><div class="kpi-sub">&nbsp;</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card">
        <div>
            <div class="kpi-label">Средний eCPM (с сезонностью)</div>
            <div class="kpi-value">{fmt_money(avg_ecpm)}</div>
        </div>
        <div class="kpi-sub">{selected_month} · коэф. {sc_shown}×</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card">
        <div>
            <div class="kpi-label">Макс. охват</div>
            <div class="kpi-value">{fmt_reach(max_reach_val)}</div>
        </div>
        <div class="kpi-sub">среди отфильтрованных</div>
    </div>""", unsafe_allow_html=True)

# ─── CHARTS ───────────────────────────────────────────────────────────────────
if len(flt) > 0:
    try:
        import plotly.graph_objects as go

        ch1, ch2 = st.columns(2)

        with ch1:
            cdf = flt[flt["ecpm_seasonal"].notna()].sort_values("ecpm_seasonal")
            if len(cdf) > 0:
                colors = ["#3E20FF" if i == 0 else "#725BFF" for i in range(len(cdf))]
                fig = go.Figure(go.Bar(
                    x=cdf["ecpm_seasonal"], y=cdf["format_name"],
                    orientation="h",
                    marker_color=colors,
                    marker_line_width=0,
                    hovertemplate="<b>%{y}</b><br>eCPM: %{x:.0f} ₽<extra></extra>"
                ))
                fig.update_layout(
                    title=dict(text="eCPM по форматам (с учетом сезонности)",
                               font_size=11, font_color="#6B5C9E", font_family="DM Sans"),
                    height=max(240, len(cdf) * 34),
                    margin=dict(l=0, r=16, t=36, b=0),
                    paper_bgcolor="white", plot_bgcolor="white",
                    xaxis=dict(gridcolor="#EDE5FF", tickfont_size=10,
                               title=None, tickfont_color="#6B5C9E"),
                    yaxis=dict(tickfont_size=10, title=None, tickfont_color="#070037"),
                    font_family="DM Sans",
                    transition={"duration": 400, "easing": "cubic-in-out"}
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with ch2:
            sdf = flt[flt["ctr_avg"].notna() & flt["viewability_avg"].notna()].copy()
            if len(sdf) >= 2:
                med = sdf["max_reach"].median()
                sdf["bubble"] = sdf["max_reach"].fillna(med).apply(
                    lambda v: max(10, min(34, v / 2_500_000))
                )
                # Score-based coloring
                if scoring_on and sdf["score"].notna().any():
                    norm = (sdf["score"] - sdf["score"].min()) / max(sdf["score"].max() - sdf["score"].min(), 1)
                    marker_colors = [f"rgba(62,32,255,{0.4 + 0.6 * n:.2f})" for n in norm]
                else:
                    marker_colors = ["#725BFF"] * len(sdf)

                fig2 = go.Figure()
                for i, (_, r) in enumerate(sdf.iterrows()):
                    fig2.add_trace(go.Scatter(
                        x=[r["ctr_avg"] * 100], y=[r["viewability_avg"] * 100],
                        mode="markers+text",
                        marker=dict(size=r["bubble"], color=marker_colors[i],
                                    line=dict(color="white", width=1.5)),
                        text=[r["format_name"]],
                        textposition="top center",
                        textfont=dict(size=8, color="#070037"),
                        hovertemplate=(f"<b>{r['format_name']}</b><br>"
                                       f"CTR: {r['ctr_avg']*100:.2f}%<br>"
                                       f"Viewability: {r['viewability_avg']*100:.0f}%<extra></extra>"),
                        showlegend=False
                    ))
                fig2.update_layout(
                    title=dict(text="CTR vs Viewability (размер — охват)",
                               font_size=11, font_color="#6B5C9E", font_family="DM Sans"),
                    height=300, margin=dict(l=0, r=16, t=36, b=0),
                    paper_bgcolor="white", plot_bgcolor="white",
                    xaxis=dict(title="CTR, %", gridcolor="#EDE5FF",
                               tickfont_size=10, title_font_size=10,
                               tickfont_color="#6B5C9E", title_font_color="#6B5C9E"),
                    yaxis=dict(title="Viewability, %", gridcolor="#EDE5FF",
                               tickfont_size=10, title_font_size=10,
                               tickfont_color="#6B5C9E", title_font_color="#6B5C9E"),
                    font_family="DM Sans",
                    transition={"duration": 400, "easing": "cubic-in-out"}
                )
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    except ImportError:
        pass

# ─── TABLE ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label-main">Форматы</div>', unsafe_allow_html=True)

# Store selected format in session state (click-based selection)
if "selected_format_id" not in st.session_state:
    st.session_state["selected_format_id"] = None

if len(flt) == 0:
    st.markdown('<div class="no-results">Нет форматов, соответствующих выбранным фильтрам.</div>',
                unsafe_allow_html=True)
else:
    def score_badge(s):
        if pd.isna(s): return ""
        cls = "score-high" if s >= 65 else ("score-mid" if s >= 40 else "score-low")
        return f'<span class="score-pill {cls}">{s:.0f}</span>'

    def type_tag(cell):
        if not isinstance(cell, list): return ""
        out = []
        for t in cell:
            out.append(f'<span class="tag {"tag-video" if t == "Видео" else "tag-banner"}">{t}</span>')
        return "".join(out)

    def model_tag(v):
        cls = "tag-cpm" if str(v).upper() == "CPM" else "tag-cpc"
        return f'<span class="tag {cls}">{v}</span>'

    def device_tags(cell):
        if not isinstance(cell, list): return ""
        return "".join(f'<span class="tag">{d}</span>' for d in cell)

    def metric_bar(value, max_val, display):
        if pd.isna(value) or pd.isna(max_val) or max_val == 0:
            return '<span style="color:#CCC;font-size:0.75rem;">—</span>'
        pct = min(value / max_val * 100, 100)
        return (f'<div class="metric-bar-wrap">'
                f'<div class="metric-bar-bg">'
                f'<div class="metric-bar-fill" style="width:{pct:.1f}%"></div></div>'
                f'<span class="metric-val">{display}</span></div>')

    max_reach_all = df["max_reach"].max()
    last_th = "<th>Скор</th>" if scoring_on else "<th>eCPM (сез.)</th>"
    sel_id = st.session_state.get("selected_format_id")

    rows_html = ""
    fmt_id_list = []
    for _, row in flt.iterrows():
        fid = row["format_id"]
        fmt_id_list.append(fid)
        ecpm_s = row.get("ecpm_seasonal", np.nan)
        selected_cls = "selected" if fid == sel_id else ""

        if scoring_on:
            last_td = score_badge(row.get("score", np.nan))
        else:
            last_td = f'<span style="font-family:\'DM Mono\',monospace;font-size:0.79rem;">{fmt_money(ecpm_s)}</span>'

        rows_html += f"""<tr class="{selected_cls}" onclick="selectFormat('{fid}')">
            <td><div class="format-name">{row['format_name']}</div>
                <div class="format-id">{fid}</div></td>
            <td>{type_tag(row.get('format_type', []))}</td>
            <td>{model_tag(row['buy_model'])}</td>
            <td>{device_tags(row.get('device', []))}</td>
            <td>{metric_bar(row.get('max_reach'), max_reach_all, fmt_reach(row.get('max_reach')))}</td>
            <td>{metric_bar(row.get('ctr_avg'), 0.03, fmt_pct(row.get('ctr_avg')))}</td>
            <td>{metric_bar(row.get('viewability_avg'), 1.0, fmt_pct(row.get('viewability_avg')))}</td>
            <td>{last_td}</td>
        </tr>"""

    # JS click → Streamlit query param trick via URL hash
    st.markdown(f"""
    <div class="fmt-table-wrap">
    <table class="format-table">
        <thead><tr>
            <th>Формат</th><th>Тип</th><th>Модель</th><th>Устройство</th>
            <th>Охват</th><th>CTR</th><th>Viewability</th>{last_th}
        </tr></thead>
        <tbody id="fmt-tbody">{rows_html}</tbody>
    </table>
    </div>
    <script>
    function selectFormat(fid) {{
        // Store in sessionStorage, then signal Streamlit via fragment
        sessionStorage.setItem('selected_fid', fid);
        window.location.hash = 'fmt_' + fid;
    }}
    // Highlight on load
    var stored = sessionStorage.getItem('selected_fid');
    if (stored) {{
        document.querySelectorAll('#fmt-tbody tr').forEach(function(tr) {{
            if (tr.getAttribute('onclick') && tr.getAttribute('onclick').includes(stored)) {{
                tr.classList.add('selected');
            }}
        }});
    }}
    </script>
    """, unsafe_allow_html=True)

    # ─ Click detection via st.query_params (hash routing) ─
    # Fallback: use a native Streamlit selectbox that mirrors the table
    st.markdown('<hr class="light">', unsafe_allow_html=True)
    st.markdown('<div class="section-label-main">Карточка формата</div>', unsafe_allow_html=True)
    st.caption("Нажмите на формат в таблице или выберите из списка")

    fmt_options = ["— не выбрано —"] + flt["format_name"].tolist()
    # Pre-select if session state has a valid id
    preselect_idx = 0
    if sel_id and sel_id in flt["format_id"].values:
        fname = flt[flt["format_id"] == sel_id]["format_name"].iloc[0]
        if fname in fmt_options:
            preselect_idx = fmt_options.index(fname)

    selected_fmt = st.selectbox("Выберите формат", fmt_options,
                                 index=preselect_idx,
                                 label_visibility="collapsed")

    if selected_fmt != "— не выбрано —":
        row = flt[flt["format_name"] == selected_fmt].iloc[0]

        def tags_html(cell):
            if not isinstance(cell, list):
                return '<span style="color:#CCC;font-size:0.75rem;">—</span>'
            return "".join(f'<span class="tag">{t}</span>' for t in cell)

        ecpm_eff = row.get("ecpm_effective", np.nan)
        ecpm_sea = row.get("ecpm_seasonal", np.nan)
        sc = row.get("season_coeff", 1.0)

        links = []
        for lbl, key in [("Пример", "example_url"),
                          ("Техтребования", "technical_requirements_url"),
                          ("Медиакит", "mediakit_url"),
                          ("Кейсы", "cases_url")]:
            val = row.get(key)
            if isinstance(val, str) and val.startswith("http"):
                links.append(
                    f'<a href="{val}" target="_blank" '
                    f'style="font-size:0.78rem;color:#3E20FF;text-decoration:none;'
                    f'margin-right:14px;font-weight:500;">{lbl} ↗</a>'
                )

        st.markdown(f"""
        <div class="card-overlay">
            <div class="card-title">{row['format_name']}</div>
            <div class="card-id">{row['format_id']} · {row['buy_model']} · {row.get('platform', '')}</div>
            <div class="card-desc">{safe_str(row.get('description'))}</div>

            <div class="card-grid">
                <div class="card-metric">
                    <div class="card-metric-label">eCPM (факт)</div>
                    <div class="card-metric-value">{fmt_money(ecpm_eff)}</div>
                </div>
                <div class="card-metric">
                    <div class="card-metric-label">eCPM (сезон. {sc}×)</div>
                    <div class="card-metric-value">{fmt_money(ecpm_sea)}</div>
                </div>
                <div class="card-metric">
                    <div class="card-metric-label">Скидка</div>
                    <div class="card-metric-value">{fmt_pct(row.get('discount'))}</div>
                </div>
                <div class="card-metric">
                    <div class="card-metric-label">Охват (макс.)</div>
                    <div class="card-metric-value">{fmt_reach(row.get('max_reach'))}</div>
                </div>
                <div class="card-metric">
                    <div class="card-metric-label">CTR (среднее)</div>
                    <div class="card-metric-value">{fmt_pct(row.get('ctr_avg'))}</div>
                </div>
                <div class="card-metric">
                    <div class="card-metric-label">VTR (среднее)</div>
                    <div class="card-metric-value">{fmt_pct(row.get('vtr_avg'))}</div>
                </div>
                <div class="card-metric">
                    <div class="card-metric-label">Viewability (среднее)</div>
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
                        <span class="info-label">CPM мин / сред / макс</span>
                        <span class="info-val">{fmt_money(row.get('cpm_min'))} / {fmt_money(row.get('cpm_avg'))} / {fmt_money(row.get('cpm_max'))}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">CPC мин / сред / макс</span>
                        <span class="info-val">{fmt_money(row.get('cpc_min'))} / {fmt_money(row.get('cpc_avg'))} / {fmt_money(row.get('cpc_max'))}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">CTR мин / макс</span>
                        <span class="info-val">{fmt_pct(row.get('ctr_min'))} / {fmt_pct(row.get('ctr_max'))}</span>
                    </div>
                    <div class="card-section">Верификация</div>
                    <div class="info-row">
                        <span class="info-label">Пиксель</span>
                        <span class="info-val">{bool_icon(row.get('verification_pixel'))}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">JS-тег</span>
                        <span class="info-val">{bool_icon(row.get('verification_js'))}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Условия верификации</span>
                        <span class="info-val" style="font-size:0.75rem;color:#6B5C9E;">{safe_str(row.get('verification_terms'))}</span>
                    </div>
                    <div class="card-section">Исследования</div>
                    <div class="info-row">
                        <span class="info-label">Brand Lift</span>
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

            {'<div class="card-section">Ссылки</div><div style="margin-top:6px;">' + "".join(links) + "</div>" if links else ""}
        </div>
        """, unsafe_allow_html=True)

        for lbl, key in [("Условия Brand Lift", "bls_terms"),
                          ("Условия Sales Lift", "sales_lift_terms"),
                          ("Условия сезонности", "seasonality_terms")]:
            val = row.get(key)
            if isinstance(val, str) and val.strip():
                with st.expander(f"📋 {lbl}"):
                    st.markdown(
                        f'<div style="font-size:0.82rem;color:#070037;line-height:1.65;">{val}</div>',
                        unsafe_allow_html=True
                    )
