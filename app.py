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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --white:  #FFFFFF;
    --mint:   #C0FFD9;
    --blue:   #3E20FF;
    --indigo: #725BFF;
    --bg:     #F8F2FF;
    --dark:   #070037;
    --muted:  rgba(7,0,55,0.45);
    --border: rgba(7,0,55,0.12);
}

/* Base */
html, body, [class*="css"], * {
    font-family: 'DM Sans', sans-serif !important;
}
[class*="css"] { color: var(--dark); }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1rem !important; }
section[data-testid="stSidebar"] > div { padding: 0 1rem !important; }
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] div {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: var(--dark) !important;
}
.sidebar-label {
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: var(--muted) !important;
    margin-top: 14px;
    margin-bottom: 4px;
    display: block;
}

/* Main */
.main { background: var(--bg) !important; }
.main .block-container { padding: 1.4rem 2rem !important; max-width: 1500px; }

/* Page header */
.page-header {
    display: flex; align-items: baseline; gap: 10px;
    margin-bottom: 1.2rem; padding-bottom: 0.9rem;
    border-bottom: 1px solid var(--border);
}
.page-header h1 { font-size: 1.2rem; font-weight: 600; color: var(--dark); margin: 0; }
.page-header span { font-size: 12px; color: var(--muted); font-family: 'DM Mono', monospace !important; }

/* Section label main */
.slabel {
    font-size: 10px; font-weight: 600; letter-spacing: 0.09em;
    text-transform: uppercase; color: var(--muted);
    margin-top: 1.3rem; margin-bottom: 0.4rem; display: block;
}

/* KPI cards — all same height via flex */
.kpi-row { display: flex; gap: 10px; }
.kpi-card {
    flex: 1; background: var(--white);
    border: 1px solid var(--border); border-radius: 10px;
    padding: 14px 16px; min-height: 90px;
    display: flex; flex-direction: column; justify-content: space-between;
    animation: fadeUp .3s ease both;
}
.kpi-lbl  { font-size: 11px; color: var(--muted); margin-bottom: 4px; }
.kpi-val  { font-size: 1.4rem; font-weight: 600; color: var(--dark); font-family: 'DM Mono', monospace !important; line-height: 1.1; }
.kpi-vsm  { font-size: 0.9rem; font-weight: 600; color: var(--dark); line-height: 1.35; }
.kpi-sub  { font-size: 11px; color: var(--muted); margin-top: 4px; }

/* Table — single clean border, no double lines */
.fmt-wrap {
    border: 1px solid var(--border);
    border-radius: 10px; overflow: hidden;
    background: var(--white);
    animation: fadeUp .35s ease both;
    margin-top: 6px;
}
.fmt-wrap table { border: none !important; }
/* Override Streamlit's dataframe container border */
.fmt-wrap [data-testid="stDataFrame"] > div {
    border: none !important;
    border-radius: 0 !important;
}

/* Card */
.card-wrap {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 12px; padding: 22px; margin-top: 14px;
    animation: fadeUp .25s ease both;
}
.c-title { font-size: 1rem; font-weight: 600; color: var(--dark); margin-bottom: 2px; }
.c-id    { font-size: 11px; color: var(--muted); font-family: 'DM Mono', monospace !important; margin-bottom: 10px; }
.c-desc  { font-size: 13px; color: var(--dark); line-height: 1.65; margin-bottom: 14px; padding: 10px 14px; background: var(--bg); border-radius: 8px; }
.c-grid  { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 14px; }
.c-m     { background: var(--bg); border-radius: 8px; padding: 10px 12px; }
.c-mlbl  { font-size: 10px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: .07em; margin-bottom: 3px; }
.c-mval  { font-size: 1rem; font-weight: 600; color: var(--dark); font-family: 'DM Mono', monospace !important; }
.c-sec   { font-size: 10px; font-weight: 600; letter-spacing: .09em; text-transform: uppercase; color: var(--muted); margin: 12px 0 5px; }
.tags-row { display: flex; flex-wrap: wrap; gap: 4px; }
.tag     { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 500; margin: 1px 2px 1px 0; background: rgba(62,32,255,.07); color: var(--dark); }
.tag-v   { background: rgba(192,255,217,.7); color: #064d2a; }
.tag-b   { background: rgba(114,91,255,.1); color: var(--indigo); }
.tag-cpm { background: transparent; color: var(--dark); border: 1px solid var(--border); }
.tag-cpc { background: rgba(62,32,255,.12); color: var(--blue); }
.info-row { display: flex; gap: 8px; margin-bottom: 5px; }
.info-lbl { font-size: 13px; color: var(--muted); min-width: 160px; flex-shrink: 0; }
.info-val { font-size: 13px; color: var(--dark); font-weight: 500; }
.bool-y  { color: var(--blue); font-weight: 700; }
.bool-n  { color: rgba(7,0,55,.2); }

/* Score badge */
.s-pill { display: inline-flex; align-items: center; padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 600; font-family: 'DM Mono', monospace !important; }
.s-hi { background: var(--mint); color: #064d2a; }
.s-md { background: rgba(62,32,255,.08); color: var(--blue); border: 1px solid var(--border); }
.s-lo { background: var(--bg); color: var(--muted); border: 1px solid var(--border); }

/* Scoring */
.w-total { display: inline-block; font-size: 12px; font-weight: 600; font-family: 'DM Mono', monospace !important; padding: 3px 10px; border-radius: 6px; margin-top: 4px; }
.w-ok    { background: var(--mint); color: #064d2a; }
.w-bad   { background: rgba(62,32,255,.08); color: var(--indigo); }

hr.light { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }
.no-res  { text-align: center; padding: 40px 20px; color: var(--muted); background: var(--white); border: 1px solid var(--border); border-radius: 10px; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
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
            fp = p(n)
            if os.path.exists(fp): return pd.read_csv(fp)
        raise FileNotFoundError(f"Не найдено: {a} / {b}")

    df = rc("DataLens_-_formats.csv", "DataLens - formats.csv")
    di = rc("DataLens_-_dict_items.csv", "DataLens - dict_items.csv")

    fi = None
    for n in ["DataLens_-_format_items.csv", "DataLens - format_items.csv"]:
        if os.path.exists(p(n)): fi = pd.read_csv(p(n)); break
    if fi is None:
        if os.path.exists(p("DataLens.xlsx")):
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
    if pd.isna(v): return "—"
    x = round(v * 100, 1)
    return (f"{int(x)}%" if x == int(x) else f"{x:.1f}%").replace(".", ",")

def pct_plain(v):
    """For dataframe column display — plain string."""
    return pct(v)

def rub(v):
    if pd.isna(v): return "—"
    return f"{int(round(v)):,} ₽".replace(",", "\u202f")

def reach_str(v):
    if pd.isna(v): return "—"
    m = v / 1e6
    if m >= 1:
        return (f"{int(m)}M" if m == int(m) else f"{m:.1f}M").replace(".", ",")
    return f"{int(v):,}".replace(",", "\u202f")

def boolv(v):
    try:
        if pd.isna(v): return '<span class="bool-n">—</span>'
    except Exception: pass
    return '<span class="bool-y">✓</span>' if str(v).upper() in ("TRUE","1") else '<span class="bool-n">—</span>'

def safes(v):
    try:
        if pd.isna(v): return "—"
    except Exception: pass
    return str(v).strip() or "—"

def thtml(cell):
    if not isinstance(cell, list): return '<span style="color:rgba(7,0,55,.18);font-size:11px;">—</span>'
    return "".join(f'<span class="tag">{t}</span>' for t in cell)

# ─── eCPM ─────────────────────────────────────────────────────────────────────
def calc_ecpm(row):
    m = str(row.get("buy_model","CPM")).upper()
    ctr = row.get("ctr_avg", np.nan)
    d   = float(row.get("discount",0) or 0)
    if m == "CPM": raw = row.get("cpm_avg", np.nan)
    elif m == "CPC":
        cpc = row.get("cpc_avg", np.nan)
        raw = cpc*ctr*1000 if not any(map(pd.isna, [cpc,ctr])) and ctr else np.nan
    elif m == "CPV":
        cpv = row.get("cpv_avg", np.nan); vtr = row.get("vtr_avg", np.nan)
        raw = cpv*vtr*1000 if not any(map(pd.isna, [cpv,vtr])) and vtr else np.nan
    else: raw = row.get("cpm_avg", np.nan)
    return np.nan if pd.isna(raw) else raw*(1-d)

df["ecpm_eff"] = df.apply(calc_ecpm, axis=1)

def opts(did): return di[di["dict_id"]==did]["item_name"].dropna().tolist()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
def slbl(t):
    st.markdown(f'<span class="sidebar-label">{t}</span>', unsafe_allow_html=True)

with st.sidebar:
    slbl("Тип формата")
    format_types = st.multiselect("Тип", ["Видео","Баннер"], default=["Видео","Баннер"],
                                   placeholder="Все типы", label_visibility="collapsed")
    slbl("Устройство")
    devices = st.multiselect("Уст", ["Desktop","Mobile Web","In-App","Smart TV"],
                              default=["Desktop","Mobile Web","In-App","Smart TV"],
                              placeholder="Все устройства", label_visibility="collapsed")
    slbl("Модель закупки")
    buy_models = st.multiselect("Мод", ["CPM","CPC"], default=["CPM","CPC"],
                                 placeholder="Все модели", label_visibility="collapsed")

    show_b = not format_types or "Баннер" in format_types
    show_v = not format_types or "Видео"  in format_types

    if show_b:
        slbl("Баннер — отображение")
        f_disp = st.multiselect("Отобр", opts("display"), default=[],
                                 placeholder="Все варианты", label_visibility="collapsed")
    else: f_disp = []

    if show_v:
        slbl("Видео — плейсмент")
        f_plac = st.multiselect("Плейс", opts("placement"), default=[],
                                 placeholder="Все плейсменты", label_visibility="collapsed")
        slbl("Видео — позиция")
        f_inst = st.multiselect("Поз", opts("instream_pos"), default=[],
                                 placeholder="Все позиции", label_visibility="collapsed")
    else: f_plac = []; f_inst = []

    slbl("Таргетинги")
    f_targ = st.multiselect("Тарг", opts("targeting"), default=[],
                              placeholder="Все таргетинги", label_visibility="collapsed")
    slbl("DMP")
    f_dmp = st.multiselect("DMP", opts("dmp"), default=[],
                             placeholder="Все DMP", label_visibility="collapsed")

    slbl("Дополнительно")
    req_px = st.checkbox("Верификация пикселем")
    req_js = st.checkbox("Верификация JS-тегом")
    req_bl = st.checkbox("Brand Lift")
    req_sl = st.checkbox("Sales Lift")

    st.markdown('<hr class="light">', unsafe_allow_html=True)
    slbl("Пороговые значения")
    max_ecpm_f = st.slider("Макс. eCPM (после скидки), ₽", 0, 1000, 1000, step=10)
    min_ctr  = st.slider("Мин. CTR, %",        0.0,  5.0, 0.0, step=0.1)
    min_rch  = st.slider("Мин. охват, млн",    0.0, 80.0, 0.0, step=1.0)
    min_view = st.slider("Мин. Viewability, %", 0,   100,  0,   step=5)
    min_vtr  = st.slider("Мин. VTR, %",        0.0,100.0, 0.0, step=5.0)

    st.markdown('<hr class="light">', unsafe_allow_html=True)
    scoring = st.toggle("Включить скоринг", value=False)
    if scoring:
        slbl("Веса (сумма = 100)")
        wr = st.slider("Охват",               0,100,20,step=5)
        we = st.slider("eCPM (ниже — лучше)", 0,100,20,step=5)
        wc = st.slider("CTR",                 0,100,20,step=5)
        wv = st.slider("VTR",                 0,100,15,step=5)
        wi = st.slider("Viewability",         0,100,15,step=5)
        wm = st.slider("Комиссия (ниже — лучше)", 0,100,10,step=5)
        tw = wr+we+wc+wv+wi+wm
        st.markdown(
            f'<div class="w-total {"w-ok" if tw==100 else "w-bad"}">Сумма: {tw} / 100</div>',
            unsafe_allow_html=True)
        norm = st.checkbox("Нормализовать веса", value=True)
    else:
        wr=we=wc=wv=wi=wm=tw=0; norm=False

    st.markdown('<hr class="light">', unsafe_allow_html=True)
    slbl("Сезонность")
    months = ["Январь","Февраль","Март","Апрель","Май","Июнь",
              "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
    sel_month = st.selectbox("Месяц", months, index=months.index("Март"),
                              label_visibility="collapsed")

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
F["sk"]     = F["platform"].apply(lambda p: season_k(p, sel_month))
F["ecpm_s"] = F["ecpm_eff"] * F["sk"]

# ─── SCORING ──────────────────────────────────────────────────────────────────
def ncol(s, inv=False):
    mn, mx = s.min(), s.max()
    if mx == mn: return pd.Series([0.5]*len(s), index=s.index)
    n = (s-mn)/(mx-mn); return 1-n if inv else n

if scoring and len(F) > 0:
    W = dict(r=wr,e=we,c=wc,v=wv,i=wi,m=wm)
    t = sum(W.values())
    if norm and t > 0: W = {k:v/t for k,v in W.items()}
    else:               W = {k:v/100 for k,v in W.items()}
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
st.markdown(
    '<div class="page-header"><h1>Format Selector</h1>'
    '<span>Анализ рекламных форматов</span></div>',
    unsafe_allow_html=True)

# ─── KPI ──────────────────────────────────────────────────────────────────────
top   = F.iloc[0] if len(F) > 0 else None
avg_e = F["ecpm_s"].mean() if len(F) > 0 else np.nan
sk0   = F["sk"].iloc[0] if len(F) > 0 else 1.0
maxr  = F["max_reach"].max() if len(F) > 0 else np.nan

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="kpi-card">
        <div><div class="kpi-lbl">Форматов после фильтров</div>
        <div class="kpi-val">{len(F)}</div></div>
        <div class="kpi-sub">из {len(df)} доступных</div>
    </div>""", unsafe_allow_html=True)
with c2:
    if top is not None:
        lbl = "Лучший по скорингу" if scoring else "Самый дешевый eCPM"
        sub = f'Скор: {top["score"]:.0f}' if (scoring and not pd.isna(top.get("score",np.nan))) else top["buy_model"]
        st.markdown(f"""<div class="kpi-card">
            <div><div class="kpi-lbl">{lbl}</div>
            <div class="kpi-vsm">{top['format_name']}</div></div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="kpi-card"><div><div class="kpi-lbl">Лучший формат</div><div class="kpi-val">—</div></div><div class="kpi-sub">&nbsp;</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card">
        <div><div class="kpi-lbl">Средний eCPM (с сезонностью)</div>
        <div class="kpi-val">{rub(avg_e)}</div></div>
        <div class="kpi-sub">{sel_month} · коэф. {sk0}×</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card">
        <div><div class="kpi-lbl">Макс. охват</div>
        <div class="kpi-val">{reach_str(maxr)}</div></div>
        <div class="kpi-sub">среди отфильтрованных</div>
    </div>""", unsafe_allow_html=True)

# ─── CHARTS ───────────────────────────────────────────────────────────────────
if len(F) > 0:
    ch1, ch2 = st.columns(2)

    with ch1:
        cdf = F[F["ecpm_s"].notna()].sort_values("ecpm_s")
        if len(cdf) > 0:
            if scoring and cdf["score"].notna().any():
                mn, mx_ = cdf["score"].min(), cdf["score"].max()
                bar_colors = [
                    f"rgba(62,32,255,{0.3+0.7*(s-mn)/max(mx_-mn,1):.2f})"
                    for s in cdf["score"].fillna(mn)
                ]
            else:
                bar_colors = ["#3E20FF" if i==0 else "#725BFF" for i in range(len(cdf))]

            fig1 = go.Figure(go.Bar(
                x=cdf["ecpm_s"], y=cdf["format_name"],
                orientation="h", marker_color=bar_colors, marker_line_width=0,
                hovertemplate="<b>%{y}</b><br>eCPM: %{x:.0f} ₽<extra></extra>"
            ))
            fig1.update_layout(
                title=dict(text="eCPM по форматам (₽, с сезонностью)",
                           font_size=11, font_color="rgba(7,0,55,0.45)", font_family="DM Sans"),
                height=max(220, len(cdf)*30),
                margin=dict(l=0,r=10,t=32,b=0),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(gridcolor="rgba(7,0,55,0.07)", tickfont_size=10, title=None,
                           tickfont_color="rgba(7,0,55,0.45)"),
                yaxis=dict(tickfont_size=11, title=None, tickfont_color="#070037"),
                font_family="DM Sans",
            )
            st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    with ch2:
        sdf = F[F["ctr_avg"].notna() & F["viewability_avg"].notna()].copy()
        if len(sdf) >= 2:
            med = sdf["max_reach"].median()
            sdf["bsz"] = sdf["max_reach"].fillna(med).apply(lambda v: max(9,min(32,v/2.5e6)))
            if scoring and sdf["score"].notna().any():
                mn2, mx2 = sdf["score"].min(), sdf["score"].max()
                colors = [f"rgba(62,32,255,{0.3+0.7*(s-mn2)/max(mx2-mn2,1):.2f})"
                          for s in sdf["score"].fillna(mn2)]
            else:
                colors = ["#725BFF"] * len(sdf)

            fig2 = go.Figure()
            for i, (_, r) in enumerate(sdf.iterrows()):
                fig2.add_trace(go.Scatter(
                    x=[r["ctr_avg"]*100], y=[r["viewability_avg"]*100],
                    mode="markers+text",
                    marker=dict(size=r["bsz"], color=colors[i],
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
                           font_size=11, font_color="rgba(7,0,55,0.45)", font_family="DM Sans"),
                height=300, margin=dict(l=0,r=10,t=32,b=0),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(title="CTR, %", gridcolor="rgba(7,0,55,0.07)", tickfont_size=10,
                           title_font_size=10, tickfont_color="rgba(7,0,55,0.45)",
                           title_font_color="rgba(7,0,55,0.45)"),
                yaxis=dict(title="Viewability, %", gridcolor="rgba(7,0,55,0.07)", tickfont_size=10,
                           title_font_size=10, tickfont_color="rgba(7,0,55,0.45)",
                           title_font_color="rgba(7,0,55,0.45)"),
                font_family="DM Sans",
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        else:
            # Fallback: reach bar
            rdf = F[F["max_reach"].notna()].sort_values("max_reach", ascending=False)
            if len(rdf) > 0:
                fig3 = go.Figure(go.Bar(
                    x=rdf["format_name"], y=rdf["max_reach"]/1e6,
                    marker_color="#725BFF", marker_line_width=0,
                    hovertemplate="<b>%{x}</b><br>Охват: %{y:.1f}M<extra></extra>"
                ))
                fig3.update_layout(
                    title=dict(text="Охват по форматам (млн)",
                               font_size=11, font_color="rgba(7,0,55,0.45)", font_family="DM Sans"),
                    height=260, margin=dict(l=0,r=10,t=32,b=0),
                    paper_bgcolor="white", plot_bgcolor="white",
                    xaxis=dict(tickfont_size=9, tickangle=-30, tickfont_color="#070037"),
                    yaxis=dict(gridcolor="rgba(7,0,55,0.07)", tickfont_size=10, title=None),
                    font_family="DM Sans",
                )
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# ─── TABLE (st.dataframe with row selection) ──────────────────────────────────
st.markdown('<span class="slabel">Форматы</span>', unsafe_allow_html=True)
st.caption("Нажмите на строку, чтобы открыть карточку")

if len(F) == 0:
    st.markdown('<div class="no-res">Нет форматов, соответствующих выбранным фильтрам.</div>',
                unsafe_allow_html=True)
else:
    # Build display dataframe for st.dataframe
    def score_disp(s):
        if pd.isna(s): return ""
        return f"{s:.0f}"

    disp = pd.DataFrame({
        "Формат":     F["format_name"],
        "ID":         F["format_id"],
        "Тип":        F["format_type"].apply(
                          lambda c: ", ".join(c) if isinstance(c, list) else ""),
        "Модель":     F["buy_model"],
        "Устройства": F["device"].apply(
                          lambda c: ", ".join(c) if isinstance(c, list) else ""),
        "Охват":      F["max_reach"].apply(reach_str),
        "CTR":        F["ctr_avg"].apply(pct_plain),
        "Viewability":F["viewability_avg"].apply(pct_plain),
        "eCPM (сез.)":F["ecpm_s"].apply(rub),
    })
    if scoring:
        disp["Скор"] = F["score"].apply(score_disp)

    # st.dataframe with selection — works in Streamlit >= 1.35
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
        height=min(600, (len(F)+1)*36+2),
    )

    # ─── CARD (shown when row clicked) ────────────────────────────────────────
    sel_rows = event.selection.rows if hasattr(event, "selection") else []

    if sel_rows:
        idx = sel_rows[0]
        row = F.iloc[idx]

        ee  = row.get("ecpm_eff", np.nan)
        es2 = row.get("ecpm_s", np.nan)
        sc  = row.get("sk", 1.0)

        links = []
        for lbl_, key in [("Пример","example_url"),
                           ("Техтребования","technical_requirements_url"),
                           ("Медиакит","mediakit_url"),
                           ("Кейсы","cases_url")]:
            v = row.get(key)
            if isinstance(v, str) and v.startswith("http"):
                links.append(
                    f'<a href="{v}" target="_blank" style="font-size:12px;color:#3E20FF;'
                    f'text-decoration:none;margin-right:14px;font-weight:500;">{lbl_} ↗</a>'
                )

        st.markdown(f"""
        <div class="card-wrap">
            <div class="c-title">{row['format_name']}</div>
            <div class="c-id">{row['format_id']} · {row['buy_model']} · {safes(row.get('platform'))}</div>
            <div class="c-desc">{safes(row.get('description'))}</div>

            <div class="c-grid">
                <div class="c-m"><div class="c-mlbl">eCPM (факт)</div>
                    <div class="c-mval">{rub(ee)}</div></div>
                <div class="c-m"><div class="c-mlbl">eCPM (сезон. {sc}×)</div>
                    <div class="c-mval">{rub(es2)}</div></div>
                <div class="c-m"><div class="c-mlbl">Скидка</div>
                    <div class="c-mval">{pct(row.get('discount'))}</div></div>
                <div class="c-m"><div class="c-mlbl">Охват (макс.)</div>
                    <div class="c-mval">{reach_str(row.get('max_reach'))}</div></div>
                <div class="c-m"><div class="c-mlbl">CTR (среднее)</div>
                    <div class="c-mval">{pct(row.get('ctr_avg'))}</div></div>
                <div class="c-m"><div class="c-mlbl">VTR (среднее)</div>
                    <div class="c-mval">{pct(row.get('vtr_avg'))}</div></div>
                <div class="c-m"><div class="c-mlbl">Viewability (среднее)</div>
                    <div class="c-mval">{pct(row.get('viewability_avg'))}</div></div>
                <div class="c-m"><div class="c-mlbl">Комиссия</div>
                    <div class="c-mval">{pct(row.get('commission'))}</div></div>
                <div class="c-m"><div class="c-mlbl">Мин. бюджет</div>
                    <div class="c-mval">{rub(row.get('min_budget'))}</div></div>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
                <div class="c-sec">Ценовой диапазон</div>
                <div class="info-row"><span class="info-lbl">CPM мин / сред / макс</span>
                    <span class="info-val">{rub(row.get('cpm_min'))} / {rub(row.get('cpm_avg'))} / {rub(row.get('cpm_max'))}</span></div>
                <div class="info-row"><span class="info-lbl">CPC мин / сред / макс</span>
                    <span class="info-val">{rub(row.get('cpc_min'))} / {rub(row.get('cpc_avg'))} / {rub(row.get('cpc_max'))}</span></div>
                <div class="info-row"><span class="info-lbl">CTR мин / макс</span>
                    <span class="info-val">{pct(row.get('ctr_min'))} / {pct(row.get('ctr_max'))}</span></div>
                <div class="c-sec">Верификация</div>
                <div class="info-row"><span class="info-lbl">Пиксель</span>
                    <span class="info-val">{boolv(row.get('verification_pixel'))}</span></div>
                <div class="info-row"><span class="info-lbl">JS-тег</span>
                    <span class="info-val">{boolv(row.get('verification_js'))}</span></div>
                <div class="info-row"><span class="info-lbl">Условия верификации</span>
                    <span class="info-val" style="font-size:12px;color:var(--muted);">{safes(row.get('verification_terms'))}</span></div>
                <div class="c-sec">Исследования</div>
                <div class="info-row"><span class="info-lbl">Brand Lift</span>
                    <span class="info-val">{boolv(row.get('bls'))}</span></div>
                <div class="info-row"><span class="info-lbl">Sales Lift</span>
                    <span class="info-val">{boolv(row.get('sales_lift'))}</span></div>
            </div>
            <div>
                <div class="c-sec">Плейсмент</div>
                <div class="tags-row">{thtml(row.get('placement'))}</div>
                <div class="c-sec">Устройства</div>
                <div class="tags-row">{thtml(row.get('device'))}</div>
                <div class="c-sec">Отображение</div>
                <div class="tags-row">{thtml(row.get('display'))}</div>
                <div class="c-sec">DMP</div>
                <div class="tags-row">{thtml(row.get('dmp'))}</div>
                <div class="c-sec">Производство</div>
                <div class="tags-row">{thtml(row.get('production'))}</div>
            </div>
            </div>

            <div class="c-sec">Таргетинг</div>
            <div class="tags-row">{thtml(row.get('targeting'))}</div>

            <div class="c-sec">Наценки за таргетинг</div>
            <div class="tags-row">{thtml(row.get('targeting_markup'))}</div>

            {'<div class="c-sec">Ссылки</div><div style="margin-top:6px;">'+"".join(links)+"</div>" if links else ""}
        </div>
        """, unsafe_allow_html=True)

        for lbl_, key in [("Условия Brand Lift","bls_terms"),
                           ("Условия Sales Lift","sales_lift_terms"),
                           ("Условия сезонности","seasonality_terms")]:
            v = row.get(key)
            if isinstance(v, str) and v.strip():
                with st.expander(f"📋 {lbl_}"):
                    st.markdown(f'<div style="font-size:13px;color:var(--dark);line-height:1.65;">{v}</div>',
                                unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="margin-top:12px;padding:16px 20px;background:var(--white);'
            'border:1px solid var(--border);border-radius:10px;'
            'font-size:13px;color:var(--muted);">'
            '← Нажмите на строку в таблице, чтобы открыть карточку формата</div>',
            unsafe_allow_html=True
        )
