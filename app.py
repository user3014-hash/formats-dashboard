import streamlit as st
import streamlit.components.v1 as components
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
  --white:#FFFFFF; --mint:#C0FFD9; --blue:#3E20FF; --indigo:#725BFF;
  --bg:#F8F2FF; --dark:#070037; --muted:rgba(7,0,55,0.42); --border:rgba(7,0,55,0.10);
}
*,*::before,*::after { font-family:'DM Sans',sans-serif !important; box-sizing:border-box; }
html,body,.main { background:var(--bg) !important; }
.main .block-container { padding:1.5rem 2rem 3rem !important; max-width:1440px; }

/* ── SIDEBAR: white bg, structured like the dark version but inverted ── */
[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: none !important;
    min-width: 220px !important;
}
[data-testid="stSidebar"] > div:first-child { padding:0 !important; overflow-x:hidden !important; }
[data-testid="stSidebar"] .block-container  { padding:0 !important; max-width:100% !important; }
[data-testid="stSidebarResizeHandle"] { display:none !important; }

/* All sidebar text */
[data-testid="stSidebar"] label { color:var(--dark) !important; font-size:13px !important; font-weight:400 !important; }
[data-testid="stSidebar"] p     { color:var(--dark) !important; font-size:13px !important; margin:0 !important; line-height:1.4 !important; }

/* Multiselect controls */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background:var(--bg) !important; border:1px solid var(--border) !important; border-radius:7px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span { color:var(--dark) !important; font-size:13px !important; }
[data-testid="stSidebar"] [data-baseweb="select"] svg  { fill:var(--muted) !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] { background:var(--blue) !important; border:none !important; border-radius:5px !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] span { color:#fff !important; font-size:11px !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] [role="presentation"] svg { fill:rgba(255,255,255,.7) !important; }
[data-testid="stSidebar"] [role="slider"] { background:var(--blue) !important; }
[data-testid="stSidebar"] .stCheckbox label { font-size:13px !important; color:var(--dark) !important; }

/* Sidebar layout classes */
.sb-head  { padding:.9rem 1rem .85rem; border-bottom:1px solid var(--border); }
.sb-brand { font-size:14px; font-weight:600; color:var(--dark); line-height:1.3; }
.sb-sub   { font-size:11px; color:var(--muted); margin-top:2px; }
.sb-body  { padding:0 1rem 2rem; }
.sb-sec   { font-size:9px; font-weight:700; letter-spacing:.12em; text-transform:uppercase;
            color:var(--muted); display:block; margin:13px 0 3px; }
.sb-rule  { border:none; border-top:1px solid var(--border); margin:10px 0; }

/* ── Header ── */
.hdr { display:flex; align-items:center; justify-content:space-between;
       padding-bottom:.9rem; margin-bottom:1.1rem; border-bottom:1px solid var(--border); }
.hdr-l { display:flex; align-items:baseline; gap:10px; }
.hdr-t { font-size:1.1rem; font-weight:600; color:var(--dark); letter-spacing:-.02em; }
.hdr-s { font-size:11.5px; color:var(--muted); font-family:'DM Mono',monospace !important; }
.hdr-badge { font-size:9px; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
             background:var(--mint); color:var(--dark); padding:3px 10px; border-radius:20px; }

/* ── KPI ── */
.kpi-row  { display:flex; gap:10px; margin-bottom:1.2rem; align-items:stretch; }
.kpi-card { flex:1; background:var(--white); border:1px solid var(--border);
            border-top:2px solid var(--blue); border-radius:11px; padding:14px 16px;
            display:flex; flex-direction:column; justify-content:space-between; min-height:86px; }
.kpi-card.mint { border-top-color:var(--mint); }
.kpi-lbl { font-size:10px; color:var(--muted); font-weight:500; margin-bottom:5px; }
.kpi-val { font-size:1.35rem; font-weight:600; color:var(--dark);
           font-family:'DM Mono',monospace !important; letter-spacing:-.02em; line-height:1.1; }
.kpi-sm  { font-size:.85rem; font-weight:600; color:var(--dark); line-height:1.35; }
.kpi-sub { font-size:10px; color:var(--muted); margin-top:3px; }
.slabel  { font-size:9px; font-weight:700; letter-spacing:.11em; text-transform:uppercase;
           color:var(--muted); margin:1.2rem 0 .4rem; display:block; }

/* ── Card ── */
.card { background:var(--white); border:1px solid var(--border); border-left:3px solid var(--blue);
        border-radius:12px; padding:22px; margin-top:0;
        animation:fadeIn .18s ease both; }
@keyframes fadeIn { from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:translateY(0)} }
.card-top  { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:3px; }
.card-ttl  { font-size:1rem; font-weight:600; color:var(--dark); letter-spacing:-.01em; }
.card-meta { font-family:'DM Mono',monospace !important; font-size:10.5px; color:var(--muted); margin-bottom:11px; }
.card-desc { font-size:13px; color:var(--dark); line-height:1.6; padding:10px 13px;
             background:var(--bg); border-radius:8px; margin-bottom:14px; }
.c-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-bottom:14px; }
.c-m    { background:var(--bg); border-radius:8px; padding:10px 12px; }
.c-lbl  { font-size:9px; color:var(--muted); font-weight:700; text-transform:uppercase;
          letter-spacing:.08em; margin-bottom:4px; }
.c-val  { font-size:.975rem; font-weight:600; color:var(--dark); font-family:'DM Mono',monospace !important; }
.c-sec  { font-size:9px; font-weight:700; letter-spacing:.10em; text-transform:uppercase;
          color:var(--muted); margin:12px 0 5px; }
.info-row { display:flex; gap:8px; margin-bottom:4px; }
.info-lbl { font-size:12px; color:var(--muted); min-width:158px; flex-shrink:0; }
.info-val { font-size:12px; color:var(--dark); font-weight:500; }
.tags-row { display:flex; flex-wrap:wrap; gap:4px; }
.bool-y   { color:var(--blue); font-weight:700; }
.bool-n   { color:rgba(7,0,55,.18); }
.link-a   { font-size:12px; color:var(--blue); text-decoration:none; margin-right:12px; font-weight:500; }
.tag      { display:inline-block; padding:2px 7px; border-radius:4px; font-size:11px; font-weight:500;
            margin:1px 2px 1px 0; background:rgba(62,32,255,.08); color:var(--dark); }
.tag-v    { background:rgba(192,255,217,.65); color:#055c30; }
.tag-b    { background:rgba(114,91,255,.12); color:#4433bb; }
.tag-cpm  { background:transparent; color:var(--dark); border:1px solid var(--border); }
.tag-cpc  { background:rgba(62,32,255,.10); color:var(--blue); }
.sc-pill  { display:inline-flex; align-items:center; padding:2px 7px; border-radius:20px;
            font-size:11px; font-weight:600; font-family:'DM Mono',monospace !important; }
.sc-hi { background:var(--mint); color:#055c30; }
.sc-md { background:rgba(62,32,255,.09); color:var(--blue); }
.sc-lo { background:var(--bg); color:var(--muted); }
.w-wrap { display:inline-block; font-size:12px; font-weight:600;
          font-family:'DM Mono',monospace !important; padding:4px 11px; border-radius:7px; margin:5px 0 2px; }
.w-ok  { background:var(--mint); color:#055c30; }
.w-bad { background:rgba(62,32,255,.09); color:var(--indigo); }
.no-res { text-align:center; padding:48px 20px; color:var(--muted);
          background:var(--white); border:1px solid var(--border); border-radius:11px; font-size:13px; }

/* ── HTML Table ── */
.fmt-wrap { border:1px solid var(--border); border-radius:11px; overflow:hidden; background:var(--white); }
.fmt-tbl  { width:100%; border-collapse:collapse; font-size:12.5px; }
.fmt-tbl th { padding:8px 12px; background:var(--bg); border-bottom:1px solid var(--border);
              font-size:9px; font-weight:700; letter-spacing:.09em; text-transform:uppercase;
              color:var(--muted); white-space:nowrap; text-align:left; }
.fmt-tbl td { padding:9px 12px; border-bottom:1px solid rgba(7,0,55,.05); vertical-align:middle; }
.fmt-tbl tbody tr:last-child td { border-bottom:none; }
.fmt-tbl tbody tr { cursor:pointer; transition:background .1s; }
.fmt-tbl tbody tr:hover td { background:rgba(62,32,255,.04); }
.fmt-tbl tbody tr.sel td   { background:rgba(62,32,255,.07) !important; }
.fmt-tbl tbody tr.sel .fn  { color:var(--blue); }
.fn  { font-weight:500; font-size:13px; color:var(--dark); }
.fid { font-family:'DM Mono',monospace; font-size:10px; color:var(--muted); margin-top:1px; }
.bar-wrap { display:flex; align-items:center; gap:5px; }
.bar-bg   { height:4px; flex:1; min-width:36px; background:rgba(7,0,55,.08); border-radius:3px; }
.bar-fill { height:4px; border-radius:3px; background:var(--blue); }
.bar-val  { font-family:'DM Mono',monospace; font-size:11px; color:var(--dark);
            min-width:36px; text-align:right; white-space:nowrap; }
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
    merged = fi.merge(di[["dict_id","item_id","item_name"]], on=["dict_id","item_id"], how="left")
    pivot  = merged.groupby(["format_id","dict_id"])["item_name"].apply(list).unstack("dict_id").reset_index()
    return df.merge(pivot, on="format_id", how="left"), di

df, di = load_data()

SEASON = {"Январь":0.80,"Февраль":1.00,"Март":1.20,"Апрель":1.20,"Май":1.00,
          "Июнь":1.00,"Июль":1.00,"Август":1.00,"Сентябрь":1.25,
          "Октябрь":1.25,"Ноябрь":1.25,"Декабрь":1.25}

def sk(platform, month): return SEASON.get(month, 1.0) if str(platform)=="Buzzoola" else 1.0

def pct(v):
    try:
        f=float(v); assert not np.isnan(f)
        x=round(f*100,1)
        return (f"{int(x)}%" if x==int(x) else f"{x:.1f}%").replace(".",",")
    except: return "—"

def rub(v):
    try:
        f=float(v); assert not np.isnan(f)
        return f"{int(round(f)):,} ₽".replace(",","\u202f")
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
        if v is None or (isinstance(v,float) and np.isnan(v)): return '<span class="bool-n">—</span>'
    except: pass
    return ('<span class="bool-y">✓</span>' if str(v).upper() in ("TRUE","1")
            else '<span class="bool-n">—</span>')

def sv(v, d="—"):
    try:
        if v is None or (isinstance(v,float) and np.isnan(v)): return d
    except: pass
    s=str(v).strip(); return s if s else d

def thtml(cell):
    if not isinstance(cell,list) or not cell:
        return '<span style="color:rgba(7,0,55,.16);font-size:11px">—</span>'
    return "".join(f'<span class="tag">{t}</span>' for t in cell if t)

def calc_ecpm(row):
    m=str(row.get("buy_model","CPM")).upper(); d=float(row.get("discount",0) or 0)
    try:
        if m=="CPM": raw=float(row.get("cpm_avg",np.nan))
        elif m=="CPC":
            cpc,ct=float(row.get("cpc_avg",np.nan)),float(row.get("ctr_avg",np.nan))
            raw=cpc*ct*1000 if not(np.isnan(cpc) or np.isnan(ct) or ct==0) else np.nan
        elif m=="CPV":
            cpv,vt=float(row.get("cpv_avg",np.nan)),float(row.get("vtr_avg",np.nan))
            raw=cpv*vt*1000 if not(np.isnan(cpv) or np.isnan(vt) or vt==0) else np.nan
        else: raw=float(row.get("cpm_avg",np.nan))
        return np.nan if np.isnan(raw) else raw*(1-d)
    except: return np.nan

df["ecpm_eff"] = df.apply(calc_ecpm, axis=1)
def opts(did): return di[di["dict_id"]==did]["item_name"].dropna().tolist()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-head"><div class="sb-brand">Format Selector</div>'
                '<div class="sb-sub">Анализ рекламных форматов</div></div>'
                '<div class="sb-body">', unsafe_allow_html=True)

    def sec(t): st.markdown(f'<span class="sb-sec">{t}</span>', unsafe_allow_html=True)
    def rule():  st.markdown('<hr class="sb-rule">', unsafe_allow_html=True)

    sec("Тип формата")
    format_types = st.multiselect("_ft", ["Видео","Баннер"], default=["Видео","Баннер"],
                                  placeholder="Все типы", label_visibility="collapsed")
    sec("Устройство")
    devices = st.multiselect("_dv", ["Desktop","Mobile Web","In-App","Smart TV"],
                              default=["Desktop","Mobile Web","In-App","Smart TV"],
                              placeholder="Все устройства", label_visibility="collapsed")
    sec("Модель закупки")
    buy_models = st.multiselect("_bm", ["CPM","CPC"], default=["CPM","CPC"],
                                placeholder="Все модели", label_visibility="collapsed")

    show_b = not format_types or "Баннер" in format_types
    show_v = not format_types or "Видео"  in format_types

    if show_b:
        sec("Отображение")
        f_disp = st.multiselect("_db", opts("display"), default=[],
                                placeholder="Все варианты", label_visibility="collapsed")
    else: f_disp=[]
    if show_v:
        sec("Плейсмент")
        f_plac = st.multiselect("_pl", opts("placement"), default=[],
                                placeholder="Все плейсменты", label_visibility="collapsed")
        sec("Позиция")
        f_inst = st.multiselect("_in", opts("instream_pos"), default=[],
                                placeholder="Все позиции", label_visibility="collapsed")
    else: f_plac=[]; f_inst=[]

    sec("Таргетинги")
    f_targ = st.multiselect("_tr", opts("targeting"), default=[],
                             placeholder="Все таргетинги", label_visibility="collapsed")
    sec("DMP")
    f_dmp = st.multiselect("_dp", opts("dmp"), default=[],
                            placeholder="Все DMP", label_visibility="collapsed")
    rule()
    sec("Дополнительно")
    req_px = st.checkbox("Верификация пикселем")
    req_js = st.checkbox("Верификация JS-тегом")
    req_bl = st.checkbox("Brand Lift")
    req_sl = st.checkbox("Sales Lift")
    rule()
    sec("Пороговые значения")
    max_ecpm_f = st.slider("Макс. eCPM (после скидки), ₽", 0, 1000, 1000, step=10)
    min_ctr    = st.slider("Мин. CTR, %",        0.0, 5.0, 0.0, step=0.1)
    min_rch    = st.slider("Мин. охват, млн",    0.0,80.0, 0.0, step=1.0)
    min_view   = st.slider("Мин. Viewability, %",  0, 100,   0, step=5)
    min_vtr    = st.slider("Мин. VTR, %",        0.0,100., 0.0, step=5.0)
    rule()
    scoring = st.toggle("Включить скоринг", value=False)
    if scoring:
        sec("Веса (сумма = 100)")
        wr=st.slider("Охват",0,100,20,step=5); we=st.slider("eCPM (ниже — лучше)",0,100,20,step=5)
        wc=st.slider("CTR",0,100,20,step=5);   wv=st.slider("VTR",0,100,15,step=5)
        wi=st.slider("Viewability",0,100,15,step=5); wm=st.slider("Комиссия (ниже — лучше)",0,100,10,step=5)
        tw=wr+we+wc+wv+wi+wm
        st.markdown(f'<div class="w-wrap {"w-ok" if tw==100 else "w-bad"}">Сумма: {tw} / 100</div>',
                    unsafe_allow_html=True)
        norm=st.checkbox("Нормализовать веса", value=True)
    else: wr=we=wc=wv=wi=wm=tw=0; norm=False
    rule()
    sec("Сезонность")
    months=["Январь","Февраль","Март","Апрель","Май","Июнь",
            "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
    sel_m=st.selectbox("_mo", months, index=months.index("Март"), label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── FILTER + SCORING ─────────────────────────────────────────────────────────
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

def ncol(s,inv=False):
    mn,mx=s.min(),s.max()
    if mx==mn: return pd.Series([0.5]*len(s),index=s.index)
    n=(s-mn)/(mx-mn); return 1-n if inv else n

if scoring and len(F)>0:
    W=dict(r=wr,e=we,c=wc,v=wv,i=wi,m=wm); t=sum(W.values())
    if norm and t>0: W={k:v/t for k,v in W.items()}
    else: W={k:v/100 for k,v in W.items()}
    ev_=F["ecpm_s"].max()*2 if F["ecpm_s"].notna().any() else 9999
    cv_=F["commission"].max() if F["commission"].notna().any() else 1
    F["score"]=(
        ncol(F["max_reach"].fillna(0))*W["r"]+
        ncol(F["ecpm_s"].fillna(ev_),inv=True)*W["e"]+
        ncol(F["ctr_avg"].fillna(0))*W["c"]+
        ncol(F["vtr_avg"].fillna(0))*W["v"]+
        ncol(F["viewability_avg"].fillna(0))*W["i"]+
        ncol(F["commission"].fillna(cv_),inv=True)*W["m"]
    )*100
    F=F.sort_values("score",ascending=False).reset_index(drop=True)
else:
    F["score"]=np.nan
    F=F.sort_values("ecpm_s",ascending=True,na_position="last").reset_index(drop=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
n_plat=df["platform"].nunique()
badge=f"{n_plat} {'площадка' if n_plat==1 else ('площадки' if n_plat<5 else 'площадок')} · бета"
st.markdown(
    f'<div class="hdr"><div class="hdr-l"><span class="hdr-t">Format Selector</span>'
    f'<span class="hdr-s">Анализ рекламных форматов</span></div>'
    f'<span class="hdr-badge">{badge}</span></div>', unsafe_allow_html=True)

# ─── KPI ──────────────────────────────────────────────────────────────────────
top=F.iloc[0] if len(F)>0 else None
avg_e=F["ecpm_s"].mean() if len(F)>0 else np.nan
sk0=float(F["_sk"].iloc[0]) if len(F)>0 else 1.0
maxr=F["max_reach"].max() if len(F)>0 else np.nan
lbl2="Лучший по скорингу" if scoring else "Самый дешевый eCPM"
if top is not None:
    sub2=(f'Скор: {top["score"]:.0f}' if scoring and not pd.isna(top.get("score",np.nan))
          else sv(top.get("buy_model","—")))
    val2=f'<div class="kpi-sm">{sv(top.get("format_name","—"))}</div>'
else: sub2=""; val2='<div class="kpi-val">—</div>'
st.markdown(
    f'<div class="kpi-row">'
    f'<div class="kpi-card"><div><div class="kpi-lbl">Форматов после фильтров</div>'
    f'<div class="kpi-val">{len(F)}</div></div><div class="kpi-sub">из {len(df)} доступных</div></div>'
    f'<div class="kpi-card"><div><div class="kpi-lbl">{lbl2}</div>{val2}</div>'
    f'<div class="kpi-sub">{sub2}</div></div>'
    f'<div class="kpi-card"><div><div class="kpi-lbl">Средний eCPM (с сезонностью)</div>'
    f'<div class="kpi-val">{rub(avg_e)}</div></div><div class="kpi-sub">{sel_m} · коэф. {sk0}×</div></div>'
    f'<div class="kpi-card mint"><div><div class="kpi-lbl">Макс. охват</div>'
    f'<div class="kpi-val">{reach_s(maxr)}</div></div><div class="kpi-sub">среди отфильтрованных</div></div>'
    f'</div>', unsafe_allow_html=True)

# ─── CHARTS ───────────────────────────────────────────────────────────────────
if len(F)>0:
    ch1,ch2=st.columns(2)
    with ch1:
        cdf=F[F["ecpm_s"].notna()].sort_values("ecpm_s",ascending=False).head(12)
        if len(cdf)>0:
            cp=cdf.sort_values("ecpm_s"); n=len(cp)
            clrs=[f"rgba(62,32,255,{0.28+0.72*i/max(n-1,1):.2f})" for i in range(n)]
            fig1=go.Figure(go.Bar(
                x=cp["ecpm_s"].round(0), y=cp["format_name"], orientation="h",
                marker_color=clrs, marker_line_width=0,
                text=cp["ecpm_s"].round(0).astype(int).astype(str)+" ₽",
                textposition="outside", textfont=dict(size=9,color="rgba(7,0,55,.4)"),
                hovertemplate="<b>%{y}</b><br>eCPM: <b>%{x:.0f} ₽</b><extra></extra>"))
            fig1.update_layout(
                title=dict(text="eCPM по форматам (₽, с сезонностью)",font=dict(size=10,color="rgba(7,0,55,.42)")),
                height=max(280,n*32+60),margin=dict(l=0,r=65,t=36,b=4),
                paper_bgcolor="white",plot_bgcolor="white",
                xaxis=dict(gridcolor="rgba(7,0,55,.06)",tickfont_size=9,tickfont_color="rgba(7,0,55,.35)",zeroline=False,title=None),
                yaxis=dict(tickfont_size=10.5,tickfont_color="#070037",title=None,tickmode="linear"),
                font_family="DM Sans",bargap=0.28)
            st.plotly_chart(fig1,use_container_width=True,config={"displayModeBar":False})
    with ch2:
        sdf=F[F["ecpm_s"].notna()&F["ctr_avg"].notna()].copy()
        if len(sdf)>=2:
            med=float(sdf["max_reach"].median()) if sdf["max_reach"].notna().any() else 1e6
            sdf["bsz"]=sdf["max_reach"].fillna(med).apply(lambda v:max(8,min(34,float(v)/2e6)))
            fig2=go.Figure()
            for _,row in sdf.iterrows():
                fig2.add_trace(go.Scatter(
                    x=[float(row["ctr_avg"])*100],y=[float(row["ecpm_s"])],
                    mode="markers+text",
                    marker=dict(size=row["bsz"],color="#725BFF",opacity=0.75,line=dict(color="white",width=1.5)),
                    text=[row["format_name"]],textposition="top center",
                    textfont=dict(size=8,color="rgba(7,0,55,.55)"),
                    hovertemplate=(f"<b>{row['format_name']}</b><br>CTR: <b>{float(row['ctr_avg'])*100:.2f}%</b><br>"
                                   f"eCPM: <b>{float(row['ecpm_s']):.0f} ₽</b><br>Охват: {reach_s(row.get('max_reach'))}<extra></extra>"),
                    showlegend=False))
            fig2.update_layout(
                title=dict(text="CTR vs eCPM (размер — охват)",font=dict(size=10,color="rgba(7,0,55,.42)")),
                height=max(280,len(sdf)*32+60),margin=dict(l=0,r=10,t=36,b=4),
                paper_bgcolor="white",plot_bgcolor="white",
                xaxis=dict(title="CTR, %",gridcolor="rgba(7,0,55,.06)",tickfont_size=9,title_font_size=9,
                           tickfont_color="rgba(7,0,55,.35)",title_font_color="rgba(7,0,55,.35)",zeroline=False),
                yaxis=dict(title="eCPM, ₽",gridcolor="rgba(7,0,55,.06)",tickfont_size=9,title_font_size=9,
                           tickfont_color="rgba(7,0,55,.35)",title_font_color="rgba(7,0,55,.35)",zeroline=False),
                font_family="DM Sans")
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

# ─── TABLE with click-to-expand card ─────────────────────────────────────────
st.markdown('<span class="slabel">Форматы</span>', unsafe_allow_html=True)

if len(F)==0:
    st.markdown('<div class="no-res">Нет форматов, соответствующих фильтрам.</div>',
                unsafe_allow_html=True)
else:
    max_r=max(float(df["max_reach"].max()),1.0)
    max_c=max(float(df["ctr_avg"].max()),0.001) if df["ctr_avg"].notna().any() else 0.05
    max_e=max(float(F["ecpm_s"].max()),1.0) if F["ecpm_s"].notna().any() else 1.0

    def type_tags(cell):
        if not isinstance(cell,list): return ""
        return "".join(f'<span class="tag {"tag-v" if t=="Видео" else "tag-b"}">{t}</span>' for t in cell)

    def model_tag(v):
        return f'<span class="tag {"tag-cpc" if str(v).upper()=="CPC" else "tag-cpm"}">{v}</span>'

    def dev_tags(cell):
        if not isinstance(cell,list): return '<span style="color:rgba(7,0,55,.18)">—</span>'
        return " ".join(f'<span class="tag">{d}</span>' for d in cell)

    def bar(val, mx, label):
        if label=="—": return '<span style="color:rgba(7,0,55,.18);font-size:11px">—</span>'
        try: pw=min(float(val)/float(mx)*100,100)
        except: pw=0
        return (f'<div class="bar-wrap"><div class="bar-bg">'
                f'<div class="bar-fill" style="width:{pw:.1f}%"></div></div>'
                f'<span class="bar-val">{label}</span></div>')

    def spill(s):
        try:
            v=float(s); assert not np.isnan(v)
            cls="sc-hi" if v>=65 else ("sc-md" if v>=40 else "sc-lo")
            return f'<span class="sc-pill {cls}">{v:.0f}</span>'
        except: return ""

    sel_idx=st.session_state.get("_sel",None)
    last_hdr="<th>Скор</th>" if scoring else "<th>eCPM (сез.)</th>"

    rows=""
    for i,(_, row) in enumerate(F.iterrows()):
        sc=" sel" if sel_idx==i else ""
        last_td=(spill(row.get("score",np.nan)) if scoring else
                 f'<span style="font-family:DM Mono,monospace;font-size:12px">{rub(row.get("ecpm_s",np.nan))}</span>')
        rows+=(
            f'<tr class="{sc}" data-i="{i}">'
            f'<td><div class="fn">{row["format_name"]}</div><div class="fid">{row["format_id"]}</div></td>'
            f'<td>{type_tags(row.get("format_type",[]))}</td>'
            f'<td>{model_tag(row["buy_model"])}</td>'
            f'<td>{dev_tags(row.get("device",[]))}</td>'
            f'<td>{bar(row.get("max_reach"),max_r,reach_s(row.get("max_reach")))}</td>'
            f'<td>{bar(row.get("ctr_avg"),max_c,pct(row.get("ctr_avg")))}</td>'
            f'<td>{bar(row.get("viewability_avg"),1.0,pct(row.get("viewability_avg")))}</td>'
            f'<td>{last_td}</td></tr>'
        )

    # Render table + invisible iframe click bridge
    table_html = (
        f'<div class="fmt-wrap"><table class="fmt-tbl"><thead><tr>'
        f'<th>Формат</th><th>Тип</th><th>Модель</th><th>Устройства</th>'
        f'<th>Охват</th><th>CTR</th><th>Viewability</th>{last_hdr}'
        f'</tr></thead><tbody>{rows}</tbody></table></div>'
    )
    st.markdown(table_html, unsafe_allow_html=True)

    # Click bridge: tiny iframe captures row click, sends index via query param
    n_rows = len(F)
    click_bridge = f"""
    <iframe id="click-bridge" style="display:none;width:0;height:0;border:none;position:absolute"></iframe>
    <script>
    (function() {{
        function attachClicks() {{
            var rows = window.parent.document.querySelectorAll('.fmt-tbl tbody tr');
            if (!rows.length) {{ setTimeout(attachClicks, 200); return; }}
            rows.forEach(function(tr) {{
                if (tr.dataset.attached) return;
                tr.dataset.attached = "1";
                tr.addEventListener('click', function() {{
                    var idx = tr.getAttribute('data-i');
                    // Use Streamlit's built-in query params mechanism
                    var url = new URL(window.parent.location.href);
                    url.searchParams.set('_row', idx);
                    window.parent.history.replaceState(null, '', url.toString());
                    // Trigger rerun by clicking a hidden button
                    var btn = window.parent.document.querySelector('[data-testid="stButton"] button.row-trigger');
                    if (btn) btn.click();
                }});
            }});
        }}
        attachClicks();
        var obs = new MutationObserver(attachClicks);
        obs.observe(window.parent.document.body, {{childList:true, subtree:true}});
    }})();
    </script>
    """

    # Read row index from query params (set by JS above)
    qp = st.query_params
    if "_row" in qp:
        try:
            new_idx = int(qp["_row"])
            if new_idx != st.session_state.get("_sel"):
                st.session_state["_sel"] = new_idx
        except: pass

    # Hidden trigger button (clicked by JS to force rerun)
    col_hidden = st.columns([1])[0]
    with col_hidden:
        if st.button("·", key="row_trigger", help="",
                     type="secondary"):
            pass  # rerun happens automatically

    # Inject JS bridge
    components.html(click_bridge, height=0)

    # Inject CSS to hide the trigger button
    st.markdown("""
    <style>
    [data-testid="stButton"]:has(.row-trigger) { display:none !important; }
    div[data-testid="column"]:has(button[kind="secondary"][data-testid="baseButton-secondary"]) { display:none !important; }
    </style>
    """, unsafe_allow_html=True)

    # ─── CARD ─────────────────────────────────────────────────────────────────
    ci=st.session_state.get("_sel",None)
    if ci is not None and 0<=ci<len(F):
        r=F.iloc[ci]
        def gf(field,default=np.nan):
            val=r.get(field,default)
            if val is None: return default
            try:
                if isinstance(val,float) and np.isnan(val): return default
            except: pass
            return val

        ee=gf("ecpm_eff"); es2=gf("ecpm_s"); sc_=gf("_sk",1.0)
        try:
            sc_f=float(sc_)
            sc_d=str(int(sc_f)) if sc_f==int(sc_f) else f"{sc_f:.1f}".replace(".",",")
        except: sc_d="1"

        score_badge=""
        if scoring:
            try:
                sv_=float(gf("score",np.nan))
                if not np.isnan(sv_):
                    cls_="sc-hi" if sv_>=65 else("sc-md" if sv_>=40 else "sc-lo")
                    score_badge=f'<span class="sc-pill {cls_}" style="margin-left:8px">{sv_:.0f}</span>'
            except: pass

        links_html=""
        for lbl_,uk in [("Пример","example_url"),("Техтребования","technical_requirements_url"),
                         ("Медиакит","mediakit_url"),("Кейсы","cases_url")]:
            v=gf(uk,"")
            if isinstance(v,str) and v.startswith("http"):
                links_html+=f'<a class="link-a" href="{v}" target="_blank">{lbl_} ↗</a>'

        ecpm_lbl=f"eCPM (сезон. {sc_d}×)"
        grid_html=(
            f'<div class="c-m"><div class="c-lbl">eCPM (факт)</div><div class="c-val">{rub(ee)}</div></div>'
            f'<div class="c-m"><div class="c-lbl">{ecpm_lbl}</div><div class="c-val">{rub(es2)}</div></div>'
            f'<div class="c-m"><div class="c-lbl">Скидка</div><div class="c-val">{pct(gf("discount"))}</div></div>'
            f'<div class="c-m"><div class="c-lbl">Охват (макс.)</div><div class="c-val">{reach_s(gf("max_reach"))}</div></div>'
            f'<div class="c-m"><div class="c-lbl">CTR (среднее)</div><div class="c-val">{pct(gf("ctr_avg"))}</div></div>'
            f'<div class="c-m"><div class="c-lbl">VTR (среднее)</div><div class="c-val">{pct(gf("vtr_avg"))}</div></div>'
            f'<div class="c-m"><div class="c-lbl">Viewability</div><div class="c-val">{pct(gf("viewability_avg"))}</div></div>'
            f'<div class="c-m"><div class="c-lbl">Комиссия</div><div class="c-val">{pct(gf("commission"))}</div></div>'
            f'<div class="c-m"><div class="c-lbl">Мин. бюджет</div><div class="c-val">{rub(gf("min_budget"))}</div></div>'
        )
        info_left=(
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
        info_right=(
            '<div class="c-sec">Плейсмент</div><div class="tags-row">'+thtml(gf("placement",[]))+'</div>'
            '<div class="c-sec">Устройства</div><div class="tags-row">'+thtml(gf("device",[]))+'</div>'
            '<div class="c-sec">Отображение</div><div class="tags-row">'+thtml(gf("display",[]))+'</div>'
            '<div class="c-sec">DMP</div><div class="tags-row">'+thtml(gf("dmp",[]))+'</div>'
            '<div class="c-sec">Производство</div><div class="tags-row">'+thtml(gf("production",[]))+'</div>'
        )
        st.markdown(
            '<div class="card">'
            '<div class="card-top">'
            f'<div><div class="card-ttl">{sv(gf("format_name"))}{score_badge}</div>'
            f'<div class="card-meta">{sv(gf("format_id"))} · {sv(gf("buy_model"))} · {sv(gf("platform"))}</div></div>'
            +(f'<div>{links_html}</div>' if links_html else '')+
            '</div>'
            f'<div class="card-desc">{sv(gf("description"),"Описание не указано")}</div>'
            f'<div class="c-grid">{grid_html}</div>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'
            f'<div>{info_left}</div><div>{info_right}</div></div>'
            '<div class="c-sec">Таргетинг</div><div class="tags-row">'+thtml(gf("targeting",[]))+'</div>'
            '<div class="c-sec">Наценки за таргетинг</div><div class="tags-row">'+thtml(gf("targeting_markup",[]))+'</div>'
            '</div>', unsafe_allow_html=True)

        for lbl_,key in [("Условия Brand Lift","bls_terms"),("Условия Sales Lift","sales_lift_terms"),
                          ("Условия сезонности","seasonality_terms")]:
            v=gf(key,"")
            if isinstance(v,str) and v.strip():
                with st.expander("📋 "+lbl_):
                    st.markdown(f'<p style="font-size:13px;line-height:1.65">{v}</p>',unsafe_allow_html=True)
