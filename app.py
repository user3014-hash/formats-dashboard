import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Format Selector",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM
# Palette: #FFFFFF · #C0FFD9 · #3E20FF · #725BFF · #F8F2FF · #070037
# Sidebar: dark (#070037) background, white text — clear hierarchy
# Main: light (#F8F2FF) background
# Accents: blue (#3E20FF) primary, mint (#C0FFD9) success/highlight
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');

:root {
    --white:   #FFFFFF;
    --mint:    #C0FFD9;
    --blue:    #3E20FF;
    --indigo:  #725BFF;
    --bg:      #F8F2FF;
    --dark:    #070037;
    --muted:   rgba(7,0,55,0.42);
    --border:  rgba(7,0,55,0.10);
    --row-h:   rgba(62,32,255,0.05);
    --sel-row: rgba(62,32,255,0.09);
}

/* ── Base ── */
html, body { background: var(--bg) !important; }
*, *::before, *::after { font-family: 'DM Sans', sans-serif !important; box-sizing: border-box; }
.main { background: var(--bg) !important; }
.main .block-container { padding: 1.5rem 2.2rem 2rem !important; max-width: 1480px; }

/* ── Sidebar: dark background ── */
section[data-testid="stSidebar"] {
    background: var(--dark) !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] .block-container { padding-top: 0 !important; }
section[data-testid="stSidebar"] > div { padding: 0 !important; }
/* All sidebar text: white */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span:not([data-baseweb="tag"] span),
section[data-testid="stSidebar"] div:not([data-baseweb]) {
    color: rgba(255,255,255,0.85) !important;
    font-size: 13px !important;
}
/* Sidebar widget inputs */
section[data-testid="stSidebar"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-baseweb="input"] {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.15) !important;
    color: white !important;
    border-radius: 7px !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: rgba(255,255,255,0.5) !important; }
/* Sidebar dropdown options text */
section[data-testid="stSidebar"] [data-baseweb="menu"] { background: #1A1060 !important; }
section[data-testid="stSidebar"] [role="option"] { color: white !important; }
/* Tags inside multiselect */
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background: var(--blue) !important;
    border: none !important;
    border-radius: 5px !important;
}
section[data-testid="stSidebar"] span[data-baseweb="tag"] span { color: white !important; font-size: 12px !important; }
section[data-testid="stSidebar"] span[data-baseweb="tag"] button svg { fill: rgba(255,255,255,0.7) !important; }
/* Slider */
section[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: var(--blue) !important;
}
/* Checkbox */
section[data-testid="stSidebar"] [data-testid="stCheckbox"] label span { color: rgba(255,255,255,0.85) !important; }
/* Toggle */
section[data-testid="stSidebar"] [data-testid="stToggle"] label span { color: rgba(255,255,255,0.85) !important; }

/* ── Sidebar layout ── */
.sb-inner { padding: 0 1.1rem 1.5rem; }
.sb-logo {
    padding: 1.1rem 1.1rem 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 0.2rem;
}
.sb-logo-title { font-size: 15px; font-weight: 600; color: white !important; letter-spacing: -0.01em; }
.sb-logo-sub { font-size: 11px; color: rgba(255,255,255,0.4) !important; margin-top: 1px; }

.sb-section {
    font-size: 9.5px; font-weight: 700; letter-spacing: 0.11em;
    text-transform: uppercase; color: rgba(255,255,255,0.35) !important;
    margin: 16px 0 5px; display: block;
}
.sb-divider { border: none; border-top: 1px solid rgba(255,255,255,0.07); margin: 12px 0; }

/* ── Header ── */
.hdr {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.3rem; padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.hdr-left { display: flex; align-items: baseline; gap: 10px; }
.hdr h1 { font-size: 1.15rem; font-weight: 600; color: var(--dark); margin: 0; letter-spacing: -0.02em; }
.hdr-sub { font-size: 12px; color: var(--muted); font-family: 'DM Mono', monospace !important; }
.hdr-badge {
    font-size: 10px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase;
    background: var(--mint); color: var(--dark); padding: 3px 9px; border-radius: 20px;
}

/* ── KPI cards ── */
.kpi-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 18px;
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 94px;
    transition: box-shadow 0.15s ease;
}
.kpi-card:hover { box-shadow: 0 2px 12px rgba(62,32,255,0.08); }
.kpi-lbl { font-size: 11px; color: var(--muted); font-weight: 500; margin-bottom: 6px; }
.kpi-val {
    font-size: 1.5rem; font-weight: 600; color: var(--dark);
    font-family: 'DM Mono', monospace !important; line-height: 1.05; letter-spacing: -0.02em;
}
.kpi-val-sm { font-size: 0.92rem; font-weight: 600; color: var(--dark); line-height: 1.4; }
.kpi-sub { font-size: 10.5px; color: var(--muted); margin-top: 5px; }
.kpi-accent { border-top: 2px solid var(--blue); }
.kpi-accent-mint { border-top: 2px solid var(--mint); }

/* ── Chart containers ── */
.chart-card {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 12px; padding: 16px; margin-top: 1.1rem;
    overflow: hidden;
}
.chart-title {
    font-size: 10px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 10px;
}

/* ── Section label ── */
.slabel {
    font-size: 9.5px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--muted); margin: 1.4rem 0 0.5rem; display: block;
}

/* ── Table ── */
.tbl-wrap {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}
/* Remove inner dataframe border */
.tbl-wrap iframe { border: none !important; }
.tbl-wrap [data-testid="stDataFrame"] > div > div { border: none !important; }

/* ── Score badge ── */
.score-badge {
    display: inline-flex; align-items: center; padding: 2px 8px;
    border-radius: 20px; font-size: 11px; font-weight: 600;
    font-family: 'DM Mono', monospace;
}
.sc-hi { background: var(--mint); color: #055c32; }
.sc-md { background: rgba(62,32,255,0.09); color: var(--blue); }
.sc-lo { background: var(--bg); color: var(--muted); }

/* ── Card ── */
.card {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 14px; padding: 24px; margin-top: 16px;
    border-left: 3px solid var(--blue);
    animation: fadeSlide .22s ease both;
}
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.card-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 6px; }
.card-title { font-size: 1.05rem; font-weight: 600; color: var(--dark); letter-spacing: -0.01em; }
.card-meta { font-family: 'DM Mono', monospace !important; font-size: 11px; color: var(--muted); margin-bottom: 12px; }
.card-desc {
    font-size: 13px; color: var(--dark); line-height: 1.6;
    padding: 10px 14px; background: var(--bg); border-radius: 8px; margin-bottom: 16px;
}
.c-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 16px; }
.c-m { background: var(--bg); border-radius: 9px; padding: 11px 13px; }
.c-lbl { font-size: 9.5px; color: var(--muted); font-weight: 700; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 4px; }
.c-val { font-size: 1.02rem; font-weight: 600; color: var(--dark); font-family: 'DM Mono', monospace !important; }
.c-sec { font-size: 9.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin: 13px 0 6px; }
.info-row { display: flex; gap: 8px; margin-bottom: 5px; align-items: baseline; }
.info-lbl { font-size: 12.5px; color: var(--muted); min-width: 162px; flex-shrink: 0; }
.info-val { font-size: 12.5px; color: var(--dark); font-weight: 500; }
.tags-row { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 2px; }
.tag { display: inline-block; padding: 3px 8px; border-radius: 5px; font-size: 11px; font-weight: 500; background: rgba(62,32,255,0.07); color: var(--dark); }
.tag-v { background: rgba(192,255,217,0.55); color: #065c30; }
.tag-b { background: rgba(114,91,255,0.10); color: #4030c0; }
.tag-cpm { background: transparent; color: var(--dark); border: 1px solid var(--border); }
.tag-cpc { background: rgba(62,32,255,0.10); color: var(--blue); }
.bool-y { color: var(--blue); font-weight: 700; font-size: 14px; }
.bool-n { color: rgba(7,0,55,0.18); }
.link-a { font-size: 12px; color: var(--blue); text-decoration: none; margin-right: 14px; font-weight: 500; transition: opacity .15s; }
.link-a:hover { opacity: .7; }
.card-links { margin-top: 6px; display: flex; flex-wrap: wrap; gap: 4px 0; }

/* ── Scoring weight total ── */
.w-wrap { display: inline-block; font-size: 12px; font-weight: 600; font-family: 'DM Mono', monospace !important; padding: 4px 12px; border-radius: 7px; margin: 6px 0 2px; }
.w-ok  { background: var(--mint); color: #055c32; }
.w-bad { background: rgba(62,32,255,0.1); color: var(--indigo); }

/* ── No results ── */
.no-res { text-align: center; padding: 48px 20px; color: var(--muted); background: var(--white); border: 1px solid var(--border); border-radius: 12px; }

/* ── Divider ── */
hr.light { border: none; border-top: 1px solid var(--border); margin: .9rem 0; }

/* ── Animation on KPI ── */
@keyframes fadeUp { from { opacity:0; transform:translateY(5px); } to { opacity:1; transform:translateY(0); } }
.kpi-card { animation: fadeUp .28s ease both; }
</style>
""", unsafe_allow_html=True)

# ─── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    def p(n): return os.path.join(base, n)
    def rc(a, b):
        for n in [a, b]:
            if os.path.exists(p(n)): return pd.read_csv(p(n))
        raise FileNotFoundError(f"Не найдено: {a} / {b}")
    df = rc("DataLens_-_formats.csv", "DataLens - formats.csv")
    di = rc("DataLens_-_dict_items.csv", "DataLens - dict_items.csv")
    fi = None
    for n in ["DataLens_-_format_items.csv", "DataLens - format_items.csv"]:
        if os.path.exists(p(n)): fi = pd.read_csv(p(n)); break
    if fi is None and os.path.exists(p("DataLens.xlsx")):
        fi = pd.read_excel(p("DataLens.xlsx"), sheet_name="format_items")
    if fi is None: raise FileNotFoundError("format_items не найден")
    merged = fi.merge(di[["dict_id","item_id","item_name"]], on=["dict_id","item_id"], how="left")
    pivot  = merged.groupby(["format_id","dict_id"])["item_name"].apply(list).unstack("dict_id").reset_index()
    return df.merge(pivot, on="format_id", how="left"), di

df, di = load_data()

# ─── UTILS ────────────────────────────────────────────────────────────────────
SEASON = {"Январь":0.80,"Февраль":1.00,"Март":1.20,"Апрель":1.20,"Май":1.00,
          "Июнь":1.00,"Июль":1.00,"Август":1.00,"Сентябрь":1.25,
          "Октябрь":1.25,"Ноябрь":1.25,"Декабрь":1.25}

def sk(platform, month):
    return SEASON.get(month, 1.0) if str(platform) == "Buzzoola" else 1.0

def pct(v):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)): return "—"
    except Exception: pass
    try:
        x = round(float(v) * 100, 1)
        return (f"{int(x)}%" if x == int(x) else f"{x:.1f}%").replace(".", ",")
    except Exception: return "—"

def rub(v):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)): return "—"
        return f"{int(round(float(v))):,} ₽".replace(",", "\u202f")
    except Exception: return "—"

def reach_s(v):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)): return "—"
        m = float(v) / 1e6
        if m >= 1:
            return (f"{int(m)}M" if m == int(m) else f"{m:.1f}M").replace(".", ",")
        return f"{int(v):,}".replace(",", "\u202f")
    except Exception: return "—"

def bv(v):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return '<span class="bool-n">—</span>'
    except Exception: pass
    return '<span class="bool-y">✓</span>' if str(v).upper() in ("TRUE","1") else '<span class="bool-n">—</span>'

def sv(v):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)): return "—"
    except Exception: pass
    s = str(v).strip()
    return s if s else "—"

def thtml(cell):
    if not isinstance(cell, list) or len(cell) == 0:
        return '<span style="color:rgba(7,0,55,.18);font-size:11px;">—</span>'
    return "".join(f'<span class="tag">{t}</span>' for t in cell if t)

def calc_ecpm(row):
    m = str(row.get("buy_model","CPM")).upper()
    ctr = row.get("ctr_avg", np.nan); d = float(row.get("discount",0) or 0)
    try:
        if m == "CPM": raw = float(row.get("cpm_avg", np.nan))
        elif m == "CPC":
            cpc, ct = float(row.get("cpc_avg",np.nan)), float(ctr)
            raw = cpc*ct*1000 if not (np.isnan(cpc) or np.isnan(ct) or ct==0) else np.nan
        elif m == "CPV":
            cpv, vt = float(row.get("cpv_avg",np.nan)), float(row.get("vtr_avg",np.nan))
            raw = cpv*vt*1000 if not (np.isnan(cpv) or np.isnan(vt) or vt==0) else np.nan
        else: raw = float(row.get("cpm_avg", np.nan))
    except Exception: raw = np.nan
    return np.nan if (raw is None or np.isnan(raw)) else raw*(1-d)

df["ecpm_eff"] = df.apply(calc_ecpm, axis=1)

def opts(did): return di[di["dict_id"]==did]["item_name"].dropna().tolist()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
def ss(t): st.markdown(f'<span class="sb-section">{t}</span>', unsafe_allow_html=True)
def sdiv(): st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-title">Format Selector</div>
        <div class="sb-logo-sub">Анализ рекламных форматов</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sb-inner">', unsafe_allow_html=True)

    ss("Тип формата")
    format_types = st.multiselect("Тип", ["Видео","Баннер"], default=["Видео","Баннер"],
                                   placeholder="Все типы", label_visibility="collapsed")
    ss("Устройство")
    devices = st.multiselect("Уст", ["Desktop","Mobile Web","In-App","Smart TV"],
                              default=["Desktop","Mobile Web","In-App","Smart TV"],
                              placeholder="Все устройства", label_visibility="collapsed")
    ss("Модель закупки")
    buy_models = st.multiselect("Мод", ["CPM","CPC"], default=["CPM","CPC"],
                                 placeholder="Все модели", label_visibility="collapsed")

    show_b = not format_types or "Баннер" in format_types
    show_v = not format_types or "Видео"  in format_types

    if show_b:
        ss("Баннер — отображение")
        f_disp = st.multiselect("Отобр", opts("display"), default=[],
                                 placeholder="Все варианты", label_visibility="collapsed")
    else: f_disp = []

    if show_v:
        ss("Видео — плейсмент")
        f_plac = st.multiselect("Плейс", opts("placement"), default=[],
                                 placeholder="Все плейсменты", label_visibility="collapsed")
        ss("Видео — позиция")
        f_inst = st.multiselect("Поз", opts("instream_pos"), default=[],
                                 placeholder="Все позиции", label_visibility="collapsed")
    else: f_plac = []; f_inst = []

    ss("Таргетинги")
    f_targ = st.multiselect("Тарг", opts("targeting"), default=[],
                              placeholder="Все таргетинги", label_visibility="collapsed")
    ss("DMP")
    f_dmp = st.multiselect("DMP", opts("dmp"), default=[],
                             placeholder="Все DMP", label_visibility="collapsed")

    sdiv()
    ss("Дополнительно")
    req_px = st.checkbox("Верификация пикселем")
    req_js = st.checkbox("Верификация JS-тегом")
    req_bl = st.checkbox("Brand Lift")
    req_sl = st.checkbox("Sales Lift")

    sdiv()
    ss("Пороговые значения")
    max_ecpm_f = st.slider("Макс. eCPM (после скидки), ₽", 0, 1000, 1000, step=10)
    min_ctr  = st.slider("Мин. CTR, %",        0.0,  5.0, 0.0, step=0.1)
    min_rch  = st.slider("Мин. охват, млн",    0.0, 80.0, 0.0, step=1.0)
    min_view = st.slider("Мин. Viewability, %", 0,   100,  0,   step=5)
    min_vtr  = st.slider("Мин. VTR, %",        0.0,100.0, 0.0, step=5.0)

    sdiv()
    scoring = st.toggle("Включить скоринг", value=False)
    if scoring:
        ss("Веса (сумма = 100)")
        wr = st.slider("Охват",               0,100,20,step=5)
        we = st.slider("eCPM (ниже — лучше)", 0,100,20,step=5)
        wc = st.slider("CTR",                 0,100,20,step=5)
        wv = st.slider("VTR",                 0,100,15,step=5)
        wi = st.slider("Viewability",         0,100,15,step=5)
        wm = st.slider("Комиссия (ниже — лучше)", 0,100,10,step=5)
        tw = wr+we+wc+wv+wi+wm
        st.markdown(f'<div class="w-wrap {"w-ok" if tw==100 else "w-bad"}">Сумма: {tw} / 100</div>',
                    unsafe_allow_html=True)
        norm = st.checkbox("Нормализовать веса", value=True)
    else:
        wr=we=wc=wv=wi=wm=tw=0; norm=False

    sdiv()
    ss("Сезонность")
    months = ["Январь","Февраль","Март","Апрель","Май","Июнь",
              "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
    sel_m = st.selectbox("Месяц", months, index=months.index("Март"),
                          label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

# ─── FILTER ───────────────────────────────────────────────────────────────────
def has(c, items): return isinstance(c, list) and any(i in c for i in items)
def all_in(c, items):
    if not items: return True
    return isinstance(c, list) and all(i in c for i in items)

F = df.copy()
if format_types: F = F[F["format_type"].apply(lambda x: has(x, format_types))]
if devices:      F = F[F["device"].apply(lambda x: has(x, devices))]
if buy_models:   F = F[F["buy_model"].isin(buy_models)]
if f_disp:  F = F[F["display"].apply(lambda x: all_in(x, f_disp))]
if f_plac:  F = F[F["placement"].apply(lambda x: all_in(x, f_plac))]
if f_inst:  F = F[F["instream_pos"].apply(lambda x: all_in(x, f_inst))]
if f_targ:  F = F[F["targeting"].apply(lambda x: all_in(x, f_targ))]
if f_dmp:   F = F[F["dmp"].apply(lambda x: all_in(x, f_dmp))]
if req_px:  F = F[F["verification_pixel"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
if req_js:  F = F[F["verification_js"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
if req_bl:  F = F[F["bls"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
if req_sl:  F = F[F["sales_lift"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
F = F[F["ecpm_eff"].fillna(9999) <= max_ecpm_f]
if min_ctr  > 0: F = F[F["ctr_avg"].fillna(0) >= min_ctr/100]
if min_rch  > 0: F = F[F["max_reach"].fillna(0) >= min_rch*1e6]
if min_view > 0: F = F[F["viewability_avg"].fillna(0) >= min_view/100]
if min_vtr  > 0: F = F[F["vtr_avg"].fillna(0) >= min_vtr/100]

F = F.copy()
F["sk_coef"] = F["platform"].apply(lambda p: sk(p, sel_m))
F["ecpm_s"]  = F["ecpm_eff"] * F["sk_coef"]

# ─── SCORING ──────────────────────────────────────────────────────────────────
def ncol(s, inv=False):
    mn, mx = s.min(), s.max()
    if mx == mn: return pd.Series([0.5]*len(s), index=s.index)
    n = (s-mn)/(mx-mn); return 1-n if inv else n

if scoring and len(F) > 0:
    W = dict(r=wr,e=we,c=wc,v=wv,i=wi,m=wm); t = sum(W.values())
    if norm and t > 0: W = {k:v/t for k,v in W.items()}
    else: W = {k:v/100 for k,v in W.items()}
    ev = F["ecpm_s"].max()*2 if F["ecpm_s"].notna().any() else 9999
    cv = F["commission"].max() if F["commission"].notna().any() else 1
    F["score"] = (
        ncol(F["max_reach"].fillna(0))             * W["r"] +
        ncol(F["ecpm_s"].fillna(ev), inv=True)     * W["e"] +
        ncol(F["ctr_avg"].fillna(0))               * W["c"] +
        ncol(F["vtr_avg"].fillna(0))               * W["v"] +
        ncol(F["viewability_avg"].fillna(0))       * W["i"] +
        ncol(F["commission"].fillna(cv), inv=True) * W["m"]
    ) * 100
    F = F.sort_values("score", ascending=False).reset_index(drop=True)
else:
    F["score"] = np.nan
    F = F.sort_values("ecpm_s", ascending=True, na_position="last").reset_index(drop=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
n_platforms = df["platform"].nunique()
badge_text = f"{n_platforms} {'площадка' if n_platforms==1 else 'площадки' if n_platforms<5 else 'площадок'}"

st.markdown(f"""
<div class="hdr">
    <div class="hdr-left">
        <h1 class="hdr">Format Selector</h1>
        <span class="hdr-sub">Анализ рекламных форматов</span>
    </div>
    <span class="hdr-badge">{badge_text} · бета</span>
</div>
""", unsafe_allow_html=True)

# ─── KPI ──────────────────────────────────────────────────────────────────────
top   = F.iloc[0] if len(F) > 0 else None
avg_e = F["ecpm_s"].mean() if len(F) > 0 else np.nan
sk0   = float(F["sk_coef"].iloc[0]) if len(F) > 0 else 1.0
maxr  = F["max_reach"].max() if len(F) > 0 else np.nan

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="kpi-card kpi-accent">
        <div><div class="kpi-lbl">Форматов после фильтров</div>
        <div class="kpi-val">{len(F)}</div></div>
        <div class="kpi-sub">из {len(df)} доступных</div>
    </div>""", unsafe_allow_html=True)
with c2:
    lbl2 = "Лучший по скорингу" if scoring else "Самый дешевый eCPM"
    if top is not None:
        sub2 = f'Скор: {top["score"]:.0f}' if (scoring and not pd.isna(top.get("score",np.nan))) else top.get("buy_model","—")
        val2 = top.get("format_name","—")
        st.markdown(f"""<div class="kpi-card kpi-accent">
            <div><div class="kpi-lbl">{lbl2}</div>
            <div class="kpi-val-sm">{val2}</div></div>
            <div class="kpi-sub">{sub2}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="kpi-card kpi-accent"><div><div class="kpi-lbl">{lbl2}</div><div class="kpi-val">—</div></div><div class="kpi-sub">&nbsp;</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card kpi-accent">
        <div><div class="kpi-lbl">Средний eCPM (с сезонностью)</div>
        <div class="kpi-val">{rub(avg_e)}</div></div>
        <div class="kpi-sub">{sel_m} · коэф. {sk0}×</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card kpi-accent-mint">
        <div><div class="kpi-lbl">Макс. охват</div>
        <div class="kpi-val">{reach_s(maxr)}</div></div>
        <div class="kpi-sub">среди отфильтрованных</div>
    </div>""", unsafe_allow_html=True)

# ─── CHARTS ───────────────────────────────────────────────────────────────────
if len(F) > 0:
    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)

    # ── Chart 1: eCPM bar ──
    with ch1:
        cdf = F[F["ecpm_s"].notna()].sort_values("ecpm_s")
        if len(cdf) > 0:
            if scoring and cdf["score"].notna().any():
                mn_, mx_ = cdf["score"].min(), cdf["score"].max()
                cols = [f"rgba(62,32,255,{0.28+0.72*(s-mn_)/max(mx_-mn_,1):.2f})"
                        for s in cdf["score"].fillna(mn_)]
            else:
                # Gradient from indigo to blue based on position
                cols = [f"rgba(62,32,255,{0.35+0.65*i/max(len(cdf)-1,1):.2f})"
                        for i in range(len(cdf))]

            fig1 = go.Figure(go.Bar(
                x=cdf["ecpm_s"].round(0), y=cdf["format_name"],
                orientation="h", marker_color=cols, marker_line_width=0,
                hovertemplate="<b>%{y}</b><br>eCPM: %{x:.0f} ₽<extra></extra>"
            ))
            fig1.update_layout(
                title=None,
                height=max(240, len(cdf)*28+40),
                margin=dict(l=0, r=14, t=8, b=8),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(gridcolor="rgba(7,0,55,0.06)", tickfont_size=10,
                           title=None, tickfont_color="rgba(7,0,55,0.4)",
                           zeroline=False),
                yaxis=dict(tickfont_size=11, title=None, tickfont_color="#070037",
                           tickmode="linear"),
                font_family="DM Sans", bargap=0.3,
            )
            st.markdown('<div class="chart-card"><div class="chart-title">eCPM по форматам (₽, с учетом сезонности)</div>', unsafe_allow_html=True)
            st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Chart 2: CTR vs Viewability scatter ──
    with ch2:
        sdf = F[F["ctr_avg"].notna() & F["viewability_avg"].notna()].copy()
        if len(sdf) >= 2:
            med = sdf["max_reach"].median()
            sdf["bsz"] = sdf["max_reach"].fillna(med).apply(lambda v: max(9,min(34,float(v)/2.2e6)))
            if scoring and sdf["score"].notna().any():
                mn2, mx2 = sdf["score"].min(), sdf["score"].max()
                scols = [f"rgba(62,32,255,{0.3+0.7*(s-mn2)/max(mx2-mn2,1):.2f})"
                         for s in sdf["score"].fillna(mn2)]
            else:
                scols = ["#725BFF"] * len(sdf)

            fig2 = go.Figure()
            for i, (_, r) in enumerate(sdf.iterrows()):
                fig2.add_trace(go.Scatter(
                    x=[float(r["ctr_avg"])*100], y=[float(r["viewability_avg"])*100],
                    mode="markers+text",
                    marker=dict(size=r["bsz"], color=scols[i],
                                line=dict(color="white", width=1.5)),
                    text=[r["format_name"]], textposition="top center",
                    textfont=dict(size=8, color="#070037"),
                    hovertemplate=(f"<b>{r['format_name']}</b><br>"
                                   f"CTR: {float(r['ctr_avg'])*100:.2f}%<br>"
                                   f"Viewability: {float(r['viewability_avg'])*100:.0f}%<extra></extra>"),
                    showlegend=False
                ))
            fig2.update_layout(
                title=None,
                height=max(240, len(sdf)*28+40),
                margin=dict(l=0,r=14,t=8,b=8),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(title="CTR, %", gridcolor="rgba(7,0,55,0.06)",
                           tickfont_size=10, title_font_size=10,
                           tickfont_color="rgba(7,0,55,0.4)",
                           title_font_color="rgba(7,0,55,0.4)", zeroline=False),
                yaxis=dict(title="Viewability, %", gridcolor="rgba(7,0,55,0.06)",
                           tickfont_size=10, title_font_size=10,
                           tickfont_color="rgba(7,0,55,0.4)",
                           title_font_color="rgba(7,0,55,0.4)", zeroline=False),
                font_family="DM Sans",
            )
            st.markdown('<div class="chart-card"><div class="chart-title">CTR vs Viewability (размер — охват)</div>', unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

# ─── TABLE ────────────────────────────────────────────────────────────────────
st.markdown('<span class="slabel">Форматы</span>', unsafe_allow_html=True)

if len(F) == 0:
    st.markdown('<div class="no-res">Нет форматов, соответствующих выбранным фильтрам.</div>',
                unsafe_allow_html=True)
else:
    def _list(c): return ", ".join(c) if isinstance(c, list) else ""
    def _score(s):
        try:
            return "" if pd.isna(s) else f"{s:.0f}"
        except Exception: return ""

    disp = pd.DataFrame({
        "Формат":     F["format_name"],
        "ID":         F["format_id"],
        "Тип":        F["format_type"].apply(_list),
        "Модель":     F["buy_model"],
        "Устройства": F["device"].apply(_list),
        "Охват":      F["max_reach"].apply(reach_s),
        "CTR":        F["ctr_avg"].apply(pct),
        "Viewability":F["viewability_avg"].apply(pct),
        "eCPM (сез.)":F["ecpm_s"].apply(rub),
    })
    if scoring: disp["Скор"] = F["score"].apply(_score)

    event = st.dataframe(
        disp,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "Формат":      st.column_config.TextColumn(width="large"),
            "ID":          st.column_config.TextColumn(width="small"),
            "Тип":         st.column_config.TextColumn(width="small"),
            "Модель":      st.column_config.TextColumn(width="small"),
            "Устройства":  st.column_config.TextColumn(width="medium"),
            "Охват":       st.column_config.TextColumn(width="small"),
            "CTR":         st.column_config.TextColumn(width="small"),
            "Viewability": st.column_config.TextColumn(width="small"),
            "eCPM (сез.)": st.column_config.TextColumn(width="small"),
            **({"Скор": st.column_config.TextColumn(width="small")} if scoring else {}),
        },
        height=min(600, (len(F)+1)*38+2),
    )

    # ─── FORMAT CARD ──────────────────────────────────────────────────────────
    sel = (event.selection.rows if hasattr(event, "selection") else []) or []

    if sel:
        idx = sel[0]
        r   = F.iloc[idx]

        # Safe field access — always use .get() with default
        def gf(field, default=np.nan):
            val = r.get(field, default)
            if val is None: return default
            try:
                if isinstance(val, float) and np.isnan(val): return default
            except Exception: pass
            return val

        ee  = gf("ecpm_eff")
        es2 = gf("ecpm_s")
        sc  = gf("sk_coef", 1.0)

        # Score display
        score_val = gf("score", np.nan)
        score_html = ""
        if scoring and not (isinstance(score_val, float) and np.isnan(score_val)):
            s = float(score_val)
            cls = "sc-hi" if s>=65 else ("sc-md" if s>=40 else "sc-lo")
            score_html = f'<span class="score-badge {cls}" style="margin-left:8px;">{s:.0f}</span>'

        links = []
        for lbl_, key in [("Пример","example_url"),("Техтребования","technical_requirements_url"),
                           ("Медиакит","mediakit_url"),("Кейсы","cases_url")]:
            v = gf(key, "")
            if isinstance(v, str) and v.startswith("http"):
                links.append(f'<a class="link-a" href="{v}" target="_blank">{lbl_} ↗</a>')

        st.markdown(f"""
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">{sv(gf('format_name','—'))}{score_html}</div>
                    <div class="card-meta">{sv(gf('format_id','—'))} · {sv(gf('buy_model','—'))} · {sv(gf('platform','—'))}</div>
                </div>
                {'<div class="card-links">'+("".join(links))+"</div>" if links else ""}
            </div>
            <div class="card-desc">{sv(gf('description','Описание не указано'))}</div>

            <div class="c-grid">
                <div class="c-m"><div class="c-lbl">eCPM (факт)</div><div class="c-val">{rub(ee)}</div></div>
                <div class="c-m"><div class="c-lbl">eCPM (сезон. {sc}×)</div><div class="c-val">{rub(es2)}</div></div>
                <div class="c-m"><div class="c-lbl">Скидка</div><div class="c-val">{pct(gf('discount'))}</div></div>
                <div class="c-m"><div class="c-lbl">Охват (макс.)</div><div class="c-val">{reach_s(gf('max_reach'))}</div></div>
                <div class="c-m"><div class="c-lbl">CTR (среднее)</div><div class="c-val">{pct(gf('ctr_avg'))}</div></div>
                <div class="c-m"><div class="c-lbl">VTR (среднее)</div><div class="c-val">{pct(gf('vtr_avg'))}</div></div>
                <div class="c-m"><div class="c-lbl">Viewability (среднее)</div><div class="c-val">{pct(gf('viewability_avg'))}</div></div>
                <div class="c-m"><div class="c-lbl">Комиссия</div><div class="c-val">{pct(gf('commission'))}</div></div>
                <div class="c-m"><div class="c-lbl">Мин. бюджет</div><div class="c-val">{rub(gf('min_budget'))}</div></div>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">
            <div>
                <div class="c-sec">Ценовой диапазон</div>
                <div class="info-row"><span class="info-lbl">CPM мин / сред / макс</span>
                    <span class="info-val">{rub(gf('cpm_min'))} / {rub(gf('cpm_avg'))} / {rub(gf('cpm_max'))}</span></div>
                <div class="info-row"><span class="info-lbl">CPC мин / сред / макс</span>
                    <span class="info-val">{rub(gf('cpc_min'))} / {rub(gf('cpc_avg'))} / {rub(gf('cpc_max'))}</span></div>
                <div class="info-row"><span class="info-lbl">CTR мин / макс</span>
                    <span class="info-val">{pct(gf('ctr_min'))} / {pct(gf('ctr_max'))}</span></div>
                <div class="c-sec">Верификация</div>
                <div class="info-row"><span class="info-lbl">Пиксель</span><span class="info-val">{bv(gf('verification_pixel'))}</span></div>
                <div class="info-row"><span class="info-lbl">JS-тег</span><span class="info-val">{bv(gf('verification_js'))}</span></div>
                <div class="info-row"><span class="info-lbl">Условия</span>
                    <span class="info-val" style="font-size:12px;color:var(--muted);">{sv(gf('verification_terms','—'))}</span></div>
                <div class="c-sec">Исследования</div>
                <div class="info-row"><span class="info-lbl">Brand Lift</span><span class="info-val">{bv(gf('bls'))}</span></div>
                <div class="info-row"><span class="info-lbl">Sales Lift</span><span class="info-val">{bv(gf('sales_lift'))}</span></div>
            </div>
            <div>
                <div class="c-sec">Плейсмент</div>
                <div class="tags-row">{thtml(gf('placement', []))}</div>
                <div class="c-sec">Устройства</div>
                <div class="tags-row">{thtml(gf('device', []))}</div>
                <div class="c-sec">Отображение</div>
                <div class="tags-row">{thtml(gf('display', []))}</div>
                <div class="c-sec">DMP</div>
                <div class="tags-row">{thtml(gf('dmp', []))}</div>
                <div class="c-sec">Производство</div>
                <div class="tags-row">{thtml(gf('production', []))}</div>
            </div>
            </div>

            <div class="c-sec">Таргетинг</div>
            <div class="tags-row">{thtml(gf('targeting', []))}</div>

            <div class="c-sec">Наценки за таргетинг</div>
            <div class="tags-row">{thtml(gf('targeting_markup', []))}</div>
        </div>
        """, unsafe_allow_html=True)

        # Expandable terms — only if text present
        for lbl_, key in [("Условия Brand Lift","bls_terms"),
                           ("Условия Sales Lift","sales_lift_terms"),
                           ("Условия сезонности","seasonality_terms")]:
            v = gf(key, "")
            if isinstance(v, str) and v.strip():
                with st.expander(f"📋 {lbl_}"):
                    st.markdown(f'<p style="font-size:13px;line-height:1.65;color:var(--dark);">{v}</p>',
                                unsafe_allow_html=True)
