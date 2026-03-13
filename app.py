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

# ─── STYLES ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --white:   #FFFFFF;
    --mint:    #C0FFD9;
    --blue:    #3E20FF;
    --indigo:  #725BFF;
    --bg:      #F8F2FF;
    --dark:    #070037;
    --muted:   rgba(7,0,55,0.42);
    --border:  rgba(7,0,55,0.10);
    --row-h:   rgba(62,32,255,0.045);
    --tag-bg:  rgba(62,32,255,0.08);
}

*, *::before, *::after { font-family: 'DM Sans', sans-serif !important; box-sizing: border-box; }
html, body, .main { background: var(--bg) !important; }
.main .block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1460px; }
[class*="css"] { color: var(--dark); }

/* ── Sidebar dark ── */
section[data-testid="stSidebar"] { background: var(--dark) !important; border-right: none !important; }
section[data-testid="stSidebar"] .block-container { padding-top: 0 !important; }
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* All sidebar text white */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div { color: rgba(255,255,255,0.82) !important; font-size: 13px !important; }

/* Sidebar selects */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.07) !important;
    border-color: rgba(255,255,255,0.13) !important;
    border-radius: 7px !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: rgba(255,255,255,0.45) !important; }
section[data-testid="stSidebar"] [data-baseweb="select"] span { color: rgba(255,255,255,0.82) !important; }

/* Tags in multiselect */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: var(--blue) !important; border: none !important; border-radius: 5px !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] span { color: white !important; font-size: 12px !important; }
section[data-testid="stSidebar"] [data-baseweb="tag"] button svg { fill: rgba(255,255,255,0.65) !important; }

/* Slider track fill */
section[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] { background: var(--blue) !important; }

/* Placeholder text */
section[data-testid="stSidebar"] [data-baseweb="select"] [data-placeholder] { color: rgba(255,255,255,0.38) !important; }

/* sb-label */
.sb-label {
    font-size: 9.5px !important; font-weight: 700 !important; letter-spacing: 0.11em;
    text-transform: uppercase; color: rgba(255,255,255,0.35) !important;
    margin: 14px 0 4px; display: block;
}
.sb-logo {
    padding: 1rem 1.1rem 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 4px;
}
.sb-logo-t { font-size: 14px !important; font-weight: 600 !important; color: white !important; }
.sb-logo-s { font-size: 11px !important; color: rgba(255,255,255,0.38) !important; margin-top: 1px; }
.sb-inner  { padding: 0 1rem 1.5rem; }
hr.sb-div  { border: none; border-top: 1px solid rgba(255,255,255,0.07); margin: 10px 0; }

/* ── Page header ── */
.hdr {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.25rem; padding-bottom: 0.95rem; border-bottom: 1px solid var(--border);
}
.hdr-l { display: flex; align-items: baseline; gap: 10px; }
.hdr-t { font-size: 1.12rem; font-weight: 600; color: var(--dark); margin: 0; letter-spacing: -.02em; }
.hdr-s { font-size: 12px; color: var(--muted); font-family: 'DM Mono', monospace !important; }
.hdr-badge {
    font-size: 9.5px; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase;
    background: var(--mint); color: var(--dark); padding: 3px 9px; border-radius: 20px;
}

/* ── KPI — EQUAL HEIGHT via inline-flex rows ── */
.kpi-row { display: flex; gap: 10px; margin-bottom: 1.25rem; align-items: stretch; }
.kpi-card {
    flex: 1;
    background: var(--white); border: 1px solid var(--border); border-radius: 11px;
    padding: 15px 17px; min-height: 92px;
    display: flex; flex-direction: column; justify-content: space-between;
    border-top: 2px solid var(--blue);
    animation: fadeUp .28s ease both;
}
.kpi-card.mint { border-top-color: var(--mint); }
.kpi-lbl  { font-size: 11px; color: var(--muted); font-weight: 500; margin-bottom: 5px; }
.kpi-val  { font-size: 1.42rem; font-weight: 600; color: var(--dark); font-family: 'DM Mono', monospace !important; line-height: 1.05; letter-spacing: -.02em; }
.kpi-vsm  { font-size: 0.9rem; font-weight: 600; color: var(--dark); line-height: 1.35; }
.kpi-sub  { font-size: 10.5px; color: var(--muted); margin-top: 4px; }

/* ── Section label ── */
.slabel {
    font-size: 9.5px; font-weight: 700; letter-spacing: 0.10em; text-transform: uppercase;
    color: var(--muted); margin: 1.3rem 0 0.55rem; display: block;
}

/* ── Custom HTML table ── */
.fmt-tbl-wrap {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 11px; overflow: hidden; margin-top: 6px;
}
.fmt-tbl { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.fmt-tbl th {
    text-align: left; padding: 9px 14px;
    background: var(--bg); border-bottom: 1px solid var(--border);
    font-size: 9.5px; font-weight: 700; letter-spacing: 0.09em;
    text-transform: uppercase; color: var(--muted); white-space: nowrap;
}
.fmt-tbl td { padding: 10px 14px; border-bottom: 1px solid rgba(7,0,55,0.055); vertical-align: middle; }
.fmt-tbl tr:last-child td { border-bottom: none; }
.fmt-tbl tbody tr { cursor: pointer; transition: background 0.1s ease; }
.fmt-tbl tbody tr:hover td { background: var(--row-h); }
.fmt-tbl tbody tr.sel td   { background: rgba(62,32,255,0.08); }

.f-name { font-weight: 500; color: var(--dark); font-size: 13px; }
.f-id   { font-family: 'DM Mono', monospace; font-size: 10.5px; color: var(--muted); margin-top: 1px; }

/* Tags */
.tag     { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 500; margin: 1px 2px 1px 0; background: var(--tag-bg); color: var(--dark); }
.tag-v   { background: rgba(192,255,217,0.6); color: #055c30; }
.tag-b   { background: rgba(114,91,255,0.10); color: #4433bb; }
.tag-cpm { background: transparent; color: var(--dark); border: 1px solid var(--border); }
.tag-cpc { background: rgba(62,32,255,0.10); color: var(--blue); }

/* Metric bar */
.mbar-wrap { display: flex; align-items: center; gap: 6px; }
.mbar-bg   { height: 4px; background: rgba(7,0,55,0.08); border-radius: 3px; flex: 1; min-width: 48px; }
.mbar-fill { height: 4px; border-radius: 3px; background: var(--blue); }
.mbar-val  { font-family: 'DM Mono', monospace; font-size: 11.5px; color: var(--dark); min-width: 42px; text-align: right; white-space: nowrap; }

/* Score badge */
.sc-pill { display: inline-flex; align-items: center; padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 600; font-family: 'DM Mono', monospace !important; }
.sc-hi { background: var(--mint); color: #055c30; }
.sc-md { background: rgba(62,32,255,0.09); color: var(--blue); }
.sc-lo { background: var(--bg); color: var(--muted); }

/* ── Card ── */
.card {
    background: var(--white); border: 1px solid var(--border);
    border-left: 3px solid var(--blue);
    border-radius: 12px; padding: 22px; margin-top: 14px;
    animation: fadeSlide .22s ease both;
}
@keyframes fadeSlide { from{opacity:0;transform:translateY(7px)} to{opacity:1;transform:translateY(0)} }
.card-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 4px; }
.card-title { font-size: 1.02rem; font-weight: 600; color: var(--dark); letter-spacing: -.01em; }
.card-meta  { font-family: 'DM Mono', monospace !important; font-size: 11px; color: var(--muted); margin-bottom: 11px; }
.card-desc  { font-size: 13px; color: var(--dark); line-height: 1.62; padding: 10px 14px; background: var(--bg); border-radius: 8px; margin-bottom: 15px; }
.c-grid     { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin-bottom: 15px; }
.c-m        { background: var(--bg); border-radius: 8px; padding: 11px 13px; }
.c-lbl      { font-size: 9.5px; color: var(--muted); font-weight: 700; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 4px; }
.c-val      { font-size: 1rem; font-weight: 600; color: var(--dark); font-family: 'DM Mono', monospace !important; }
.c-sec      { font-size: 9.5px; font-weight: 700; letter-spacing: .10em; text-transform: uppercase; color: var(--muted); margin: 13px 0 5px; }
.info-row   { display: flex; gap: 8px; margin-bottom: 5px; }
.info-lbl   { font-size: 12.5px; color: var(--muted); min-width: 162px; flex-shrink: 0; }
.info-val   { font-size: 12.5px; color: var(--dark); font-weight: 500; }
.tags-row   { display: flex; flex-wrap: wrap; gap: 4px; }
.bool-y     { color: var(--blue); font-weight: 700; }
.bool-n     { color: rgba(7,0,55,0.18); }
.link-a     { font-size: 12px; color: var(--blue); text-decoration: none; margin-right: 14px; font-weight: 500; }

/* Weight total */
.w-wrap { display: inline-block; font-size: 12px; font-weight: 600; font-family: 'DM Mono', monospace !important; padding: 4px 11px; border-radius: 7px; margin: 5px 0 2px; }
.w-ok   { background: var(--mint); color: #055c30; }
.w-bad  { background: rgba(62,32,255,0.09); color: var(--indigo); }

hr.light { border: none; border-top: 1px solid var(--border); margin: .9rem 0; }
.no-res  { text-align: center; padding: 48px 20px; color: var(--muted); background: var(--white); border: 1px solid var(--border); border-radius: 11px; font-size: 13px; }
.empty-card { margin-top: 14px; padding: 20px; background: var(--white); border: 1px solid var(--border); border-radius: 11px; color: var(--muted); font-size: 13px; }

@keyframes fadeUp { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)} }
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

# ─── HELPERS ──────────────────────────────────────────────────────────────────
SEASON = {"Январь":0.80,"Февраль":1.00,"Март":1.20,"Апрель":1.20,"Май":1.00,
          "Июнь":1.00,"Июль":1.00,"Август":1.00,"Сентябрь":1.25,
          "Октябрь":1.25,"Ноябрь":1.25,"Декабрь":1.25}

def season_k(platform, month):
    return SEASON.get(month, 1.0) if str(platform) == "Buzzoola" else 1.0

def pct(v):
    try:
        f = float(v)
        if np.isnan(f): return "—"
        x = round(f * 100, 1)
        return (f"{int(x)}%" if x == int(x) else f"{x:.1f}%").replace(".", ",")
    except Exception: return "—"

def rub(v):
    try:
        f = float(v)
        if np.isnan(f): return "—"
        return f"{int(round(f)):,} ₽".replace(",", "\u202f")
    except Exception: return "—"

def reach_s(v):
    try:
        f = float(v)
        if np.isnan(f): return "—"
        m = f / 1e6
        if m >= 1:
            return (f"{int(m)}M" if m == int(m) else f"{m:.1f}M").replace(".", ",")
        return f"{int(f):,}".replace(",", "\u202f")
    except Exception: return "—"

def bv(v):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return '<span class="bool-n">—</span>'
    except Exception: pass
    return '<span class="bool-y">✓</span>' if str(v).upper() in ("TRUE","1") else '<span class="bool-n">—</span>'

def sv(v, default="—"):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)): return default
    except Exception: pass
    s = str(v).strip(); return s if s else default

def thtml(cell):
    if not isinstance(cell, list) or not cell:
        return '<span style="color:rgba(7,0,55,.16);font-size:11px;">—</span>'
    return "".join(f'<span class="tag">{t}</span>' for t in cell if t)

def mbar(val, max_val, disp):
    if disp == "—":
        return '<span style="color:rgba(7,0,55,.18);font-size:11px;">—</span>'
    try:
        pct_w = min(float(val) / float(max_val) * 100, 100) if max_val else 0
    except Exception: pct_w = 0
    return (f'<div class="mbar-wrap">'
            f'<div class="mbar-bg"><div class="mbar-fill" style="width:{pct_w:.1f}%"></div></div>'
            f'<span class="mbar-val">{disp}</span></div>')

def calc_ecpm(row):
    m = str(row.get("buy_model","CPM")).upper()
    d = float(row.get("discount", 0) or 0)
    try:
        if m == "CPM": raw = float(row.get("cpm_avg", np.nan))
        elif m == "CPC":
            cpc, ct = float(row.get("cpc_avg",np.nan)), float(row.get("ctr_avg",np.nan))
            raw = cpc*ct*1000 if not (np.isnan(cpc) or np.isnan(ct) or ct==0) else np.nan
        elif m == "CPV":
            cpv, vt = float(row.get("cpv_avg",np.nan)), float(row.get("vtr_avg",np.nan))
            raw = cpv*vt*1000 if not (np.isnan(cpv) or np.isnan(vt) or vt==0) else np.nan
        else: raw = float(row.get("cpm_avg", np.nan))
        return np.nan if np.isnan(raw) else raw*(1-d)
    except Exception: return np.nan

df["ecpm_eff"] = df.apply(calc_ecpm, axis=1)

def opts(did): return di[di["dict_id"]==did]["item_name"].dropna().tolist()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
def ss(t): st.markdown(f'<span class="sb-label">{t}</span>', unsafe_allow_html=True)
def sd():  st.markdown('<hr class="sb-div">', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""<div class="sb-logo">
        <div class="sb-logo-t">Format Selector</div>
        <div class="sb-logo-s">Анализ рекламных форматов</div>
    </div><div class="sb-inner">""", unsafe_allow_html=True)

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
    sd()
    ss("Дополнительно")
    req_px = st.checkbox("Верификация пикселем")
    req_js = st.checkbox("Верификация JS-тегом")
    req_bl = st.checkbox("Brand Lift")
    req_sl = st.checkbox("Sales Lift")
    sd()
    ss("Пороговые значения")
    max_ecpm_f = st.slider("Макс. eCPM (после скидки), ₽", 0, 1000, 1000, step=10)
    min_ctr  = st.slider("Мин. CTR, %",        0.0,  5.0, 0.0, step=0.1)
    min_rch  = st.slider("Мин. охват, млн",    0.0, 80.0, 0.0, step=1.0)
    min_view = st.slider("Мин. Viewability, %", 0,   100,  0,   step=5)
    min_vtr  = st.slider("Мин. VTR, %",        0.0,100.0, 0.0, step=5.0)
    sd()
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
    sd()
    ss("Сезонность")
    months = ["Январь","Февраль","Март","Апрель","Май","Июнь",
              "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
    sel_m = st.selectbox("Месяц", months, index=months.index("Март"), label_visibility="collapsed")

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
F["sk"] = F["platform"].apply(lambda p: season_k(p, sel_m))
F["ecpm_s"] = F["ecpm_eff"] * F["sk"]

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
n_plat = df["platform"].nunique()
badge  = f"{n_plat} {'площадка' if n_plat==1 else ('площадки' if n_plat<5 else 'площадок')} · бета"
st.markdown(f"""<div class="hdr">
    <div class="hdr-l">
        <h1 class="hdr-t">Format Selector</h1>
        <span class="hdr-s">Анализ рекламных форматов</span>
    </div>
    <span class="hdr-badge">{badge}</span>
</div>""", unsafe_allow_html=True)

# ─── KPI ──────────────────────────────────────────────────────────────────────
top   = F.iloc[0] if len(F) > 0 else None
avg_e = F["ecpm_s"].mean() if len(F) > 0 else np.nan
sk0   = float(F["sk"].iloc[0]) if len(F) > 0 else 1.0
maxr  = F["max_reach"].max() if len(F) > 0 else np.nan

# Use HTML for all 4 cards in one flex row — guarantees equal height
lbl2 = "Лучший по скорингу" if scoring else "Самый дешевый eCPM"
if top is not None:
    sub2 = f'Скор: {top["score"]:.0f}' if (scoring and not pd.isna(top.get("score",np.nan))) else sv(top.get("buy_model","—"))
    val2_html = f'<div class="kpi-vsm">{sv(top.get("format_name","—"))}</div>'
else:
    sub2 = ""; val2_html = '<div class="kpi-val">—</div>'

st.markdown(f"""<div class="kpi-row">
    <div class="kpi-card">
        <div><div class="kpi-lbl">Форматов после фильтров</div>
        <div class="kpi-val">{len(F)}</div></div>
        <div class="kpi-sub">из {len(df)} доступных</div>
    </div>
    <div class="kpi-card">
        <div><div class="kpi-lbl">{lbl2}</div>{val2_html}</div>
        <div class="kpi-sub">{sub2}</div>
    </div>
    <div class="kpi-card">
        <div><div class="kpi-lbl">Средний eCPM (с сезонностью)</div>
        <div class="kpi-val">{rub(avg_e)}</div></div>
        <div class="kpi-sub">{sel_m} · коэф. {sk0}×</div>
    </div>
    <div class="kpi-card mint">
        <div><div class="kpi-lbl">Макс. охват</div>
        <div class="kpi-val">{reach_s(maxr)}</div></div>
        <div class="kpi-sub">среди отфильтрованных</div>
    </div>
</div>""", unsafe_allow_html=True)

# ─── CHARTS ───────────────────────────────────────────────────────────────────
if len(F) > 0:
    ch1, ch2 = st.columns(2)

    with ch1:
        cdf = F[F["ecpm_s"].notna()].sort_values("ecpm_s")
        if len(cdf) > 0:
            if scoring and cdf["score"].notna().any():
                mn_, mx_ = cdf["score"].min(), cdf["score"].max()
                cols = [f"rgba(62,32,255,{0.28+0.72*(s-mn_)/max(mx_-mn_,1):.2f})"
                        for s in cdf["score"].fillna(mn_)]
            else:
                n = len(cdf)
                cols = [f"rgba(62,32,255,{0.32+0.68*i/max(n-1,1):.2f})" for i in range(n)]

            fig1 = go.Figure(go.Bar(
                x=cdf["ecpm_s"].round(0), y=cdf["format_name"],
                orientation="h", marker_color=cols, marker_line_width=0,
                hovertemplate="<b>%{y}</b><br>eCPM: %{x:.0f} ₽<extra></extra>"
            ))
            fig1.update_layout(
                title=dict(text="eCPM по форматам (₽, с сезонностью)",
                           font_size=11, font_color="rgba(7,0,55,0.42)", font_family="DM Sans"),
                height=max(260, len(cdf)*29+44),
                margin=dict(l=0, r=12, t=36, b=4),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(gridcolor="rgba(7,0,55,0.06)", tickfont_size=10,
                           title=None, tickfont_color="rgba(7,0,55,0.4)", zeroline=False),
                yaxis=dict(tickfont_size=11, title=None, tickfont_color="#070037", tickmode="linear"),
                font_family="DM Sans", bargap=0.32,
            )
            st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    with ch2:
        sdf = F[F["ctr_avg"].notna() & F["viewability_avg"].notna()].copy()
        if len(sdf) >= 2:
            med = float(sdf["max_reach"].median()) if sdf["max_reach"].notna().any() else 1e6
            sdf["bsz"] = sdf["max_reach"].fillna(med).apply(lambda v: max(9, min(34, float(v)/2.2e6)))
            if scoring and sdf["score"].notna().any():
                mn2, mx2 = sdf["score"].min(), sdf["score"].max()
                scols = [f"rgba(62,32,255,{0.28+0.72*(s-mn2)/max(mx2-mn2,1):.2f})"
                         for s in sdf["score"].fillna(mn2)]
            else:
                scols = ["#725BFF"] * len(sdf)

            fig2 = go.Figure()
            for i, (_, r) in enumerate(sdf.iterrows()):
                fig2.add_trace(go.Scatter(
                    x=[float(r["ctr_avg"])*100], y=[float(r["viewability_avg"])*100],
                    mode="markers+text",
                    marker=dict(size=r["bsz"], color=scols[i], line=dict(color="white", width=1.5)),
                    text=[r["format_name"]], textposition="top center",
                    textfont=dict(size=8, color="#070037"),
                    hovertemplate=(f"<b>{r['format_name']}</b><br>"
                                   f"CTR: {float(r['ctr_avg'])*100:.2f}%<br>"
                                   f"Viewability: {float(r['viewability_avg'])*100:.0f}%<extra></extra>"),
                    showlegend=False
                ))
            fig2.update_layout(
                title=dict(text="CTR vs Viewability (размер — охват)",
                           font_size=11, font_color="rgba(7,0,55,0.42)", font_family="DM Sans"),
                height=max(260, len(sdf)*29+44),
                margin=dict(l=0, r=12, t=36, b=4),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(title="CTR, %", gridcolor="rgba(7,0,55,0.06)", tickfont_size=10,
                           title_font_size=10, tickfont_color="rgba(7,0,55,0.4)",
                           title_font_color="rgba(7,0,55,0.4)", zeroline=False),
                yaxis=dict(title="Viewability, %", gridcolor="rgba(7,0,55,0.06)", tickfont_size=10,
                           title_font_size=10, tickfont_color="rgba(7,0,55,0.4)",
                           title_font_color="rgba(7,0,55,0.4)", zeroline=False),
                font_family="DM Sans",
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ─── TABLE ────────────────────────────────────────────────────────────────────
st.markdown('<span class="slabel">Форматы</span>', unsafe_allow_html=True)

if len(F) == 0:
    st.markdown('<div class="no-res">Нет форматов, соответствующих выбранным фильтрам.</div>',
                unsafe_allow_html=True)
else:
    # Max values for progress bars
    max_reach_all = df["max_reach"].max()
    max_ctr_all   = min(df["ctr_avg"].max(), 0.05) if df["ctr_avg"].notna().any() else 0.05
    max_vw_all    = 1.0

    sel_id = st.session_state.get("sel_fmt_id", None)

    # Build HTML table rows
    def type_tags(cell):
        if not isinstance(cell, list): return ""
        return "".join(f'<span class="tag {"tag-v" if t=="Видео" else "tag-b"}">{t}</span>' for t in cell)

    def model_tag(v):
        return f'<span class="tag {"tag-cpm" if str(v).upper()=="CPM" else "tag-cpc"}">{v}</span>'

    def dev_tags(cell):
        if not isinstance(cell, list): return ""
        return "".join(f'<span class="tag">{d}</span>' for d in cell)

    def score_html(s):
        try:
            if pd.isna(s): return ""
            v = float(s)
            cls = "sc-hi" if v>=65 else ("sc-md" if v>=40 else "sc-lo")
            return f'<span class="sc-pill {cls}">{v:.0f}</span>'
        except Exception: return ""

    last_th = "<th>Скор</th>" if scoring else "<th>eCPM (сез.)</th>"

    rows_html = ""
    for _, row in F.iterrows():
        fid = row["format_id"]
        sel_cls = "sel" if fid == sel_id else ""

        es = row.get("ecpm_s", np.nan)
        last_td = score_html(row.get("score", np.nan)) if scoring else \
                  f'<span style="font-family:\'DM Mono\',monospace;font-size:12px;">{rub(es)}</span>'

        rows_html += f"""
        <tr class="{sel_cls}" data-fid="{fid}">
            <td><div class="f-name">{row['format_name']}</div>
                <div class="f-id">{fid}</div></td>
            <td>{type_tags(row.get('format_type',[]))}</td>
            <td>{model_tag(row['buy_model'])}</td>
            <td>{dev_tags(row.get('device',[]))}</td>
            <td>{mbar(row.get('max_reach'), max_reach_all, reach_s(row.get('max_reach')))}</td>
            <td>{mbar(row.get('ctr_avg'), max_ctr_all, pct(row.get('ctr_avg')))}</td>
            <td>{mbar(row.get('viewability_avg'), max_vw_all, pct(row.get('viewability_avg')))}</td>
            <td>{last_td}</td>
        </tr>"""

    # Hidden input to receive selected format id from JS
    clicked_id = st.query_params.get("fmt", None)
    if clicked_id and clicked_id in F["format_id"].values:
        st.session_state["sel_fmt_id"] = clicked_id
        sel_id = clicked_id

    st.markdown(f"""
    <div class="fmt-tbl-wrap">
    <table class="fmt-tbl">
        <thead><tr>
            <th>Формат</th><th>Тип</th><th>Модель</th><th>Устройства</th>
            <th>Охват</th><th>CTR</th><th>Viewability</th>{last_th}
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    # ─── ROW CLICK: use st.dataframe on top (invisible), capture selection ───
    # Build minimal df just for selection
    sel_df = F[["format_name","format_id"]].copy().reset_index(drop=True)
    ev = st.dataframe(
        sel_df,
        hide_index=True,
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "format_name": st.column_config.TextColumn("Выберите формат из таблицы выше"),
            "format_id":   st.column_config.TextColumn("ID", width="small"),
        },
        height=min(500, (len(F)+1)*38+2),
        key="sel_df",
    )
    sel_rows = ev.selection.rows if hasattr(ev, "selection") else []

    # ─── CARD ─────────────────────────────────────────────────────────────────
    if sel_rows:
        idx = sel_rows[0]
        r   = F.iloc[idx]

        def gf(field, default=np.nan):
            val = r.get(field, default)
            if val is None: return default
            try:
                if isinstance(val, float) and np.isnan(val): return default
            except Exception: pass
            return val

        ee  = gf("ecpm_eff")
        es2 = gf("ecpm_s")
        sc  = gf("sk", 1.0)
        sc_disp = f"{float(sc):.1f}".replace(".", ",") if sc != int(sc) else str(int(sc))

        sc_score = gf("score", np.nan)
        score_badge_html = ""
        if scoring:
            try:
                if not np.isnan(float(sc_score)):
                    sv2 = float(sc_score)
                    cls2 = "sc-hi" if sv2>=65 else ("sc-md" if sv2>=40 else "sc-lo")
                    score_badge_html = f'<span class="sc-pill {cls2}" style="margin-left:8px;">{sv2:.0f}</span>'
            except Exception: pass

        links = []
        for lbl_, key in [("Пример","example_url"),("Техтребования","technical_requirements_url"),
                           ("Медиакит","mediakit_url"),("Кейсы","cases_url")]:
            v = gf(key, "")
            if isinstance(v, str) and v.startswith("http"):
                links.append(f'<a class="link-a" href="{v}" target="_blank">{lbl_} ↗</a>')

        st.markdown(f"""
        <div class="card">
            <div class="card-top">
                <div>
                    <div class="card-title">{sv(gf('format_name'))}{score_badge_html}</div>
                    <div class="card-meta">{sv(gf('format_id'))} · {sv(gf('buy_model'))} · {sv(gf('platform'))}</div>
                </div>
                <div>{"".join(links)}</div>
            </div>
            <div class="card-desc">{sv(gf('description'), 'Описание не указано')}</div>

            <div class="c-grid">
                <div class="c-m"><div class="c-lbl">eCPM (факт)</div><div class="c-val">{rub(ee)}</div></div>
                <div class="c-m"><div class="c-lbl">eCPM (сезон. {sc_disp}×)</div><div class="c-val">{rub(es2)}</div></div>
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
                    <span class="info-val" style="font-size:12px;color:var(--muted);">{sv(gf('verification_terms'))}</span></div>
                <div class="c-sec">Исследования</div>
                <div class="info-row"><span class="info-lbl">Brand Lift</span><span class="info-val">{bv(gf('bls'))}</span></div>
                <div class="info-row"><span class="info-lbl">Sales Lift</span><span class="info-val">{bv(gf('sales_lift'))}</span></div>
            </div>
            <div>
                <div class="c-sec">Плейсмент</div><div class="tags-row">{thtml(gf('placement',[]))}</div>
                <div class="c-sec">Устройства</div><div class="tags-row">{thtml(gf('device',[]))}</div>
                <div class="c-sec">Отображение</div><div class="tags-row">{thtml(gf('display',[]))}</div>
                <div class="c-sec">DMP</div><div class="tags-row">{thtml(gf('dmp',[]))}</div>
                <div class="c-sec">Производство</div><div class="tags-row">{thtml(gf('production',[]))}</div>
            </div>
            </div>

            <div class="c-sec">Таргетинг</div>
            <div class="tags-row">{thtml(gf('targeting',[]))}</div>
            <div class="c-sec">Наценки за таргетинг</div>
            <div class="tags-row">{thtml(gf('targeting_markup',[]))}</div>
        </div>
        """, unsafe_allow_html=True)

        for lbl_, key in [("Условия Brand Lift","bls_terms"),
                           ("Условия Sales Lift","sales_lift_terms"),
                           ("Условия сезонности","seasonality_terms")]:
            v = gf(key, "")
            if isinstance(v, str) and v.strip():
                with st.expander(f"📋 {lbl_}"):
                    st.markdown(f'<p style="font-size:13px;line-height:1.65;">{v}</p>',
                                unsafe_allow_html=True)
