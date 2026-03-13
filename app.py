import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Format Selector", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

# ─── DESIGN SYSTEM (per audit) ────────────────────────────────────────────────
# Primary accent:  #3E20FF  — CTAs, active states, key highlights only
# Background:      #FFFFFF / page #F8F2FF
# Dark surfaces:   #070037
# Secondary:       #725BFF  — progress bars, secondary badges
# Soft purple bg:  #F8F2FF  — hover rows, selected panel bg
# Status teal:     #77F5DF / #C0FFD9 / #EEFFF5 — Видео tags, positive metrics
# Neutral muted:   #B1B4B8
# Typography: Inter, 400 body / 500 labels+values, sentence case, max 18px

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
  --accent:   #3E20FF;
  --bg-page:  #F8F2FF;
  --bg-white: #FFFFFF;
  --bg-soft:  #F8F2FF;
  --dark:     #070037;
  --muted:    #B1B4B8;
  --border:   rgba(7,0,55,.08);
  --border2:  #E8E8F0;
  --secondary:#725BFF;
  --teal:     #77F5DF;
  --teal-bg:  #EEFFF5;
  --teal-text:#0F6E56;
  --purple-bg:#F0EEFF;
  --purple-text:#3E20FF;
  --shadow-sm:0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
  --shadow-md:0 4px 12px rgba(0,0,0,.08), 0 2px 4px rgba(0,0,0,.04);
  --radius:   8px;
  --mono:     'DM Mono', monospace;
}

/* reset */
*, *::before, *::after { box-sizing:border-box; font-family:'Inter',sans-serif !important; }
html, body, .main, .stApp { background:var(--bg-page) !important; }
.main .block-container { padding:1.75rem 2rem 4rem !important; max-width:1480px; }
p, span, div, label { color:var(--dark); }

/* ── SIDEBAR ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background:var(--bg-white) !important;
  border-right:1px solid var(--border2) !important;
  box-shadow:none !important;
}
[data-testid="stSidebar"] > div:first-child { padding:0 !important; overflow-x:hidden !important; }
[data-testid="stSidebar"] .block-container   { padding:0 !important; max-width:100% !important; }
[data-testid="stSidebarResizeHandle"] { display:none !important; }

/* padding on Streamlit's generated inner containers */
[data-testid="stSidebarContent"],
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
  padding-left:1.1rem !important;
  padding-right:1.1rem !important;
  padding-bottom:2rem !important;
}
[data-testid="stSidebar"] > div > div > div {
  padding-left:1.1rem !important;
  padding-right:1.1rem !important;
}

/* sidebar text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p { color:var(--dark) !important; font-size:13px !important; font-weight:400 !important; margin:0 !important; }
[data-testid="stSidebar"] [data-testid="stSlider"] p { font-size:11px !important; color:var(--muted) !important; }

/* sidebar selects — neutral bg, no heavy fill */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background:var(--bg-white) !important; border:1px solid var(--border2) !important; border-radius:var(--radius) !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span { color:var(--dark) !important; font-size:13px !important; }
[data-testid="stSidebar"] [data-baseweb="select"] svg  { fill:var(--muted) !important; }

/* active filter tags — soft bg #F8F2FF, accent text, small × — no heavy fill */
[data-testid="stSidebar"] [data-baseweb="tag"] {
  background:var(--bg-soft) !important; border:0.5px solid var(--secondary) !important; border-radius:5px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span { color:var(--accent) !important; font-size:11px !important; font-weight:500 !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] [role="presentation"] svg { fill:var(--secondary) !important; }
[data-testid="stSidebar"] [role="slider"]     { background:var(--accent) !important; }
[data-testid="stSidebar"] .stCheckbox label   { font-size:13px !important; color:var(--dark) !important; }
[data-testid="stSidebar"] .stToggle   label   { font-size:13px !important; color:var(--dark) !important; }

/* sidebar section headers — 11px uppercase #B1B4B8, no borders */
.sb-group-label {
  display:block; font-size:11px; font-weight:500; letter-spacing:.08em;
  text-transform:uppercase; color:var(--muted); margin:20px 0 6px; padding:0;
}
.sb-rule { border:none; border-top:1px solid var(--border2); margin:12px 0; }
.sb-subgroup { margin-left:0; }

/* ── HEADER ──────────────────────────────────────────────────────────────── */
.hdr { display:flex; align-items:center; justify-content:space-between;
       padding-bottom:.85rem; margin-bottom:1.25rem; border-bottom:1px solid var(--border2); }
.hdr-title { font-size:18px; font-weight:600; color:var(--dark); letter-spacing:-.02em; }
.hdr-sub   { font-size:12px; color:var(--muted); margin-left:10px; }

/* ── KPI CARDS ───────────────────────────────────────────────────────────── */
.kpi-row  { display:flex; gap:10px; margin-bottom:1.5rem; }
.kpi-card { flex:1; background:var(--bg-white); border:1px solid var(--border2);
            border-radius:12px; padding:16px 18px; box-shadow:var(--shadow-sm);
            display:flex; flex-direction:column; gap:3px; }
/* muted 12px label */
.kpi-label { font-size:11px; font-weight:400; color:var(--muted); text-transform:none; letter-spacing:0; }
/* 28px number — only place we go big */
.kpi-value { font-size:26px; font-weight:500; color:var(--dark); line-height:1.1;
             font-family:var(--mono) !important; letter-spacing:-.02em; }
/* 500 value — text KPI same size as others but non-mono */
.kpi-value.text { font-family:'Inter',sans-serif !important; font-size:15px; font-weight:500; line-height:1.3; }
/* small context string */
.kpi-sub  { font-size:12px; color:var(--muted); margin-top:2px; }
/* colored dot */
.kpi-dot  { display:inline-block; width:6px; height:6px; border-radius:50%;
            background:var(--accent); margin-right:5px; vertical-align:middle; }

/* ── SECTION LABEL ───────────────────────────────────────────────────────── */
.sec-label { font-size:12px; font-weight:500; color:var(--muted);
             margin:1.5rem 0 .6rem; display:block; }

/* ── TABLE ───────────────────────────────────────────────────────────────── */
.fmt-tbl-outer { background:var(--bg-white); border-radius:12px;
                 overflow:hidden; box-shadow:var(--shadow-sm); }
.fmt-tbl { width:100%; border-collapse:collapse; font-size:13px; }
/* sentence case, 12px, #B1B4B8, NO ALL CAPS */
.fmt-tbl th {
  padding:9px 14px; background:#FAFAFA;
  font-size:12px; font-weight:500; color:var(--muted);
  text-align:left; white-space:nowrap;
  border-bottom:1px solid var(--border2);
  letter-spacing:0; text-transform:none;
}
.fmt-tbl td { padding:9px 14px; border-bottom:1px solid #F2F2F8; vertical-align:middle; }
.fmt-tbl tbody tr:last-child td { border-bottom:none; }
.fmt-tbl tbody tr { cursor:pointer; transition:background .1s; }
/* alternating rows: white / #FAFAFA */
.fmt-tbl tbody tr:nth-child(even) td { background:#FAFAFA; }
/* hover: #F8F2FF, no border flash */
.fmt-tbl tbody tr:hover td { background:var(--bg-soft) !important; }
/* selected row */
.fmt-tbl tbody tr.sel td   { background:var(--bg-soft) !important; }
.fmt-tbl tbody tr.sel .fn  { color:var(--accent); font-weight:500; }

.fn  { font-size:13px; font-weight:400; color:var(--dark); line-height:1.2; }
.fid { font-size:11px; font-family:var(--mono); color:var(--muted); margin-top:1px; }

/* type tags: Видео = teal, Баннер = soft purple */
.tag     { display:inline-block; padding:2px 8px; border-radius:5px; font-size:11px;
           font-weight:500; margin:1px 2px 1px 0; background:#F2F2F8; color:var(--dark); }
.tag-v   { background:var(--teal-bg); color:var(--teal-text); }
.tag-b   { background:var(--purple-bg); color:var(--purple-text); }
/* CPM/CPC: small pill, #070037 10% opacity bg, text #070037 */
.tag-cpm { background:rgba(7,0,55,.07); color:var(--dark); border:none; font-size:11px; }
.tag-cpc { background:rgba(62,32,255,.08); color:var(--accent); font-size:11px; }

/* progress bars: filled #725BFF on track #F8F2FF, fixed 80px, numeric inline */
.bw { display:flex; align-items:center; gap:6px; }
.bb { width:80px; flex-shrink:0; height:4px; background:#EDEDF8; border-radius:2px; }
.bf { height:4px; border-radius:2px; background:var(--secondary); }
.bv { font-family:var(--mono); font-size:11px; color:var(--dark); white-space:nowrap; }

/* score */
.sc-pill { display:inline-flex; align-items:center; padding:2px 8px; border-radius:20px;
           font-size:11px; font-weight:500; font-family:var(--mono) !important; }
.sc-hi { background:var(--teal-bg); color:var(--teal-text); }
.sc-md { background:var(--purple-bg); color:var(--accent); }
.sc-lo { background:#F2F2F8; color:var(--muted); }

/* ── DETAIL PANEL (card) ─────────────────────────────────────────────────── */
.card {
  background:var(--bg-soft); border:1px solid var(--border2);
  border-left:3px solid var(--accent); border-radius:12px;
  padding:24px; margin-top:12px;
  box-shadow:var(--shadow-sm);
  animation:slideUp .16s ease both;
}
@keyframes slideUp { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)} }
.card-header { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:4px; }
/* card title 16px */
.card-title  { font-size:16px; font-weight:600; color:var(--dark); letter-spacing:-.01em; }
.card-meta   { font-size:11px; color:var(--muted); font-family:var(--mono) !important; margin-bottom:14px; }
.card-desc   { font-size:13px; color:var(--dark); line-height:1.65;
               background:var(--bg-white); padding:12px 14px; border-radius:var(--radius); margin-bottom:18px; }

/* CTA buttons — ghost style */
.card-links { display:flex; gap:6px; flex-wrap:wrap; }
.card-link  { font-size:12px; color:var(--accent); font-weight:500; text-decoration:none;
              padding:4px 10px; border-radius:6px; border:1px solid var(--accent);
              transition:all .12s; background:transparent; }
.card-link:hover { background:var(--accent); color:#fff; }

/* 3-col stat grid, white bg, radius 8 */
.metrics-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-bottom:20px; }
.metric-box  { background:var(--bg-white); border-radius:var(--radius); padding:11px 13px; }
.metric-lbl  { font-size:11px; font-weight:500; color:var(--muted); margin-bottom:5px; text-transform:none; }
.metric-val  { font-size:15px; font-weight:500; color:var(--dark); font-family:var(--mono) !important; line-height:1.1; }

.info-grid   { display:grid; grid-template-columns:1fr 1fr; gap:24px; margin-bottom:12px; }
/* section labels 11px uppercase */
.c-sec   { font-size:11px; font-weight:500; letter-spacing:.08em; text-transform:uppercase;
           color:var(--muted); margin:14px 0 6px; }
.info-row { display:flex; gap:8px; margin-bottom:5px; align-items:baseline; }
.info-lbl { font-size:13px; color:var(--muted); min-width:148px; flex-shrink:0; }
.info-val { font-size:13px; color:var(--dark); font-weight:500; }
.tags-row { display:flex; flex-wrap:wrap; gap:4px; margin-bottom:2px; }
.bool-y   { color:var(--accent); font-weight:500; font-size:13px; }
.bool-n   { color:#D0D0DC; font-size:13px; }

.terms-box { font-size:13px; color:var(--dark); line-height:1.65;
             background:var(--bg-white); padding:11px 14px; border-radius:var(--radius); margin-top:4px; }

.w-pill { display:inline-block; font-size:12px; font-weight:500;
          font-family:var(--mono) !important; padding:4px 12px; border-radius:6px; margin-top:6px; }
.w-ok  { background:var(--teal-bg); color:var(--teal-text); }
.w-bad { background:var(--purple-bg); color:var(--accent); }

.no-res { text-align:center; padding:56px 20px; color:var(--muted); font-size:13px;
          background:var(--bg-white); border-radius:12px; box-shadow:var(--shadow-sm); }

#MainMenu, footer, [data-testid="stToolbar"] { display:none !important; }
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
        raise FileNotFoundError(f"{a}/{b}")
    df = rc("DataLens_-_formats.csv", "DataLens - formats.csv")
    di = rc("DataLens_-_dict_items.csv", "DataLens - dict_items.csv")
    fi = None
    for n in ["DataLens_-_format_items.csv", "DataLens - format_items.csv"]:
        if os.path.exists(p(n)): fi = pd.read_csv(p(n)); break
    if fi is None and os.path.exists(p("DataLens.xlsx")):
        fi = pd.read_excel(p("DataLens.xlsx"), sheet_name="format_items")
    if fi is None: raise FileNotFoundError("format_items")
    m  = fi.merge(di[["dict_id","item_id","item_name"]], on=["dict_id","item_id"], how="left")
    pv = m.groupby(["format_id","dict_id"])["item_name"].apply(list).unstack("dict_id").reset_index()
    return df.merge(pv, on="format_id", how="left"), di

df, di = load_data()

SEASON = {"Январь":.80,"Февраль":1.,"Март":1.2,"Апрель":1.2,"Май":1.,
          "Июнь":1.,"Июль":1.,"Август":1.,"Сентябрь":1.25,
          "Октябрь":1.25,"Ноябрь":1.25,"Декабрь":1.25}

def sk(plat, mo): return SEASON.get(mo, 1.) if str(plat)=="Buzzoola" else 1.

def pct(v):
    try:
        f=float(v); assert not np.isnan(f)
        x=round(f*100,1)
        return (f"{int(x)}%" if x==int(x) else f"{x:.1f}%").replace(".",",")
    except: return "—"

def rub(v):
    try:
        f=float(v); assert not np.isnan(f)
        return f"{int(round(f)):,}\u202f₽".replace(",","\u202f")
    except: return "—"

def reach_s(v):
    try:
        f=float(v); assert not np.isnan(f)
        m=f/1e6
        if m>=1: return (f"{int(m)}M" if m==int(m) else f"{m:.1f}M").replace(".",",")
        return f"{int(f):,}".replace(",","\u202f")
    except: return "—"

def bv(v):
    try:
        if v is None or (isinstance(v,float) and np.isnan(v)):
            return '<span class="bool-n">—</span>'
    except: pass
    return ('<span class="bool-y">✓</span>' if str(v).upper() in ("TRUE","1")
            else '<span class="bool-n">—</span>')

def sv(v, d="—"):
    try:
        if v is None or (isinstance(v,float) and np.isnan(v)): return d
    except: pass
    s=str(v).strip(); return s if s else d

def th(cell):
    if not isinstance(cell,list) or not cell:
        return '<span style="color:#D0D0DC;font-size:11px">—</span>'
    return "".join(f'<span class="tag">{t}</span>' for t in cell if t)

def calc_ecpm(row):
    m=str(row.get("buy_model","CPM")).upper(); d=float(row.get("discount",0) or 0)
    try:
        if m=="CPM": raw=float(row.get("cpm_avg",np.nan))
        elif m=="CPC":
            a,b=float(row.get("cpc_avg",np.nan)),float(row.get("ctr_avg",np.nan))
            raw=a*b*1000 if not(np.isnan(a) or np.isnan(b) or b==0) else np.nan
        elif m=="CPV":
            a,b=float(row.get("cpv_avg",np.nan)),float(row.get("vtr_avg",np.nan))
            raw=a*b*1000 if not(np.isnan(a) or np.isnan(b) or b==0) else np.nan
        else: raw=float(row.get("cpm_avg",np.nan))
        return np.nan if np.isnan(raw) else raw*(1-d)
    except: return np.nan

df["ecpm_eff"] = df.apply(calc_ecpm, axis=1)
def opts(did): return di[di["dict_id"]==did]["item_name"].dropna().tolist()

# ─── SIDEBAR — 3 groups: Основные / Аудитория / Качество ─────────────────────
with st.sidebar:
    def grp(t): st.markdown(f'<span class="sb-group-label">{t}</span>', unsafe_allow_html=True)
    def rule():  st.markdown('<hr class="sb-rule">', unsafe_allow_html=True)

    # ── GROUP 1: Основные ──
    grp("Основные")
    format_types = st.multiselect("_ft", ["Видео","Баннер"], default=["Видео","Баннер"],
                                  placeholder="Тип формата", label_visibility="collapsed")
    devices      = st.multiselect("_dv", ["Desktop","Mobile Web","In-App","Smart TV"],
                                  default=["Desktop","Mobile Web","In-App","Smart TV"],
                                  placeholder="Устройство", label_visibility="collapsed")
    buy_models   = st.multiselect("_bm", ["CPM","CPC"], default=["CPM","CPC"],
                                  placeholder="Модель закупки", label_visibility="collapsed")

    show_b = not format_types or "Баннер" in format_types
    show_v = not format_types or "Видео"  in format_types
    if show_b:
        f_disp = st.multiselect("_db", opts("display"), default=[],
                                placeholder="Отображение", label_visibility="collapsed")
    else: f_disp=[]
    if show_v:
        f_plac = st.multiselect("_pl", opts("placement"), default=[],
                                placeholder="Плейсмент", label_visibility="collapsed")
        f_inst = st.multiselect("_in", opts("instream_pos"), default=[],
                                placeholder="Позиция", label_visibility="collapsed")
    else: f_plac=[]; f_inst=[]

    rule()
    # ── GROUP 2: Аудитория ──
    grp("Аудитория")
    f_targ = st.multiselect("_tr", opts("targeting"), default=[],
                             placeholder="Таргетинги", label_visibility="collapsed")
    f_dmp  = st.multiselect("_dp", opts("dmp"), default=[],
                             placeholder="DMP", label_visibility="collapsed")

    rule()
    # ── GROUP 3: Качество ──
    grp("Качество")
    req_px = st.checkbox("Верификация пикселем")
    req_js = st.checkbox("Верификация JS-тегом")
    req_bl = st.checkbox("Brand Lift")
    req_sl = st.checkbox("Sales Lift")

    # Secondary filters collapsed under "Пороговые значения"
    with st.expander("Пороговые значения"):
        max_ecpm_f = st.slider("Макс. eCPM (после скидки), ₽", 0, 1000, 1000, step=10)
        min_ctr    = st.slider("Мин. CTR, %",        0.0, 5.0, 0.0, step=0.1)
        min_rch    = st.slider("Мин. охват, млн",    0.0,80.0, 0.0, step=1.0)
        min_view   = st.slider("Мин. Viewability, %",  0, 100,   0, step=5)
        min_vtr    = st.slider("Мин. VTR, %",        0.0,100., 0.0, step=5.0)

    rule()
    scoring = st.toggle("Скоринг", value=False)
    if scoring:
        grp("Веса (сумма = 100)")
        wr=st.slider("Охват",0,100,20,step=5)
        we=st.slider("eCPM",0,100,20,step=5)
        wc=st.slider("CTR",0,100,20,step=5)
        wv=st.slider("VTR",0,100,15,step=5)
        wi=st.slider("Viewability",0,100,15,step=5)
        wm=st.slider("Комиссия",0,100,10,step=5)
        tw=wr+we+wc+wv+wi+wm
        st.markdown(f'<div class="w-pill {"w-ok" if tw==100 else "w-bad"}">Сумма: {tw}/100</div>',
                    unsafe_allow_html=True)
        norm=st.checkbox("Нормализовать", value=True)
    else: wr=we=wc=wv=wi=wm=tw=0; norm=False

    rule()
    grp("Сезонность")
    months=["Январь","Февраль","Март","Апрель","Май","Июнь",
            "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
    sel_m=st.selectbox("_mo", months, index=months.index("Март"), label_visibility="collapsed")

# ─── FILTER ───────────────────────────────────────────────────────────────────
def has(c,i): return isinstance(c,list) and any(x in c for x in i)
def all_in(c,i):
    if not i: return True
    return isinstance(c,list) and all(x in c for x in i)

F=df.copy()
if format_types: F=F[F["format_type"].apply(lambda x:has(x,format_types))]
if devices:      F=F[F["device"].apply(lambda x:has(x,devices))]
if buy_models:   F=F[F["buy_model"].isin(buy_models)]
if f_disp:  F=F[F["display"].apply(lambda x:all_in(x,f_disp))]
if f_plac:  F=F[F["placement"].apply(lambda x:all_in(x,f_plac))]
if f_inst:  F=F[F["instream_pos"].apply(lambda x:all_in(x,f_inst))]
if f_targ:  F=F[F["targeting"].apply(lambda x:all_in(x,f_targ))]
if f_dmp:   F=F[F["dmp"].apply(lambda x:all_in(x,f_dmp))]
if req_px: F=F[F["verification_pixel"].apply(lambda v:str(v).upper() in ("TRUE","1"))]
if req_js: F=F[F["verification_js"].apply(lambda v:str(v).upper() in ("TRUE","1"))]
if req_bl: F=F[F["bls"].apply(lambda v:str(v).upper() in ("TRUE","1"))]
if req_sl: F=F[F["sales_lift"].apply(lambda v:str(v).upper() in ("TRUE","1"))]
F=F[F["ecpm_eff"].fillna(9999)<=max_ecpm_f]
if min_ctr >0: F=F[F["ctr_avg"].fillna(0)        >=min_ctr/100]
if min_rch >0: F=F[F["max_reach"].fillna(0)       >=min_rch*1e6]
if min_view>0: F=F[F["viewability_avg"].fillna(0) >=min_view/100]
if min_vtr >0: F=F[F["vtr_avg"].fillna(0)         >=min_vtr/100]
F=F.copy()
F["_sk"]   = F["platform"].apply(lambda p:sk(p,sel_m))
F["ecpm_s"]= F["ecpm_eff"]*F["_sk"]

# ─── SCORING ──────────────────────────────────────────────────────────────────
def ncol(s,inv=False):
    mn,mx=s.min(),s.max()
    if mx==mn: return pd.Series([.5]*len(s),index=s.index)
    n=(s-mn)/(mx-mn); return 1-n if inv else n

if scoring and len(F)>0:
    W=dict(r=wr,e=we,c=wc,v=wv,i=wi,m=wm); t=sum(W.values())
    W={k:(v/t if norm and t>0 else v/100) for k,v in W.items()}
    ev_=F["ecpm_s"].max()*2 if F["ecpm_s"].notna().any() else 9999
    cv_=F["commission"].max() if F["commission"].notna().any() else 1
    F["score"]=(
        ncol(F["max_reach"].fillna(0))*W["r"]+
        ncol(F["ecpm_s"].fillna(ev_),True)*W["e"]+
        ncol(F["ctr_avg"].fillna(0))*W["c"]+
        ncol(F["vtr_avg"].fillna(0))*W["v"]+
        ncol(F["viewability_avg"].fillna(0))*W["i"]+
        ncol(F["commission"].fillna(cv_),True)*W["m"]
    )*100
    F=F.sort_values("score",ascending=False).reset_index(drop=True)
else:
    F["score"]=np.nan
    F=F.sort_values("ecpm_s",ascending=True,na_position="last").reset_index(drop=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="hdr">'
    '<div style="display:flex;align-items:baseline;gap:8px">'
    '<span class="hdr-title">Format Selector</span>'
    '<span class="hdr-sub">Анализ рекламных форматов</span>'
    '</div></div>',
    unsafe_allow_html=True)

# ─── KPI — 4 cards, colored dot as directional signal ─────────────────────────
top    = F.iloc[0] if len(F)>0 else None
avg_e  = F["ecpm_s"].mean() if len(F)>0 else np.nan
sk0    = float(F["_sk"].iloc[0]) if len(F)>0 else 1.
maxr   = F["max_reach"].max() if len(F)>0 else np.nan
lbl2   = "Лучший по скорингу" if scoring else "Самый дешевый eCPM"
top_nm = sv(top.get("format_name","—")) if top is not None else "—"
top_sb = (f'Скор: {top["score"]:.0f}' if scoring and top is not None and not pd.isna(top.get("score",np.nan))
          else sv(top.get("buy_model","—")) if top is not None else "")
sk0_d  = str(int(sk0)) if sk0==int(sk0) else f"{sk0:.1f}".replace(".",",")

st.markdown(
    f'<div class="kpi-row">'

    f'<div class="kpi-card">'
    f'<div class="kpi-label">Форматов после фильтров</div>'
    f'<div class="kpi-value">{len(F)}</div>'
    f'<div class="kpi-sub">из {len(df)} доступных</div></div>'

    f'<div class="kpi-card">'
    f'<div class="kpi-label">{lbl2}</div>'
    f'<div class="kpi-value text">{top_nm}</div>'
    f'<div class="kpi-sub">{top_sb}</div></div>'

    f'<div class="kpi-card">'
    f'<div class="kpi-label">Средний eCPM</div>'
    f'<div class="kpi-value">{rub(avg_e)}</div>'
    f'<div class="kpi-sub">{sel_m} · коэф. {sk0_d}×</div></div>'

    f'<div class="kpi-card">'
    f'<div class="kpi-label">Макс. охват</div>'
    f'<div class="kpi-value">{reach_s(maxr)}</div>'
    f'<div class="kpi-sub">среди отфильтрованных</div></div>'

    f'</div>',
    unsafe_allow_html=True)

# ─── TABLE ────────────────────────────────────────────────────────────────────
st.markdown('<span class="sec-label">Форматы</span>', unsafe_allow_html=True)

# Row selection via query params
qp = st.query_params
if "_row" in qp:
    try:
        ni = int(str(qp["_row"]))
        if st.session_state.get("_sel") != ni:
            st.session_state["_sel"] = ni
            st.rerun()
    except: pass

if len(F)==0:
    st.markdown('<div class="no-res">Нет форматов, соответствующих выбранным фильтрам.</div>',
                unsafe_allow_html=True)
else:
    max_r=max(float(df["max_reach"].max()),1.)
    max_c=max(float(df["ctr_avg"].max()),.001) if df["ctr_avg"].notna().any() else .05
    max_e=max(float(F["ecpm_s"].max()),1.)      if F["ecpm_s"].notna().any()   else 1.

    def type_tags(c):
        if not isinstance(c,list): return ""
        return "".join(f'<span class="tag {"tag-v" if t=="Видео" else "tag-b"}">{t}</span>' for t in c)

    def mtag(v):
        return f'<span class="tag {"tag-cpc" if str(v).upper()=="CPC" else "tag-cpm"}">{v}</span>'

    def dtags(c):
        if not isinstance(c,list): return '<span style="color:#D0D0DC">—</span>'
        return " ".join(f'<span class="tag">{d}</span>' for d in c)

    def bar(val, mx, label):
        if label=="—": return '<span style="color:#D0D0DC;font-size:11px">—</span>'
        try: pw=min(float(val)/float(mx)*100,100)
        except: pw=0
        return (f'<div class="bw"><div class="bb">'
                f'<div class="bf" style="width:{pw:.1f}%"></div></div>'
                f'<span class="bv">{label}</span></div>')

    def spill(s):
        try:
            v=float(s); assert not np.isnan(v)
            cls="sc-hi" if v>=65 else("sc-md" if v>=40 else "sc-lo")
            return f'<span class="sc-pill {cls}">{v:.0f}</span>'
        except: return ""

    sel_idx = st.session_state.get("_sel")
    last_hdr = "<th>Скор</th>" if scoring else "<th>eCPM (сез.)</th>"
    rows=""
    for i,(_,row) in enumerate(F.iterrows()):
        sc=" sel" if sel_idx==i else ""
        ltd = (spill(row.get("score",np.nan)) if scoring else
               f'<span style="font-family:var(--mono);font-size:12px">{rub(row.get("ecpm_s",np.nan))}</span>')
        rows+=(
            f'<tr class="{sc}" data-i="{i}">'
            f'<td><div class="fn">{row["format_name"]}</div><div class="fid">{row["format_id"]}</div></td>'
            f'<td>{type_tags(row.get("format_type",[]))}</td>'
            f'<td>{mtag(row["buy_model"])}</td>'
            f'<td>{dtags(row.get("device",[]))}</td>'
            f'<td>{bar(row.get("max_reach"),max_r,reach_s(row.get("max_reach")))}</td>'
            f'<td>{bar(row.get("ctr_avg"),max_c,pct(row.get("ctr_avg")))}</td>'
            f'<td>{bar(row.get("viewability_avg"),1.,pct(row.get("viewability_avg")))}</td>'
            f'<td>{ltd}</td></tr>'
        )

    st.markdown(
        f'<div class="fmt-tbl-outer"><table class="fmt-tbl"><thead><tr>'
        f'<th>Формат</th><th>Тип</th><th>Модель</th><th>Устройства</th>'
        f'<th>Охват</th><th>CTR</th><th>Viewability</th>{last_hdr}'
        f'</tr></thead><tbody>{rows}</tbody></table></div>',
        unsafe_allow_html=True)

    # JS click → query_params → rerun
    components.html("""<script>
(function() {
  function attach() {
    var rows = window.parent.document.querySelectorAll('.fmt-tbl tbody tr[data-i]');
    rows.forEach(function(tr) {
      if (tr._ok) return;
      tr._ok = true;
      tr.addEventListener('click', function() {
        var url = new URL(window.parent.location.href);
        url.searchParams.set('_row', tr.getAttribute('data-i'));
        window.parent.history.pushState({}, '', url.toString());
        window.parent.dispatchEvent(new PopStateEvent('popstate', {state:{}}));
      });
    });
  }
  attach();
  new MutationObserver(attach).observe(window.parent.document.body, {childList:true, subtree:true});
})();
</script>""", height=0, scrolling=False)

    # ─── DETAIL PANEL ─────────────────────────────────────────────────────────
    ci = st.session_state.get("_sel")
    if ci is not None and 0<=ci<len(F):
        r = F.iloc[ci]
        def gf(field, default=np.nan):
            val=r.get(field,default)
            if val is None: return default
            try:
                if isinstance(val,float) and np.isnan(val): return default
            except: pass
            return val

        ee=gf("ecpm_eff"); es2=gf("ecpm_s"); sc_=gf("_sk",1.)
        try:
            f_=float(sc_)
            scd=str(int(f_)) if f_==int(f_) else f"{f_:.1f}".replace(".",",")
        except: scd="1"

        sbadge=""
        if scoring:
            try:
                sv_=float(gf("score",np.nan))
                if not np.isnan(sv_):
                    cls_="sc-hi" if sv_>=65 else("sc-md" if sv_>=40 else "sc-lo")
                    sbadge=f'<span class="sc-pill {cls_}" style="margin-left:10px">{sv_:.0f}</span>'
            except: pass

        links=""
        for lbl_,uk in [("Пример","example_url"),("Техтребования","technical_requirements_url"),
                         ("Медиакит","mediakit_url"),("Кейсы","cases_url")]:
            v=gf(uk,"")
            if isinstance(v,str) and v.startswith("http"):
                links+=f'<a class="card-link" href="{v}" target="_blank">{lbl_} ↗</a>'

        grid=(
            f'<div class="metric-box"><div class="metric-lbl">eCPM факт</div><div class="metric-val">{rub(ee)}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">eCPM сезон. {scd}×</div><div class="metric-val">{rub(es2)}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">Скидка</div><div class="metric-val">{pct(gf("discount"))}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">Охват макс.</div><div class="metric-val">{reach_s(gf("max_reach"))}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">CTR среднее</div><div class="metric-val">{pct(gf("ctr_avg"))}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">VTR среднее</div><div class="metric-val">{pct(gf("vtr_avg"))}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">Viewability</div><div class="metric-val">{pct(gf("viewability_avg"))}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">Комиссия</div><div class="metric-val">{pct(gf("commission"))}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">Мин. бюджет</div><div class="metric-val">{rub(gf("min_budget"))}</div></div>'
        )
        il=(
            '<div class="c-sec">Ценовой диапазон</div>'
            f'<div class="info-row"><span class="info-lbl">CPM мин / сред / макс</span>'
            f'<span class="info-val">{rub(gf("cpm_min"))} / {rub(gf("cpm_avg"))} / {rub(gf("cpm_max"))}</span></div>'
            f'<div class="info-row"><span class="info-lbl">CPC мин / сред / макс</span>'
            f'<span class="info-val">{rub(gf("cpc_min"))} / {rub(gf("cpc_avg"))} / {rub(gf("cpc_max"))}</span></div>'
            f'<div class="info-row"><span class="info-lbl">CTR мин / макс</span>'
            f'<span class="info-val">{pct(gf("ctr_min"))} / {pct(gf("ctr_max"))}</span></div>'
            '<div class="c-sec">Верификация</div>'
            f'<div class="info-row"><span class="info-lbl">Пиксель</span><span class="info-val">{bv(gf("verification_pixel"))}</span></div>'
            f'<div class="info-row"><span class="info-lbl">JS-тег</span><span class="info-val">{bv(gf("verification_js"))}</span></div>'
            '<div class="c-sec">Исследования</div>'
            f'<div class="info-row"><span class="info-lbl">Brand Lift</span><span class="info-val">{bv(gf("bls"))}</span></div>'
            f'<div class="info-row"><span class="info-lbl">Sales Lift</span><span class="info-val">{bv(gf("sales_lift"))}</span></div>'
        )
        ir=(
            '<div class="c-sec">Плейсмент</div><div class="tags-row">'+th(gf("placement",[]))+'</div>'
            '<div class="c-sec">Устройства</div><div class="tags-row">'+th(gf("device",[]))+'</div>'
            '<div class="c-sec">Отображение</div><div class="tags-row">'+th(gf("display",[]))+'</div>'
            '<div class="c-sec">DMP</div><div class="tags-row">'+th(gf("dmp",[]))+'</div>'
            '<div class="c-sec">Производство</div><div class="tags-row">'+th(gf("production",[]))+'</div>'
        )

        terms=""
        for tlbl,tkey in [("Условия Brand Lift","bls_terms"),("Условия Sales Lift","sales_lift_terms"),
                           ("Условия сезонности","seasonality_terms")]:
            v=gf(tkey,"")
            if isinstance(v,str) and v.strip():
                terms+=f'<div class="c-sec">{tlbl}</div><div class="terms-box">{v}</div>'

        st.markdown(
            '<div class="card">'
            '<div class="card-header">'
            f'<div><div class="card-title">{sv(gf("format_name"))}{sbadge}</div>'
            f'<div class="card-meta">{sv(gf("format_id"))} · {sv(gf("buy_model"))} · {sv(gf("platform"))}</div></div>'
            +(f'<div class="card-links">{links}</div>' if links else '')+
            '</div>'
            f'<div class="card-desc">{sv(gf("description"),"Описание не указано")}</div>'
            f'<div class="metrics-grid">{grid}</div>'
            f'<div class="info-grid"><div>{il}</div><div>{ir}</div></div>'
            '<div class="c-sec">Таргетинг</div><div class="tags-row">'+th(gf("targeting",[]))+'</div>'
            '<div class="c-sec">Наценки за таргетинг</div><div class="tags-row">'+th(gf("targeting_markup",[]))+'</div>'
            +terms+
            '</div>',
            unsafe_allow_html=True)

# ─── CHARTS at bottom ─────────────────────────────────────────────────────────
if len(F)>0:
    st.markdown('<span class="sec-label">Аналитика</span>', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        cdf=F[F["ecpm_s"].notna()].sort_values("ecpm_s",ascending=False).head(12)
        if len(cdf)>0:
            cp=cdf.sort_values("ecpm_s"); n=len(cp)
            clrs=[f"rgba(114,91,255,{.3+.7*i/max(n-1,1):.2f})" for i in range(n)]
            fig1=go.Figure(go.Bar(
                x=cp["ecpm_s"].round(0), y=cp["format_name"], orientation="h",
                marker_color=clrs, marker_line_width=0,
                text=cp["ecpm_s"].round(0).astype(int).astype(str)+" ₽",
                textposition="outside", textfont=dict(size=9,color="#B1B4B8"),
                hovertemplate="<b>%{y}</b><br>eCPM: <b>%{x:.0f} ₽</b><extra></extra>"))
            fig1.update_layout(
                title=dict(text="eCPM по форматам, ₽",font=dict(size=11,color="#B1B4B8",family="Inter")),
                height=max(260,n*30+60), margin=dict(l=0,r=65,t=36,b=4),
                paper_bgcolor="#FFFFFF", plot_bgcolor="#F8F2FF",
                xaxis=dict(gridcolor="#F0EBF8",gridwidth=0.5,tickfont_size=10,
                           tickfont_color="#B1B4B8",zeroline=False,title=None),
                yaxis=dict(tickfont_size=11,tickfont_color="#070037",title=None,tickmode="linear"),
                font_family="Inter", bargap=0.3)
            st.plotly_chart(fig1,use_container_width=True,config={"displayModeBar":False})
    with c2:
        sdf=F[F["ecpm_s"].notna()&F["ctr_avg"].notna()].copy()
        if len(sdf)>=2:
            med=float(sdf["max_reach"].median()) if sdf["max_reach"].notna().any() else 1e6
            sdf["bsz"]=sdf["max_reach"].fillna(med).apply(lambda v:max(8,min(34,float(v)/2e6)))
            fig2=go.Figure()
            for _,row in sdf.iterrows():
                fig2.add_trace(go.Scatter(
                    x=[float(row["ctr_avg"])*100], y=[float(row["ecpm_s"])],
                    mode="markers+text",
                    marker=dict(size=row["bsz"],color="#725BFF",opacity=.7,
                                line=dict(color="white",width=1.5)),
                    text=[row["format_name"]], textposition="top center",
                    textfont=dict(size=9,color="#B1B4B8"),
                    hovertemplate=(
                        f"<b>{row['format_name']}</b><br>"
                        f"CTR: <b>{float(row['ctr_avg'])*100:.2f}%</b><br>"
                        f"eCPM: <b>{float(row['ecpm_s']):.0f} ₽</b><br>"
                        f"Охват: {reach_s(row.get('max_reach'))}<extra></extra>"),
                    showlegend=False))
            fig2.update_layout(
                title=dict(text="CTR vs eCPM",font=dict(size=11,color="#B1B4B8",family="Inter")),
                height=max(260,len(sdf)*30+60), margin=dict(l=0,r=10,t=36,b=4),
                paper_bgcolor="#FFFFFF", plot_bgcolor="#F8F2FF",
                xaxis=dict(title="CTR, %",gridcolor="#F0EBF8",gridwidth=0.5,tickfont_size=10,title_font_size=10,
                           tickfont_color="#B1B4B8",title_font_color="#B1B4B8",zeroline=False),
                yaxis=dict(title="eCPM, ₽",gridcolor="#F0EBF8",gridwidth=0.5,tickfont_size=10,title_font_size=10,
                           tickfont_color="#B1B4B8",title_font_color="#B1B4B8",zeroline=False),
                font_family="Inter")
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
