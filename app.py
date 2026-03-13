import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Format Selector", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

# ─── DESIGN SYSTEM ────────────────────────────────────────────────────────────
# Typography: 3 levels only
#   Display  — 22px / 600  → titles, KPI numbers
#   Body     — 13px / 400  → text, table, card content
#   Label    — 10px / 700  → uppercase section headers, meta
# Colors: --white --mint --blue --indigo --bg --dark --muted --border
# Numbers always in DM Mono

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=DM+Mono:wght@400;500&display=swap');

:root {
  --white:#FFFFFF;
  --mint:#C0FFD9;
  --blue:#3E20FF;
  --indigo:#725BFF;
  --bg:#F8F2FF;
  --dark:#070037;
  --muted:rgba(7,0,55,.42);
  --border:rgba(7,0,55,.09);
  --shadow:0 1px 3px rgba(7,0,55,.06);
}

/* ── reset ── */
*,*::before,*::after { box-sizing:border-box; font-family:'DM Sans',sans-serif !important; }
html,body,.main,.stApp { background:var(--bg) !important; }
.main .block-container { padding:2rem 2.5rem 4rem !important; max-width:1480px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background:var(--white) !important;
  border-right:1px solid var(--border) !important;
  box-shadow:none !important;
}
[data-testid="stSidebar"] > div:first-child {
  padding:0 !important;
  overflow-x:hidden !important;
}
[data-testid="stSidebar"] .block-container {
  padding:0 !important; max-width:100% !important;
}
[data-testid="stSidebarResizeHandle"] { display:none !important; }

/* sidebar controls */
[data-testid="stSidebar"] label {
  color:var(--dark) !important; font-size:13px !important;
  font-weight:400 !important; line-height:1.45 !important;
}
[data-testid="stSidebar"] p {
  color:var(--dark) !important; font-size:13px !important; margin:0 !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] p {
  font-size:10px !important; color:var(--muted) !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background:var(--bg) !important;
  border:1px solid var(--border) !important;
  border-radius:8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span {
  color:var(--dark) !important; font-size:13px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] svg { fill:var(--muted) !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] {
  background:var(--blue) !important; border:none !important; border-radius:5px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span { color:#fff !important; font-size:11px !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] [role="presentation"] svg { fill:rgba(255,255,255,.7) !important; }
[data-testid="stSidebar"] [role="slider"] { background:var(--blue) !important; }
[data-testid="stSidebar"] .stCheckbox label { font-size:13px !important; color:var(--dark) !important; }
[data-testid="stSidebar"] .stToggle label  { font-size:13px !important; color:var(--dark) !important; }

/* Sidebar layout */
.sb-body  { padding:0 1.25rem 2.5rem; }
.sb-rule  { border:none; border-top:1px solid var(--border); margin:14px 0; }
.sb-sec   {
  display:block; font-size:10px !important; font-weight:700; letter-spacing:.11em;
  text-transform:uppercase; color:var(--muted) !important; margin:16px 0 5px;
}

/* ── HEADER ── */
.hdr { display:flex; align-items:center; justify-content:space-between;
       padding-bottom:1rem; margin-bottom:1.4rem; border-bottom:1px solid var(--border); }
.hdr-title { font-size:18px; font-weight:600; color:var(--dark); letter-spacing:-.03em; }
.hdr-sub   { font-size:10px; color:var(--muted); font-family:'DM Mono',monospace !important;
             letter-spacing:.04em; margin-left:10px; }

/* ── KPI cards ── */
.kpi-row  { display:flex; gap:12px; margin-bottom:1.5rem; }
.kpi-card { flex:1; background:var(--white); border:1px solid var(--border);
            border-radius:12px; padding:16px 18px;
            display:flex; flex-direction:column; gap:4px;
            box-shadow:var(--shadow); }
.kpi-label { font-size:10px; font-weight:700; letter-spacing:.08em;
             text-transform:uppercase; color:var(--muted); }
.kpi-value { font-size:22px; font-weight:600; color:var(--dark); line-height:1.1;
             font-family:'DM Mono',monospace !important; letter-spacing:-.03em; }
.kpi-value.text { font-family:'DM Sans',sans-serif !important; font-size:15px; line-height:1.3; }
.kpi-sub   { font-size:10px; color:var(--muted); margin-top:1px; }

/* ── Section label ── */
.sec-label { font-size:10px; font-weight:700; letter-spacing:.10em;
             text-transform:uppercase; color:var(--muted);
             margin:1.8rem 0 .7rem; display:block; }

/* ── Table (no outer border, clean rows) ── */
.fmt-tbl-outer { background:var(--white); border-radius:12px;
                 overflow:hidden; box-shadow:var(--shadow); }
.fmt-tbl { width:100%; border-collapse:collapse; font-size:13px; }
.fmt-tbl thead tr { background:var(--bg); }
.fmt-tbl th {
  padding:9px 14px;
  font-size:10px; font-weight:700; letter-spacing:.09em;
  text-transform:uppercase; color:var(--muted);
  text-align:left; white-space:nowrap;
  border-bottom:1px solid var(--border);
}
.fmt-tbl td {
  padding:10px 14px;
  border-bottom:1px solid rgba(7,0,55,.045);
  vertical-align:middle;
}
.fmt-tbl tbody tr:last-child td { border-bottom:none; }
.fmt-tbl tbody tr { cursor:pointer; transition:background .1s; }
.fmt-tbl tbody tr:hover td { background:rgba(62,32,255,.035); }
.fmt-tbl tbody tr.sel td   { background:rgba(62,32,255,.065) !important; }
.fmt-tbl tbody tr.sel .fn  { color:var(--blue); }

.fn  { font-size:13px; font-weight:500; color:var(--dark); line-height:1.2; }
.fid { font-size:10px; font-family:'DM Mono',monospace; color:var(--muted); margin-top:2px; }

/* tags */
.tag { display:inline-block; padding:2px 7px; border-radius:5px; font-size:11px;
       font-weight:500; margin:1px 2px 1px 0;
       background:rgba(62,32,255,.08); color:var(--dark); }
.tag-v   { background:rgba(192,255,217,.7); color:#055c30; }
.tag-b   { background:rgba(114,91,255,.11); color:#3d2faa; }
.tag-cpm { border:1px solid var(--border); background:transparent; color:var(--muted); }
.tag-cpc { background:rgba(62,32,255,.09); color:var(--blue); }

/* bar */
.bw { display:flex; align-items:center; gap:6px; }
.bb { flex:1; min-width:32px; height:4px; background:rgba(7,0,55,.08); border-radius:2px; }
.bf { height:4px; border-radius:2px; background:var(--blue); }
.bv { font-family:'DM Mono',monospace; font-size:10px; color:var(--dark);
      min-width:32px; text-align:right; white-space:nowrap; }

/* score pill */
.sc-pill { display:inline-flex; align-items:center; padding:2px 8px; border-radius:20px;
           font-size:11px; font-weight:600; font-family:'DM Mono',monospace !important; }
.sc-hi { background:var(--mint); color:#055c30; }
.sc-md { background:rgba(62,32,255,.09); color:var(--blue); }
.sc-lo { background:rgba(7,0,55,.06); color:var(--muted); }

/* ── CARD ── */
.card {
  background:var(--white); border:1px solid var(--border);
  border-left:3px solid var(--blue); border-radius:12px;
  padding:24px; margin-top:16px; box-shadow:var(--shadow);
  animation:slideUp .18s ease both;
}
@keyframes slideUp {
  from { opacity:0; transform:translateY(6px); }
  to   { opacity:1; transform:translateY(0); }
}
.card-header { display:flex; align-items:flex-start;
               justify-content:space-between; margin-bottom:5px; }
.card-title  { font-size:16px; font-weight:600; color:var(--dark); letter-spacing:-.02em; }
.card-meta   { font-size:10px; color:var(--muted);
               font-family:'DM Mono',monospace !important;
               letter-spacing:.04em; margin-bottom:14px; }
.card-desc   { font-size:13px; color:var(--dark); line-height:1.65;
               background:var(--bg); padding:12px 14px; border-radius:8px;
               margin-bottom:18px; }
.card-links  { display:flex; gap:2px; flex-wrap:wrap; }
.card-link   { font-size:12px; color:var(--blue); font-weight:500;
               text-decoration:none; padding:3px 8px; border-radius:5px;
               border:1px solid rgba(62,32,255,.15);
               transition:background .1s; }
.card-link:hover { background:rgba(62,32,255,.07); }

.metrics-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-bottom:20px; }
.metric-box  { background:var(--bg); border-radius:9px; padding:11px 13px; }
.metric-lbl  { font-size:10px; font-weight:700; text-transform:uppercase;
               letter-spacing:.08em; color:var(--muted); margin-bottom:5px; }
.metric-val  { font-size:15px; font-weight:600; color:var(--dark);
               font-family:'DM Mono',monospace !important; line-height:1.1; }

.info-grid   { display:grid; grid-template-columns:1fr 1fr; gap:24px; margin-bottom:12px; }
.c-sec   { font-size:10px; font-weight:700; letter-spacing:.10em; text-transform:uppercase;
           color:var(--muted); margin:14px 0 6px; }
.info-row { display:flex; gap:8px; margin-bottom:5px; align-items:baseline; }
.info-lbl { font-size:13px; color:var(--muted); min-width:148px; flex-shrink:0; }
.info-val { font-size:13px; color:var(--dark); font-weight:500; }
.tags-row { display:flex; flex-wrap:wrap; gap:4px; margin-bottom:2px; }
.bool-y   { color:var(--blue); font-weight:600; font-size:13px; }
.bool-n   { color:rgba(7,0,55,.16); font-size:13px; }

.terms-box { font-size:13px; color:var(--dark); line-height:1.65;
             background:var(--bg); padding:11px 14px; border-radius:8px;
             margin-top:4px; }

/* scoring weight indicator */
.w-pill { display:inline-block; font-size:12px; font-weight:600;
          font-family:'DM Mono',monospace !important; padding:4px 12px;
          border-radius:7px; margin-top:6px; }
.w-ok  { background:var(--mint); color:#055c30; }
.w-bad { background:rgba(62,32,255,.09); color:var(--indigo); }

.no-res { text-align:center; padding:56px 20px; color:var(--muted);
          font-size:13px; background:var(--white); border-radius:12px;
          box-shadow:var(--shadow); }

/* hide Streamlit chrome we don't need */
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
    m = fi.merge(di[["dict_id","item_id","item_name"]], on=["dict_id","item_id"], how="left")
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
        return '<span style="color:rgba(7,0,55,.14);font-size:10px">—</span>'
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

df["ecpm_eff"]=df.apply(calc_ecpm,axis=1)
def opts(did): return di[di["dict_id"]==did]["item_name"].dropna().tolist()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Padding injected here via HTML — Streamlit can't be blocked from
    # resetting its own .block-container padding, so we wrap in a div
    st.markdown('<div class="sb-body">', unsafe_allow_html=True)

    def sec(t): st.markdown(f'<span class="sb-sec">{t}</span>', unsafe_allow_html=True)
    def rule():  st.markdown('<hr class="sb-rule">', unsafe_allow_html=True)

    sec("Тип формата")
    format_types=st.multiselect("_ft",["Видео","Баннер"],default=["Видео","Баннер"],
                                placeholder="Все типы",label_visibility="collapsed")
    sec("Устройство")
    devices=st.multiselect("_dv",["Desktop","Mobile Web","In-App","Smart TV"],
                           default=["Desktop","Mobile Web","In-App","Smart TV"],
                           placeholder="Все устройства",label_visibility="collapsed")
    sec("Модель закупки")
    buy_models=st.multiselect("_bm",["CPM","CPC"],default=["CPM","CPC"],
                              placeholder="Все модели",label_visibility="collapsed")

    show_b=not format_types or "Баннер" in format_types
    show_v=not format_types or "Видео"  in format_types
    if show_b:
        sec("Отображение")
        f_disp=st.multiselect("_db",opts("display"),default=[],
                              placeholder="Все варианты",label_visibility="collapsed")
    else: f_disp=[]
    if show_v:
        sec("Плейсмент")
        f_plac=st.multiselect("_pl",opts("placement"),default=[],
                              placeholder="Все плейсменты",label_visibility="collapsed")
        sec("Позиция")
        f_inst=st.multiselect("_in",opts("instream_pos"),default=[],
                              placeholder="Все позиции",label_visibility="collapsed")
    else: f_plac=[]; f_inst=[]
    sec("Таргетинги")
    f_targ=st.multiselect("_tr",opts("targeting"),default=[],
                          placeholder="Все таргетинги",label_visibility="collapsed")
    sec("DMP")
    f_dmp=st.multiselect("_dp",opts("dmp"),default=[],
                         placeholder="Все DMP",label_visibility="collapsed")
    rule()
    sec("Дополнительно")
    req_px=st.checkbox("Верификация пикселем")
    req_js=st.checkbox("Верификация JS-тегом")
    req_bl=st.checkbox("Brand Lift")
    req_sl=st.checkbox("Sales Lift")
    rule()
    sec("Пороговые значения")
    max_ecpm_f=st.slider("Макс. eCPM (после скидки), ₽",0,1000,1000,step=10)
    min_ctr   =st.slider("Мин. CTR, %",0.0,5.0,0.0,step=0.1)
    min_rch   =st.slider("Мин. охват, млн",0.0,80.0,0.0,step=1.0)
    min_view  =st.slider("Мин. Viewability, %",0,100,0,step=5)
    min_vtr   =st.slider("Мин. VTR, %",0.0,100.,0.0,step=5.0)
    rule()
    scoring=st.toggle("Включить скоринг",value=False)
    if scoring:
        sec("Веса (сумма = 100)")
        wr=st.slider("Охват",0,100,20,step=5)
        we=st.slider("eCPM (ниже — лучше)",0,100,20,step=5)
        wc=st.slider("CTR",0,100,20,step=5)
        wv=st.slider("VTR",0,100,15,step=5)
        wi=st.slider("Viewability",0,100,15,step=5)
        wm=st.slider("Комиссия (ниже — лучше)",0,100,10,step=5)
        tw=wr+we+wc+wv+wi+wm
        st.markdown(f'<div class="w-pill {"w-ok" if tw==100 else "w-bad"}">Сумма: {tw}/100</div>',
                    unsafe_allow_html=True)
        norm=st.checkbox("Нормализовать веса",value=True)
    else: wr=we=wc=wv=wi=wm=tw=0; norm=False
    rule()
    sec("Сезонность")
    months=["Январь","Февраль","Март","Апрель","Май","Июнь",
            "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
    sel_m=st.selectbox("_mo",months,index=months.index("Март"),label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

# Inject sidebar padding fix via components — runs in parent frame context
components.html("""
<script>
(function patchSidebar() {
  var sb = window.parent.document.querySelector('[data-testid="stSidebar"] .block-container');
  if (!sb) { setTimeout(patchSidebar, 100); return; }
  sb.style.setProperty('padding', '0', 'important');
  var wrap = window.parent.document.querySelector('.sb-body');
  if (wrap) wrap.style.setProperty('padding', '0 1.25rem 2.5rem', 'important');
})();
</script>
""", height=0, scrolling=False)

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
F["_sk"]=F["platform"].apply(lambda p:sk(p,sel_m))
F["ecpm_s"]=F["ecpm_eff"]*F["_sk"]

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
    '<div style="display:flex;align-items:baseline;gap:10px">'
    '<span class="hdr-title">Format Selector</span>'
    '<span class="hdr-sub">Анализ рекламных форматов</span>'
    '</div></div>',
    unsafe_allow_html=True)

# ─── KPI ──────────────────────────────────────────────────────────────────────
top=F.iloc[0] if len(F)>0 else None
avg_e=F["ecpm_s"].mean() if len(F)>0 else np.nan
sk0=float(F["_sk"].iloc[0]) if len(F)>0 else 1.
maxr=F["max_reach"].max() if len(F)>0 else np.nan
lbl2="Лучший по скорингу" if scoring else "Самый дешевый eCPM"
top_name=sv(top.get("format_name","—")) if top is not None else "—"
top_sub=(f'Скор: {top["score"]:.0f}' if scoring and top is not None and not pd.isna(top.get("score",np.nan))
         else sv(top.get("buy_model","—")) if top is not None else "")
sk0_d=str(int(sk0)) if sk0==int(sk0) else f"{sk0:.1f}".replace(".",",")

st.markdown(
    f'<div class="kpi-row">'
    f'<div class="kpi-card">'
    f'<div class="kpi-label">Форматов после фильтров</div>'
    f'<div class="kpi-value">{len(F)}</div>'
    f'<div class="kpi-sub">из {len(df)} доступных</div></div>'

    f'<div class="kpi-card">'
    f'<div class="kpi-label">{lbl2}</div>'
    f'<div class="kpi-value text">{top_name}</div>'
    f'<div class="kpi-sub">{top_sub}</div></div>'

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

# Handle row selection via query params (set by JS click handler)
qp=st.query_params
if "_row" in qp:
    try:
        ni=int(str(qp["_row"]))
        if st.session_state.get("_sel")!=ni:
            st.session_state["_sel"]=ni
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
        if not isinstance(c,list): return '<span style="color:rgba(7,0,55,.14)">—</span>'
        return " ".join(f'<span class="tag">{d}</span>' for d in c)
    def bar(val,mx,label):
        if label=="—": return '<span style="color:rgba(7,0,55,.18);font-size:10px">—</span>'
        try: pw=min(float(val)/float(mx)*100,100)
        except: pw=0
        return (f'<div class="bw"><div class="bb"><div class="bf" style="width:{pw:.1f}%"></div></div>'
                f'<span class="bv">{label}</span></div>')
    def spill(s):
        try:
            v=float(s); assert not np.isnan(v)
            cls="sc-hi" if v>=65 else("sc-md" if v>=40 else "sc-lo")
            return f'<span class="sc-pill {cls}">{v:.0f}</span>'
        except: return ""

    sel_idx=st.session_state.get("_sel")
    last_hdr="<th>Скор</th>" if scoring else "<th>eCPM (сез.)</th>"
    rows=""
    for i,(_,row) in enumerate(F.iterrows()):
        sc=" sel" if sel_idx==i else ""
        ltd=(spill(row.get("score",np.nan)) if scoring else
             f'<span style="font-family:DM Mono,monospace;font-size:12px">{rub(row.get("ecpm_s",np.nan))}</span>')
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

    # JS click → query param → rerun (no extra UI)
    components.html("""
<script>
(function() {
  function attach() {
    var rows = window.parent.document.querySelectorAll('.fmt-tbl tbody tr[data-i]');
    rows.forEach(function(tr) {
      if (tr._ok) return;
      tr._ok = true;
      tr.addEventListener('click', function() {
        var idx = tr.getAttribute('data-i');
        var url = new URL(window.parent.location.href);
        url.searchParams.set('_row', idx);
        window.parent.history.pushState({}, '', url.toString());
        window.parent.dispatchEvent(new PopStateEvent('popstate', {state:{}}));
      });
    });
  }
  attach();
  new MutationObserver(attach).observe(
    window.parent.document.body, {childList:true, subtree:true}
  );
})();
</script>
""", height=0, scrolling=False)

    # ─── CARD ─────────────────────────────────────────────────────────────────
    ci=st.session_state.get("_sel")
    if ci is not None and 0<=ci<len(F):
        r=F.iloc[ci]
        def gf(field,default=np.nan):
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
            f'<div class="metric-box"><div class="metric-lbl">eCPM (факт)</div><div class="metric-val">{rub(ee)}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">eCPM (сезон. {scd}×)</div><div class="metric-val">{rub(es2)}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">Скидка</div><div class="metric-val">{pct(gf("discount"))}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">Охват (макс.)</div><div class="metric-val">{reach_s(gf("max_reach"))}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">CTR (среднее)</div><div class="metric-val">{pct(gf("ctr_avg"))}</div></div>'
            f'<div class="metric-box"><div class="metric-lbl">VTR (среднее)</div><div class="metric-val">{pct(gf("vtr_avg"))}</div></div>'
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

        # Terms inline
        terms=""
        for tlbl,tkey in [("Условия Brand Lift","bls_terms"),
                           ("Условия Sales Lift","sales_lift_terms"),
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
            clrs=[f"rgba(62,32,255,{.28+.72*i/max(n-1,1):.2f})" for i in range(n)]
            fig1=go.Figure(go.Bar(
                x=cp["ecpm_s"].round(0), y=cp["format_name"], orientation="h",
                marker_color=clrs, marker_line_width=0,
                text=cp["ecpm_s"].round(0).astype(int).astype(str)+" ₽",
                textposition="outside", textfont=dict(size=9,color="rgba(7,0,55,.38)"),
                hovertemplate="<b>%{y}</b><br>eCPM: <b>%{x:.0f} ₽</b><extra></extra>"))
            fig1.update_layout(
                title=dict(text="eCPM по форматам, ₽ (с сезонностью)",
                           font=dict(size=10,color="rgba(7,0,55,.4)")),
                height=max(260,n*30+60), margin=dict(l=0,r=65,t=36,b=4),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(gridcolor="rgba(7,0,55,.055)",tickfont_size=9,
                           tickfont_color="rgba(7,0,55,.3)",zeroline=False,title=None),
                yaxis=dict(tickfont_size=10,tickfont_color="#070037",title=None,tickmode="linear"),
                font_family="DM Sans", bargap=0.3)
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
                    marker=dict(size=row["bsz"],color="#725BFF",opacity=.72,
                                line=dict(color="white",width=1.5)),
                    text=[row["format_name"]], textposition="top center",
                    textfont=dict(size=8,color="rgba(7,0,55,.5)"),
                    hovertemplate=(
                        f"<b>{row['format_name']}</b><br>"
                        f"CTR: <b>{float(row['ctr_avg'])*100:.2f}%</b><br>"
                        f"eCPM: <b>{float(row['ecpm_s']):.0f} ₽</b><br>"
                        f"Охват: {reach_s(row.get('max_reach'))}<extra></extra>"),
                    showlegend=False))
            fig2.update_layout(
                title=dict(text="CTR vs eCPM (размер пузыря — охват)",
                           font=dict(size=10,color="rgba(7,0,55,.4)")),
                height=max(260,len(sdf)*30+60), margin=dict(l=0,r=10,t=36,b=4),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(title="CTR, %",gridcolor="rgba(7,0,55,.055)",tickfont_size=9,
                           title_font_size=9,tickfont_color="rgba(7,0,55,.3)",
                           title_font_color="rgba(7,0,55,.3)",zeroline=False),
                yaxis=dict(title="eCPM, ₽",gridcolor="rgba(7,0,55,.055)",tickfont_size=9,
                           title_font_size=9,tickfont_color="rgba(7,0,55,.3)",
                           title_font_color="rgba(7,0,55,.3)",zeroline=False),
                font_family="DM Sans")
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
