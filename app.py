import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Format Selector", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=DM+Mono:wght@400;500&display=swap');

:root {
  --white:  #FFFFFF;
  --mint:   #C0FFD9;
  --blue:   #3E20FF;
  --indigo: #725BFF;
  --bg:     #F8F2FF;
  --dark:   #070037;
  --muted:  rgba(7,0,55,0.42);
  --border: rgba(7,0,55,0.10);
}

/* ── global ── */
*, *::before, *::after { font-family: 'DM Sans', sans-serif !important; box-sizing: border-box; }
html, body { background: var(--bg) !important; }
.main      { background: var(--bg) !important; }
.main .block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1440px; }

/* ── sidebar shell – white with right border ── */
section[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: none !important;
}
/* inner Streamlit padding override */
section[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
section[data-testid="stSidebar"] .block-container  { padding: 0 !important; max-width: none !important; }

/* all text inside sidebar */
section[data-testid="stSidebar"] * {
    color: var(--dark) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* select boxes inside sidebar */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 7px !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: var(--muted) !important; }
/* multiselect tags */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: var(--blue) !important;
    border: none !important;
    border-radius: 5px !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] span { color: #fff !important; font-size: 11.5px !important; }
section[data-testid="stSidebar"] [data-baseweb="tag"] [role="presentation"] svg { fill: rgba(255,255,255,.65) !important; }

/* slider dot */
section[data-testid="stSidebar"] [role="slider"] { background: var(--blue) !important; }

/* ── sidebar custom classes ── */
.sb-wrap  { padding: 0 1.1rem 2rem; }
.sb-head  { padding: 1rem 1.1rem .9rem; border-bottom: 1px solid var(--border); margin-bottom: 2px; }
.sb-brand { font-size: 14px; font-weight: 600; color: var(--dark) !important; }
.sb-sub   { font-size: 11px; color: var(--muted) !important; margin-top: 2px; }
.sb-sec   { font-size: 9px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
            color: var(--muted) !important; display: block; margin: 14px 0 4px; }
.sb-rule  { border: none; border-top: 1px solid var(--border); margin: 12px 0; }

/* ── header ── */
.hdr { display: flex; align-items: center; justify-content: space-between;
       padding-bottom: .9rem; margin-bottom: 1.2rem; border-bottom: 1px solid var(--border); }
.hdr-l { display: flex; align-items: baseline; gap: 10px; }
.hdr-t { font-size: 1.1rem; font-weight: 600; color: var(--dark); margin: 0; letter-spacing: -.02em; }
.hdr-s { font-size: 11.5px; color: var(--muted); font-family: 'DM Mono', monospace !important; }
.hdr-badge { font-size: 9px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
             background: var(--mint); color: var(--dark); padding: 3px 10px; border-radius: 20px; }

/* ── KPI row – equal height ── */
.kpi-row  { display: flex; gap: 10px; margin-bottom: 1.1rem; align-items: stretch; }
.kpi-card { flex: 1; background: var(--white); border: 1px solid var(--border);
            border-top: 2px solid var(--blue); border-radius: 11px;
            padding: 14px 16px; min-height: 88px;
            display: flex; flex-direction: column; justify-content: space-between; }
.kpi-card.mint { border-top-color: var(--mint); }
.kpi-lbl { font-size: 10.5px; color: var(--muted); font-weight: 500; margin-bottom: 5px; }
.kpi-val { font-size: 1.38rem; font-weight: 600; color: var(--dark);
           font-family: 'DM Mono', monospace !important; line-height: 1.05; letter-spacing: -.02em; }
.kpi-sm  { font-size: .875rem; font-weight: 600; color: var(--dark); line-height: 1.35; }
.kpi-sub { font-size: 10px; color: var(--muted); margin-top: 4px; }

/* ── section label ── */
.slabel { font-size: 9px; font-weight: 700; letter-spacing: .11em; text-transform: uppercase;
          color: var(--muted); margin: 1.2rem 0 .5rem; display: block; }

/* ── HTML table ── */
.fmt-tbl-wrap { background: var(--white); border: 1px solid var(--border); border-radius: 11px; overflow: hidden; }
.fmt-tbl { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.fmt-tbl th { padding: 9px 13px; background: var(--bg); border-bottom: 1px solid var(--border);
              font-size: 9px; font-weight: 700; letter-spacing: .09em; text-transform: uppercase;
              color: var(--muted); white-space: nowrap; text-align: left; }
.fmt-tbl td { padding: 9px 13px; border-bottom: 1px solid rgba(7,0,55,.05); vertical-align: middle; }
.fmt-tbl tbody tr:last-child td { border-bottom: none; }
.fmt-tbl tbody tr { transition: background .1s; }
.fmt-tbl tbody tr:hover td { background: rgba(62,32,255,.04); }

.f-name { font-weight: 500; font-size: 13px; color: var(--dark); }
.f-id   { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--muted); margin-top: 1px; }

.tag     { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 500;
           margin: 1px 2px 1px 0; background: rgba(62,32,255,.08); color: var(--dark); }
.tag-v   { background: rgba(192,255,217,.6); color: #055c30; }
.tag-b   { background: rgba(114,91,255,.10); color: #4433bb; }
.tag-cpm { background: transparent; color: var(--dark); border: 1px solid var(--border); }
.tag-cpc { background: rgba(62,32,255,.10); color: var(--blue); }

.mbar-wrap { display: flex; align-items: center; gap: 6px; }
.mbar-bg   { height: 4px; background: rgba(7,0,55,.08); border-radius: 3px; flex: 1; min-width: 40px; }
.mbar-fill { height: 4px; border-radius: 3px; background: var(--blue); }
.mbar-val  { font-family: 'DM Mono', monospace; font-size: 11px; color: var(--dark);
             min-width: 38px; text-align: right; white-space: nowrap; }

.sc-pill { display: inline-flex; align-items: center; padding: 2px 7px; border-radius: 20px;
           font-size: 11px; font-weight: 600; font-family: 'DM Mono', monospace !important; }
.sc-hi { background: var(--mint); color: #055c30; }
.sc-md { background: rgba(62,32,255,.09); color: var(--blue); }
.sc-lo { background: var(--bg); color: var(--muted); }

/* ── Card ── */
.card { background: var(--white); border: 1px solid var(--border); border-left: 3px solid var(--blue);
        border-radius: 12px; padding: 22px; margin-top: 14px;
        animation: fadeSlide .2s ease both; }
@keyframes fadeSlide { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }
.card-top  { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 4px; }
.card-ttl  { font-size: 1rem; font-weight: 600; color: var(--dark); letter-spacing: -.01em; }
.card-meta { font-family: 'DM Mono', monospace !important; font-size: 10.5px; color: var(--muted); margin-bottom: 11px; }
.card-desc { font-size: 13px; color: var(--dark); line-height: 1.6; padding: 10px 13px;
             background: var(--bg); border-radius: 8px; margin-bottom: 14px; }
.c-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin-bottom: 14px; }
.c-m    { background: var(--bg); border-radius: 8px; padding: 10px 12px; }
.c-lbl  { font-size: 9px; color: var(--muted); font-weight: 700; text-transform: uppercase;
          letter-spacing: .08em; margin-bottom: 4px; }
.c-val  { font-size: .975rem; font-weight: 600; color: var(--dark);
          font-family: 'DM Mono', monospace !important; }
.c-sec  { font-size: 9px; font-weight: 700; letter-spacing: .10em; text-transform: uppercase;
          color: var(--muted); margin: 12px 0 5px; }
.info-row { display: flex; gap: 8px; margin-bottom: 4px; }
.info-lbl { font-size: 12px; color: var(--muted); min-width: 158px; flex-shrink: 0; }
.info-val { font-size: 12px; color: var(--dark); font-weight: 500; }
.tags-row { display: flex; flex-wrap: wrap; gap: 4px; }
.bool-y   { color: var(--blue); font-weight: 700; }
.bool-n   { color: rgba(7,0,55,.18); }
.link-a   { font-size: 12px; color: var(--blue); text-decoration: none; margin-right: 12px; font-weight: 500; }

.w-wrap { display: inline-block; font-size: 12px; font-weight: 600;
          font-family: 'DM Mono', monospace !important; padding: 4px 11px;
          border-radius: 7px; margin: 5px 0 2px; }
.w-ok  { background: var(--mint); color: #055c30; }
.w-bad { background: rgba(62,32,255,.09); color: var(--indigo); }

.no-res { text-align: center; padding: 48px 20px; color: var(--muted);
          background: var(--white); border: 1px solid var(--border);
          border-radius: 11px; font-size: 13px; }
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
        raise FileNotFoundError(f"{a} / {b}")
    df = rc("DataLens_-_formats.csv", "DataLens - formats.csv")
    di = rc("DataLens_-_dict_items.csv", "DataLens - dict_items.csv")
    fi = None
    for n in ["DataLens_-_format_items.csv", "DataLens - format_items.csv"]:
        if os.path.exists(p(n)): fi = pd.read_csv(p(n)); break
    if fi is None and os.path.exists(p("DataLens.xlsx")):
        fi = pd.read_excel(p("DataLens.xlsx"), sheet_name="format_items")
    if fi is None: raise FileNotFoundError("format_items")
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
        f = float(v)
        if np.isnan(f): return "—"
        x = round(f*100, 1)
        s = f"{int(x)}%" if x == int(x) else f"{x:.1f}%"
        return s.replace(".", ",")
    except: return "—"

def rub(v):
    try:
        f = float(v)
        if np.isnan(f): return "—"
        return f"{int(round(f)):,} ₽".replace(",", "\u202f")
    except: return "—"

def reach_s(v):
    try:
        f = float(v)
        if np.isnan(f): return "—"
        m = f / 1e6
        if m >= 1:
            s = f"{int(m)}M" if m == int(m) else f"{m:.1f}M"
            return s.replace(".", ",")
        return f"{int(f):,}".replace(",", "\u202f")
    except: return "—"

def bv(v):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return '<span class="bool-n">—</span>'
    except: pass
    return ('<span class="bool-y">✓</span>'
            if str(v).upper() in ("TRUE","1")
            else '<span class="bool-n">—</span>')

def sv(v, default="—"):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)): return default
    except: pass
    s = str(v).strip(); return s if s else default

def thtml(cell):
    if not isinstance(cell, list) or not cell:
        return '<span style="color:rgba(7,0,55,.16);font-size:11px;">—</span>'
    return "".join(f'<span class="tag">{t}</span>' for t in cell if t)

def mbar(val, max_val, disp):
    if disp == "—": return '<span style="color:rgba(7,0,55,.18);font-size:11px;">—</span>'
    try: pw = min(float(val)/float(max_val)*100, 100) if max_val else 0
    except: pw = 0
    return (f'<div class="mbar-wrap">'
            f'<div class="mbar-bg"><div class="mbar-fill" style="width:{pw:.1f}%"></div></div>'
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
    except: return np.nan

df["ecpm_eff"] = df.apply(calc_ecpm, axis=1)
def opts(did): return di[di["dict_id"]==did]["item_name"].dropna().tolist()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-head"><div class="sb-brand">Format Selector</div>'
                '<div class="sb-sub">Анализ рекламных форматов</div></div>'
                '<div class="sb-wrap">', unsafe_allow_html=True)

    def ss(t): st.markdown(f'<span class="sb-sec">{t}</span>', unsafe_allow_html=True)
    def sd():  st.markdown('<hr class="sb-rule">', unsafe_allow_html=True)

    ss("Тип формата")
    format_types = st.multiselect("_", ["Видео","Баннер"],
                                  default=["Видео","Баннер"],
                                  placeholder="Все типы",
                                  label_visibility="collapsed")
    ss("Устройство")
    devices = st.multiselect("_d", ["Desktop","Mobile Web","In-App","Smart TV"],
                              default=["Desktop","Mobile Web","In-App","Smart TV"],
                              placeholder="Все устройства",
                              label_visibility="collapsed")
    ss("Модель закупки")
    buy_models = st.multiselect("_m", ["CPM","CPC"],
                                default=["CPM","CPC"],
                                placeholder="Все модели",
                                label_visibility="collapsed")

    show_b = not format_types or "Баннер" in format_types
    show_v = not format_types or "Видео"  in format_types

    if show_b:
        ss("Отображение (баннер)")
        f_disp = st.multiselect("_db", opts("display"), default=[],
                                placeholder="Все варианты",
                                label_visibility="collapsed")
    else:
        f_disp = []

    if show_v:
        ss("Плейсмент (видео)")
        f_plac = st.multiselect("_pl", opts("placement"), default=[],
                                placeholder="Все плейсменты",
                                label_visibility="collapsed")
        ss("Позиция (видео)")
        f_inst = st.multiselect("_in", opts("instream_pos"), default=[],
                                placeholder="Все позиции",
                                label_visibility="collapsed")
    else:
        f_plac = []; f_inst = []

    ss("Таргетинги")
    f_targ = st.multiselect("_tr", opts("targeting"), default=[],
                             placeholder="Все таргетинги",
                             label_visibility="collapsed")
    ss("DMP")
    f_dmp = st.multiselect("_dp", opts("dmp"), default=[],
                            placeholder="Все DMP",
                            label_visibility="collapsed")
    sd()

    ss("Дополнительно")
    req_px = st.checkbox("Верификация пикселем", key="cb_px")
    req_js = st.checkbox("Верификация JS-тегом", key="cb_js")
    req_bl = st.checkbox("Brand Lift",            key="cb_bl")
    req_sl = st.checkbox("Sales Lift",            key="cb_sl")
    sd()

    ss("Пороговые значения")
    max_ecpm_f = st.slider("Макс. eCPM (после скидки), ₽", 0, 1000, 1000, step=10)
    min_ctr    = st.slider("Мин. CTR, %",         0.0, 5.0, 0.0, step=0.1)
    min_rch    = st.slider("Мин. охват, млн",     0.0,80.0, 0.0, step=1.0)
    min_view   = st.slider("Мин. Viewability, %",   0, 100,   0, step=5)
    min_vtr    = st.slider("Мин. VTR, %",         0.0,100., 0.0, step=5.0)
    sd()

    scoring = st.toggle("Включить скоринг", value=False)
    if scoring:
        ss("Веса (сумма = 100)")
        wr = st.slider("Охват",                    0,100,20,step=5)
        we = st.slider("eCPM (ниже — лучше)",      0,100,20,step=5)
        wc = st.slider("CTR",                      0,100,20,step=5)
        wv = st.slider("VTR",                      0,100,15,step=5)
        wi = st.slider("Viewability",              0,100,15,step=5)
        wm = st.slider("Комиссия (ниже — лучше)",  0,100,10,step=5)
        tw = wr+we+wc+wv+wi+wm
        st.markdown(
            f'<div class="w-wrap {"w-ok" if tw==100 else "w-bad"}">Сумма: {tw} / 100</div>',
            unsafe_allow_html=True)
        norm = st.checkbox("Нормализовать веса", value=True)
    else:
        wr=we=wc=wv=wi=wm=tw=0; norm=False
    sd()

    ss("Сезонность")
    months = ["Январь","Февраль","Март","Апрель","Май","Июнь",
              "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
    sel_m = st.selectbox("_mo", months, index=months.index("Март"),
                          label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

# ─── FILTER ───────────────────────────────────────────────────────────────────
def has(c, items):   return isinstance(c, list) and any(i in c for i in items)
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
if req_px: F = F[F["verification_pixel"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
if req_js: F = F[F["verification_js"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
if req_bl: F = F[F["bls"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
if req_sl: F = F[F["sales_lift"].apply(lambda v: str(v).upper() in ("TRUE","1"))]
F = F[F["ecpm_eff"].fillna(9999) <= max_ecpm_f]
if min_ctr  > 0: F = F[F["ctr_avg"].fillna(0)          >= min_ctr/100]
if min_rch  > 0: F = F[F["max_reach"].fillna(0)         >= min_rch*1e6]
if min_view > 0: F = F[F["viewability_avg"].fillna(0)   >= min_view/100]
if min_vtr  > 0: F = F[F["vtr_avg"].fillna(0)           >= min_vtr/100]

F = F.copy()
F["_sk"] = F["platform"].apply(lambda p: sk(p, sel_m))
F["ecpm_s"] = F["ecpm_eff"] * F["_sk"]

# ─── SCORING ──────────────────────────────────────────────────────────────────
def ncol(s, inv=False):
    mn, mx = s.min(), s.max()
    if mx == mn: return pd.Series([0.5]*len(s), index=s.index)
    n = (s-mn)/(mx-mn); return 1-n if inv else n

if scoring and len(F) > 0:
    W = dict(r=wr,e=we,c=wc,v=wv,i=wi,m=wm); t = sum(W.values())
    if norm and t > 0: W = {k:v/t   for k,v in W.items()}
    else:              W = {k:v/100 for k,v in W.items()}
    ev = F["ecpm_s"].max()*2 if F["ecpm_s"].notna().any() else 9999
    cv = F["commission"].max() if F["commission"].notna().any() else 1
    F["score"] = (
        ncol(F["max_reach"].fillna(0))            * W["r"] +
        ncol(F["ecpm_s"].fillna(ev), inv=True)    * W["e"] +
        ncol(F["ctr_avg"].fillna(0))              * W["c"] +
        ncol(F["vtr_avg"].fillna(0))              * W["v"] +
        ncol(F["viewability_avg"].fillna(0))      * W["i"] +
        ncol(F["commission"].fillna(cv),inv=True) * W["m"]
    ) * 100
    F = F.sort_values("score", ascending=False).reset_index(drop=True)
else:
    F["score"] = np.nan
    F = F.sort_values("ecpm_s", ascending=True, na_position="last").reset_index(drop=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
n_plat = df["platform"].nunique()
badge  = f"{n_plat} {'площадка' if n_plat==1 else ('площадки' if n_plat<5 else 'площадок')} · бета"
st.markdown(
    f'<div class="hdr">'
    f'<div class="hdr-l"><span class="hdr-t">Format Selector</span>'
    f'<span class="hdr-s">Анализ рекламных форматов</span></div>'
    f'<span class="hdr-badge">{badge}</span></div>',
    unsafe_allow_html=True)

# ─── KPI ──────────────────────────────────────────────────────────────────────
top   = F.iloc[0] if len(F) > 0 else None
avg_e = F["ecpm_s"].mean() if len(F) > 0 else np.nan
sk0   = float(F["_sk"].iloc[0]) if len(F) > 0 else 1.0
maxr  = F["max_reach"].max() if len(F) > 0 else np.nan

lbl2 = "Лучший по скорингу" if scoring else "Самый дешевый eCPM"
if top is not None:
    sub2 = (f'Скор: {top["score"]:.0f}'
            if scoring and not pd.isna(top.get("score", np.nan))
            else sv(top.get("buy_model","—")))
    val2 = f'<div class="kpi-sm">{sv(top.get("format_name","—"))}</div>'
else:
    sub2 = ""; val2 = '<div class="kpi-val">—</div>'

st.markdown(
    f'<div class="kpi-row">'
    f'<div class="kpi-card"><div><div class="kpi-lbl">Форматов после фильтров</div>'
    f'<div class="kpi-val">{len(F)}</div></div>'
    f'<div class="kpi-sub">из {len(df)} доступных</div></div>'
    f'<div class="kpi-card"><div><div class="kpi-lbl">{lbl2}</div>{val2}</div>'
    f'<div class="kpi-sub">{sub2}</div></div>'
    f'<div class="kpi-card"><div><div class="kpi-lbl">Средний eCPM (с сезонностью)</div>'
    f'<div class="kpi-val">{rub(avg_e)}</div></div>'
    f'<div class="kpi-sub">{sel_m} · коэф. {sk0}×</div></div>'
    f'<div class="kpi-card mint"><div><div class="kpi-lbl">Макс. охват</div>'
    f'<div class="kpi-val">{reach_s(maxr)}</div></div>'
    f'<div class="kpi-sub">среди отфильтрованных</div></div>'
    f'</div>',
    unsafe_allow_html=True)

# ─── CHARTS ───────────────────────────────────────────────────────────────────
if len(F) > 0:
    ch1, ch2 = st.columns(2)

    # ── LEFT: horizontal bar – compact, max 12 bars ──
    with ch1:
        cdf = F[F["ecpm_s"].notna()].sort_values("ecpm_s", ascending=False).head(12)
        if len(cdf) > 0:
            cdf_plot = cdf.sort_values("ecpm_s")  # ascending for horizontal bar
            n = len(cdf_plot)
            if scoring and cdf_plot["score"].notna().any():
                mn_, mx_ = cdf_plot["score"].min(), cdf_plot["score"].max()
                cols = [f"rgba(62,32,255,{0.3+0.7*(s-mn_)/max(mx_-mn_,1):.2f})"
                        for s in cdf_plot["score"].fillna(mn_)]
            else:
                cols = [f"rgba(62,32,255,{0.32+0.68*i/max(n-1,1):.2f})" for i in range(n)]

            fig1 = go.Figure(go.Bar(
                x=cdf_plot["ecpm_s"].round(0),
                y=cdf_plot["format_name"],
                orientation="h",
                marker_color=cols, marker_line_width=0,
                hovertemplate="<b>%{y}</b><br>eCPM: %{x:.0f} ₽<extra></extra>"
            ))
            fig1.update_layout(
                title=dict(text="eCPM по форматам (₽, с сезонностью)",
                           font=dict(size=10, color="rgba(7,0,55,.42)", family="DM Sans")),
                height=max(220, n*26+50),
                margin=dict(l=0,r=10,t=34,b=4),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(gridcolor="rgba(7,0,55,.06)", tickfont_size=9,
                           tickfont_color="rgba(7,0,55,.4)", zeroline=False, title=None),
                yaxis=dict(tickfont_size=10, tickfont_color="#070037", title=None, tickmode="linear"),
                font_family="DM Sans", bargap=0.35,
            )
            st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    # ── RIGHT: eCPM vs CTR scatter (bubble = reach) ──
    with ch2:
        sdf = F[F["ecpm_s"].notna() & F["ctr_avg"].notna()].copy()
        if len(sdf) >= 2:
            med = float(sdf["max_reach"].median()) if sdf["max_reach"].notna().any() else 1e6
            sdf["bsz"] = sdf["max_reach"].fillna(med).apply(lambda v: max(7, min(32, float(v)/2.2e6)))
            if scoring and sdf["score"].notna().any():
                mn2, mx2 = sdf["score"].min(), sdf["score"].max()
                scols = [f"rgba(62,32,255,{0.28+0.72*(s-mn2)/max(mx2-mn2,1):.2f})"
                         for s in sdf["score"].fillna(mn2)]
            else:
                scols = ["#725BFF"] * len(sdf)

            fig2 = go.Figure()
            for i, (_, row) in enumerate(sdf.iterrows()):
                fig2.add_trace(go.Scatter(
                    x=[float(row["ctr_avg"])*100],
                    y=[float(row["ecpm_s"])],
                    mode="markers+text",
                    marker=dict(size=row["bsz"], color=scols[i],
                                line=dict(color="white", width=1.5)),
                    text=[row["format_name"]],
                    textposition="top center",
                    textfont=dict(size=8, color="#070037"),
                    hovertemplate=(
                        f"<b>{row['format_name']}</b><br>"
                        f"CTR: {float(row['ctr_avg'])*100:.2f}%<br>"
                        f"eCPM: {float(row['ecpm_s']):.0f} ₽<extra></extra>"),
                    showlegend=False
                ))
            fig2.update_layout(
                title=dict(text="CTR vs eCPM (размер — охват)",
                           font=dict(size=10, color="rgba(7,0,55,.42)", family="DM Sans")),
                height=max(220, len(sdf)*26+50),
                margin=dict(l=0,r=10,t=34,b=4),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(title="CTR, %", gridcolor="rgba(7,0,55,.06)",
                           tickfont_size=9, title_font_size=9,
                           tickfont_color="rgba(7,0,55,.4)", title_font_color="rgba(7,0,55,.4)",
                           zeroline=False),
                yaxis=dict(title="eCPM, ₽", gridcolor="rgba(7,0,55,.06)",
                           tickfont_size=9, title_font_size=9,
                           tickfont_color="rgba(7,0,55,.4)", title_font_color="rgba(7,0,55,.4)",
                           zeroline=False),
                font_family="DM Sans",
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ─── TABLE via st.dataframe with row selection ────────────────────────────────
st.markdown('<span class="slabel">Форматы</span>', unsafe_allow_html=True)

if len(F) == 0:
    st.markdown('<div class="no-res">Нет форматов, соответствующих выбранным фильтрам.</div>',
                unsafe_allow_html=True)
else:
    # Build display dataframe – text columns so we can format nicely
    def _list(c): return ", ".join(c) if isinstance(c, list) else ""
    def _sc(s):
        try: return "" if pd.isna(s) else f"{s:.0f}"
        except: return ""

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
    if scoring: disp["Скор"] = F["score"].apply(_sc)

    ev = st.dataframe(
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
        height=min(560, (len(F)+1)*38+2),
        key="main_tbl",
    )

    sel = ev.selection.rows if hasattr(ev, "selection") else []

    # ─── CARD ─────────────────────────────────────────────────────────────────
    if sel:
        r = F.iloc[sel[0]]

        def gf(field, default=np.nan):
            val = r.get(field, default)
            if val is None: return default
            try:
                if isinstance(val, float) and np.isnan(val): return default
            except: pass
            return val

        ee  = gf("ecpm_eff")
        es2 = gf("ecpm_s")
        sc  = gf("_sk", 1.0)
        try:
            sc_f = float(sc)
            sc_d = str(int(sc_f)) if sc_f == int(sc_f) else f"{sc_f:.1f}".replace(".", ",")
        except: sc_d = "1"

        # score badge
        score_badge = ""
        if scoring:
            try:
                sv_ = float(gf("score", np.nan))
                if not np.isnan(sv_):
                    cls_ = "sc-hi" if sv_>=65 else ("sc-md" if sv_>=40 else "sc-lo")
                    score_badge = '<span class="sc-pill ' + cls_ + '" style="margin-left:8px;">' + str(int(sv_)) + '</span>'
            except: pass

        # links
        links_html = ""
        for lbl_, uk in [("Пример","example_url"),
                          ("Техтребования","technical_requirements_url"),
                          ("Медиакит","mediakit_url"),
                          ("Кейсы","cases_url")]:
            v = gf(uk, "")
            if isinstance(v, str) and v.startswith("http"):
                links_html += '<a class="link-a" href="' + v + '" target="_blank">' + lbl_ + ' ↗</a>'

        # metric grid
        ecpm_lbl = "eCPM (сезон. " + sc_d + "×)"
        grid_html = (
            '<div class="c-m"><div class="c-lbl">eCPM (факт)</div><div class="c-val">' + rub(ee) + '</div></div>'
            + '<div class="c-m"><div class="c-lbl">' + ecpm_lbl + '</div><div class="c-val">' + rub(es2) + '</div></div>'
            + '<div class="c-m"><div class="c-lbl">Скидка</div><div class="c-val">' + pct(gf("discount")) + '</div></div>'
            + '<div class="c-m"><div class="c-lbl">Охват (макс.)</div><div class="c-val">' + reach_s(gf("max_reach")) + '</div></div>'
            + '<div class="c-m"><div class="c-lbl">CTR (среднее)</div><div class="c-val">' + pct(gf("ctr_avg")) + '</div></div>'
            + '<div class="c-m"><div class="c-lbl">VTR (среднее)</div><div class="c-val">' + pct(gf("vtr_avg")) + '</div></div>'
            + '<div class="c-m"><div class="c-lbl">Viewability (среднее)</div><div class="c-val">' + pct(gf("viewability_avg")) + '</div></div>'
            + '<div class="c-m"><div class="c-lbl">Комиссия</div><div class="c-val">' + pct(gf("commission")) + '</div></div>'
            + '<div class="c-m"><div class="c-lbl">Мин. бюджет</div><div class="c-val">' + rub(gf("min_budget")) + '</div></div>'
        )

        info_left = (
            '<div class="c-sec">Ценовой диапазон</div>'
            + '<div class="info-row"><span class="info-lbl">CPM мин / сред / макс</span>'
            + '<span class="info-val">' + rub(gf("cpm_min")) + " / " + rub(gf("cpm_avg")) + " / " + rub(gf("cpm_max")) + '</span></div>'
            + '<div class="info-row"><span class="info-lbl">CPC мин / сред / макс</span>'
            + '<span class="info-val">' + rub(gf("cpc_min")) + " / " + rub(gf("cpc_avg")) + " / " + rub(gf("cpc_max")) + '</span></div>'
            + '<div class="info-row"><span class="info-lbl">CTR мин / макс</span>'
            + '<span class="info-val">' + pct(gf("ctr_min")) + " / " + pct(gf("ctr_max")) + '</span></div>'
            + '<div class="c-sec">Верификация</div>'
            + '<div class="info-row"><span class="info-lbl">Пиксель</span><span class="info-val">' + bv(gf("verification_pixel")) + '</span></div>'
            + '<div class="info-row"><span class="info-lbl">JS-тег</span><span class="info-val">' + bv(gf("verification_js")) + '</span></div>'
            + '<div class="info-row"><span class="info-lbl">Условия</span>'
            + '<span class="info-val" style="font-size:12px;color:var(--muted);">' + sv(gf("verification_terms")) + '</span></div>'
            + '<div class="c-sec">Исследования</div>'
            + '<div class="info-row"><span class="info-lbl">Brand Lift</span><span class="info-val">' + bv(gf("bls")) + '</span></div>'
            + '<div class="info-row"><span class="info-lbl">Sales Lift</span><span class="info-val">' + bv(gf("sales_lift")) + '</span></div>'
        )

        info_right = (
            '<div class="c-sec">Плейсмент</div><div class="tags-row">' + thtml(gf("placement",[])) + '</div>'
            + '<div class="c-sec">Устройства</div><div class="tags-row">' + thtml(gf("device",[])) + '</div>'
            + '<div class="c-sec">Отображение</div><div class="tags-row">' + thtml(gf("display",[])) + '</div>'
            + '<div class="c-sec">DMP</div><div class="tags-row">' + thtml(gf("dmp",[])) + '</div>'
            + '<div class="c-sec">Производство</div><div class="tags-row">' + thtml(gf("production",[])) + '</div>'
        )

        card_html = (
            '<div class="card">'
            + '<div class="card-top">'
            + '<div><div class="card-ttl">' + sv(gf("format_name")) + score_badge + '</div>'
            + '<div class="card-meta">' + sv(gf("format_id")) + ' · ' + sv(gf("buy_model")) + ' · ' + sv(gf("platform")) + '</div></div>'
            + ('<div>' + links_html + '</div>' if links_html else '')
            + '</div>'
            + '<div class="card-desc">' + sv(gf("description"), "Описание не указано") + '</div>'
            + '<div class="c-grid">' + grid_html + '</div>'
            + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">'
            + '<div>' + info_left + '</div><div>' + info_right + '</div>'
            + '</div>'
            + '<div class="c-sec">Таргетинг</div>'
            + '<div class="tags-row">' + thtml(gf("targeting",[])) + '</div>'
            + '<div class="c-sec">Наценки за таргетинг</div>'
            + '<div class="tags-row">' + thtml(gf("targeting_markup",[])) + '</div>'
            + '</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

        for lbl_, key in [("Условия Brand Lift","bls_terms"),
                           ("Условия Sales Lift","sales_lift_terms"),
                           ("Условия сезонности","seasonality_terms")]:
            v = gf(key, "")
            if isinstance(v, str) and v.strip():
                with st.expander("📋 " + lbl_):
                    st.markdown('<p style="font-size:13px;line-height:1.65;">' + v + '</p>',
                                unsafe_allow_html=True)
