import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Подбор форматов", layout="wide")

# =========================
# Стили
# =========================
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.25rem;
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stCheckbox,
        section[data-testid="stSidebar"] .stRadio,
        section[data-testid="stSidebar"] .stNumberInput,
        section[data-testid="stSidebar"] .stMultiSelect,
        section[data-testid="stSidebar"] .stSelectbox,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {
            font-size: 14px;
        }

        .sidebar-section-title {
            font-size: 18px;
            font-weight: 700;
            margin: 1rem 0 0.5rem 0;
        }

        .sidebar-subtitle {
            font-size: 14px;
            font-weight: 600;
            margin: 0.5rem 0 0.25rem 0;
        }

        .small-muted {
            color: #6b7280;
            font-size: 13px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# Настройки
# =========================
DEFAULT_CSV_NAME = "DataLens - formats.csv"

LABELS = {
    "format_id": "ID формата",
    "format_name": "Название формата",
    "type_service": "Тип сервиса",
    "platform": "Площадка",
    "buy_model": "Модель закупки",
    "description": "Описание",
    "example_url": "Пример",
    "technical_requirements_url": "Технические требования",
    "mediakit_url": "Медиакит",
    "cases_url": "Кейсы",
    "max_reach": "Максимальный охват",
    "min_budget": "Минимальный бюджет",
    "discount": "Скидка",
    "commission": "Комиссия",
    "ecpm_base": "eCPM без скидки",
    "ecpm_discounted": "eCPM со скидкой",
    "ctr_avg": "CTR",
    "vtr_avg": "VTR",
    "viewability_avg": "Viewability",
    "bls": "BLS",
    "sales_lift": "Sales Lift",
    "verification_pixel": "Верификация пикселем",
    "verification_js": "Верификация JS-кодом",
    "verification_terms": "Условия верификации",
    "seasonality_terms": "Сезонность",
    "bls_terms": "Условия BLS",
    "sales_lift_terms": "Условия Sales Lift",
}

TEXT_SEARCH_COLUMNS = [
    "format_id",
    "format_name",
    "platform",
    "type_service",
    "description",
    "buy_model",
]

PERCENT_COLUMNS = {
    "discount",
    "commission",
    "ctr_avg",
    "vtr_avg",
    "viewability_avg",
    "score",
}

BOOLEAN_REQUIRE_COLUMNS = [
    "verification_pixel",
    "verification_js",
    "bls",
    "sales_lift",
]

CATEGORY_FILTER_COLUMNS = [
    "platform",
    "type_service",
    "buy_model",
]

SCORING_COLUMNS = [
    "max_reach",
    "ecpm_discounted",
    "ctr_avg",
    "vtr_avg",
    "viewability_avg",
    "commission",
]

SCORING_REVERSE_COLUMNS = {
    "ecpm_discounted",
}

TABLE_COLUMNS = [
    "format_id",
    "format_name",
    "type_service",
    "platform",
    "buy_model",
    "min_budget",
    "max_reach",
    "discount",
    "commission",
    "ecpm_discounted",
    "ctr_avg",
    "vtr_avg",
    "viewability_avg",
    "verification_pixel",
    "verification_js",
    "bls",
    "sales_lift",
]

DETAIL_ORDER = [
    "format_id",
    "format_name",
    "type_service",
    "platform",
    "buy_model",
    "description",
    "min_budget",
    "max_reach",
    "discount",
    "commission",
    "ecpm_base",
    "ecpm_discounted",
    "ctr_avg",
    "vtr_avg",
    "viewability_avg",
    "bls",
    "sales_lift",
    "verification_pixel",
    "verification_js",
    "verification_terms",
    "seasonality_terms",
    "bls_terms",
    "sales_lift_terms",
    "example_url",
    "technical_requirements_url",
    "mediakit_url",
    "cases_url",
]

FILTER_CONFIG = {
    "min_budget": {"mode": "max", "step": 10000.0},
    "max_reach": {"mode": "min", "step": 10000.0},
    "ecpm_discounted": {"mode": "max", "step": 10.0},
    "ctr_avg": {"mode": "min", "step": 0.1},
    "vtr_avg": {"mode": "min", "step": 0.1},
    "viewability_avg": {"mode": "min", "step": 0.1},
    "commission": {"mode": "min", "step": 0.1},
    "discount": {"mode": "min", "step": 0.1},
}

# =========================
# Вспомогательные функции
# =========================
def label(col: str) -> str:
    return LABELS.get(col, col)


def safe_to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def to_rate(series: pd.Series) -> pd.Series:
    s = safe_to_numeric(series).copy()
    mask = s > 1
    s.loc[mask] = s.loc[mask] / 100
    return s


def clean_yes_no(series: pd.Series) -> pd.Series:
    if series.dtype != "object":
        return series

    replacements = {
        "true": "Да",
        "false": "Нет",
        "yes": "Да",
        "no": "Нет",
        "1": "Да",
        "0": "Нет",
        "да": "Да",
        "нет": "Нет",
    }

    cleaned = (
        series.astype(str)
        .str.strip()
        .replace({"nan": np.nan, "None": np.nan, "": np.nan})
    )

    lower = cleaned.str.lower()
    mapped = lower.map(replacements)

    result = cleaned.copy()
    result.loc[mapped.notna()] = mapped.loc[mapped.notna()]
    return result


def format_number(value, digits: int = 2) -> str:
    if pd.isna(value):
        return "—"
    return f"{value:,.{digits}f}".replace(",", " ")


def format_percent(value, digits: int = 2) -> str:
    if pd.isna(value):
        return "—"
    return f"{value * 100:.{digits}f}%"


def display_value(col: str, value):
    if pd.isna(value):
        return "—"

    if col in PERCENT_COLUMNS:
        return format_percent(value)

    if col in ["min_budget", "max_reach"]:
        return format_number(value, 0)

    if col in ["ecpm_base", "ecpm_discounted"]:
        return format_number(value, 2)

    if col in ["verification_pixel", "verification_js"]:
        return str(value)

    if col in ["bls", "sales_lift"]:
        return "Да" if safe_scalar_to_bool(value) else "—"

    return value


def safe_scalar_to_bool(value) -> bool:
    if pd.isna(value):
        return False

    if isinstance(value, str):
        return value.strip().lower() in {"да", "true", "1", "yes"}

    try:
        return float(value) > 0
    except Exception:
        return False


def percent_to_internal(value: float) -> float:
    return value / 100


def internal_to_percent(value: float) -> float:
    return value * 100


def apply_text_search(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query.strip():
        return df

    search_cols = [c for c in TEXT_SEARCH_COLUMNS if c in df.columns]
    if not search_cols:
        return df

    mask = pd.Series(False, index=df.index)
    q = query.strip()

    for col in search_cols:
        mask = mask | df[col].astype(str).str.contains(q, case=False, na=False)

    return df[mask]


def apply_categorical_filter(df: pd.DataFrame, column: str, selected_values: list[str]) -> pd.DataFrame:
    if not selected_values or column not in df.columns:
        return df
    return df[df[column].isin(selected_values)]


def apply_required_flag_filter(df: pd.DataFrame, column: str, required: bool) -> pd.DataFrame:
    if not required or column not in df.columns:
        return df

    if df[column].dtype == "object":
        normalized = df[column].astype(str).str.strip().str.lower()
        return df[normalized.isin({"да", "true", "1", "yes"})]

    numeric = safe_to_numeric(df[column]).fillna(0)
    return df[numeric > 0]


def apply_min_filter(df: pd.DataFrame, column: str, min_value: float) -> pd.DataFrame:
    if column not in df.columns:
        return df
    series = safe_to_numeric(df[column])
    return df[series.isna() | (series >= min_value)]


def apply_max_filter(df: pd.DataFrame, column: str, max_value: float) -> pd.DataFrame:
    if column not in df.columns:
        return df
    series = safe_to_numeric(df[column])
    return df[series.isna() | (series <= max_value)]


def normalize_series(series: pd.Series, reverse: bool = False) -> pd.Series:
    s = safe_to_numeric(series)

    if s.notna().sum() == 0:
        return pd.Series(0.0, index=s.index)

    min_val = s.min()
    max_val = s.max()

    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return pd.Series(1.0, index=s.index)

    normalized = (s - min_val) / (max_val - min_val)
    normalized = normalized.fillna(0)

    if reverse:
        normalized = 1 - normalized

    return normalized


def normalize_weights_to_100(weights: dict[str, int]) -> dict[str, int]:
    total = sum(weights.values())

    if total == 0:
        return weights.copy()

    raw = {k: (v / total) * 100 for k, v in weights.items()}
    rounded = {k: int(round(v / 5) * 5) for k, v in raw.items()}

    diff = 100 - sum(rounded.values())

    while diff != 0:
        if diff > 0:
            candidates = sorted(raw.keys(), key=lambda k: raw[k] - rounded[k], reverse=True)
            moved = False
            for k in candidates:
                if rounded[k] <= 95:
                    rounded[k] += 5
                    diff -= 5
                    moved = True
                    if diff == 0:
                        break
            if not moved:
                break
        else:
            candidates = sorted(raw.keys(), key=lambda k: raw[k] - rounded[k])
            moved = False
            for k in candidates:
                if rounded[k] >= 5:
                    rounded[k] -= 5
                    diff += 5
                    moved = True
                    if diff == 0:
                        break
            if not moved:
                break

    return rounded


def add_scoring(df: pd.DataFrame, weights: dict[str, int]) -> pd.DataFrame:
    scored = df.copy()
    total_weight = sum(weights.values())

    if total_weight == 0:
        scored["score"] = np.nan
        return scored

    score = pd.Series(0.0, index=scored.index)

    for metric, weight in weights.items():
        if metric in scored.columns and weight > 0:
            normalized = normalize_series(
                scored[metric],
                reverse=(metric in SCORING_REVERSE_COLUMNS),
            )
            score += normalized * weight

    scored["score"] = score / total_weight
    return scored


def build_display_table(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    visible_cols = [c for c in columns if c in df.columns]
    display_df = df[visible_cols].copy()

    rename_map = {c: label(c) for c in visible_cols}
    display_df = display_df.rename(columns=rename_map)

    for raw_col in visible_cols:
        pretty_col = rename_map[raw_col]
        display_df[pretty_col] = display_df[pretty_col].apply(lambda x: display_value(raw_col, x))

    return display_df


def display_link(title: str, url: str):
    if pd.notna(url) and str(url).strip():
        st.markdown(f"**{title}:** [открыть]({url})")


def render_format_card(row: pd.Series):
    st.markdown("---")
    st.subheader("Карточка формата")

    left, right = st.columns([1.4, 1])

    with left:
        st.markdown(f"## {row.get('format_name', 'Без названия')}")
        st.write(f"**{label('format_id')}:** {display_value('format_id', row.get('format_id'))}")
        st.write(f"**{label('platform')}:** {display_value('platform', row.get('platform'))}")
        st.write(f"**{label('type_service')}:** {display_value('type_service', row.get('type_service'))}")
        st.write(f"**{label('buy_model')}:** {display_value('buy_model', row.get('buy_model'))}")

        description = row.get("description")
        if pd.notna(description) and str(description).strip():
            st.markdown("### Описание")
            st.write(description)

        st.markdown("### Ссылки")
        display_link("Пример", row.get("example_url"))
        display_link("Технические требования", row.get("technical_requirements_url"))
        display_link("Медиакит", row.get("mediakit_url"))
        display_link("Кейсы", row.get("cases_url"))

        verification_terms = row.get("verification_terms")
        if pd.notna(verification_terms) and str(verification_terms).strip():
            st.markdown("### Условия верификации")
            st.write(verification_terms)

        seasonality_terms = row.get("seasonality_terms")
        if pd.notna(seasonality_terms) and str(seasonality_terms).strip():
            st.markdown("### Сезонность")
            st.write(seasonality_terms)

        bls_terms = row.get("bls_terms")
        if pd.notna(bls_terms) and str(bls_terms).strip():
            st.markdown("### Условия BLS")
            st.write(bls_terms)

        sales_lift_terms = row.get("sales_lift_terms")
        if pd.notna(sales_lift_terms) and str(sales_lift_terms).strip():
            st.markdown("### Условия Sales Lift")
            st.write(sales_lift_terms)

    with right:
        st.markdown("### Метрики")

        c1, c2 = st.columns(2)
        c1.metric(label("min_budget"), format_number(row.get("min_budget"), 0))
        c2.metric(label("max_reach"), format_number(row.get("max_reach"), 0))

        c3, c4 = st.columns(2)
        c3.metric(label("discount"), format_percent(row.get("discount")))
        c4.metric(label("commission"), format_percent(row.get("commission")))

        c5, c6 = st.columns(2)
        c5.metric(label("ecpm_base"), format_number(row.get("ecpm_base")))
        c6.metric(label("ecpm_discounted"), format_number(row.get("ecpm_discounted")))

        c7, c8 = st.columns(2)
        c7.metric(label("ctr_avg"), format_percent(row.get("ctr_avg")))
        c8.metric(label("vtr_avg"), format_percent(row.get("vtr_avg")))

        c9, c10 = st.columns(2)
        c9.metric(label("viewability_avg"), format_percent(row.get("viewability_avg")))
        c10.metric("Скоринг", format_percent(row.get("score")) if "score" in row.index and pd.notna(row.get("score")) else "—")

        st.markdown("### Дополнительно")
        st.write(f"**{label('verification_pixel')}:** {display_value('verification_pixel', row.get('verification_pixel'))}")
        st.write(f"**{label('verification_js')}:** {display_value('verification_js', row.get('verification_js'))}")
        st.write(f"**{label('bls')}:** {'Да' if safe_scalar_to_bool(row.get('bls')) else '—'}")
        st.write(f"**{label('sales_lift')}:** {'Да' if safe_scalar_to_bool(row.get('sales_lift')) else '—'}")

    with st.expander("Показать все поля"):
        payload = {}
        for col in DETAIL_ORDER:
            if col in row.index:
                payload[label(col)] = display_value(col, row.get(col))
        st.json(payload)


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DEFAULT_CSV_NAME)
    df.columns = [c.strip() for c in df.columns]

    numeric_columns = [
        "max_reach",
        "min_budget",
        "discount",
        "commission",
        "cpm_min",
        "cpm_max",
        "cpm_avg",
        "cpc_min",
        "cpc_max",
        "cpc_avg",
        "cpv_min",
        "cpv_max",
        "cpv_avg",
        "ctr_min",
        "ctr_max",
        "ctr_avg",
        "vtr_min",
        "vtr_max",
        "vtr_avg",
        "viewability_min",
        "viewability_max",
        "viewability_avg",
        "bls",
        "sales_lift",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = safe_to_numeric(df[col])

    for col in ["verification_pixel", "verification_js"]:
        if col in df.columns:
            df[col] = clean_yes_no(df[col])

    for col in ["discount", "commission", "ctr_avg", "vtr_avg", "viewability_avg"]:
        if col in df.columns:
            df[col] = to_rate(df[col])

    for col in ["bls", "sales_lift"]:
        if col in df.columns:
            df[col] = safe_to_numeric(df[col]).fillna(0)

    if "buy_model" in df.columns:
        df["buy_model"] = df["buy_model"].astype(str).str.strip().str.upper()

    df["ecpm_base"] = np.nan

    if "buy_model" in df.columns:
        cpm_mask = df["buy_model"] == "CPM"
        cpc_mask = df["buy_model"] == "CPC"
        cpv_mask = df["buy_model"] == "CPV"

        if "cpm_avg" in df.columns:
            df.loc[cpm_mask, "ecpm_base"] = df.loc[cpm_mask, "cpm_avg"]

        if {"cpc_avg", "ctr_avg"}.issubset(df.columns):
            df.loc[cpc_mask, "ecpm_base"] = (
                df.loc[cpc_mask, "cpc_avg"] * df.loc[cpc_mask, "ctr_avg"] * 1000
            )

        if {"cpv_avg", "vtr_avg"}.issubset(df.columns):
            df.loc[cpv_mask, "ecpm_base"] = (
                df.loc[cpv_mask, "cpv_avg"] * df.loc[cpv_mask, "vtr_avg"] * 1000
            )

    if "discount" in df.columns:
        df["ecpm_discounted"] = df["ecpm_base"] * (1 - df["discount"])
    else:
        df["ecpm_discounted"] = df["ecpm_base"]

    return df


# =========================
# Состояние
# =========================
default_weights = {
    "max_reach": 20,
    "ecpm_discounted": 25,
    "ctr_avg": 20,
    "vtr_avg": 10,
    "viewability_avg": 10,
    "commission": 15,
}

if "weights" not in st.session_state:
    st.session_state["weights"] = default_weights.copy()

# Чтобы после нормализации слайдеры реально обновлялись
for metric in SCORING_COLUMNS:
    widget_key = f"score_{metric}"
    if widget_key not in st.session_state:
        st.session_state[widget_key] = st.session_state["weights"][metric]

# Выбор карточки
if "selected_format_id" not in st.session_state:
    st.session_state["selected_format_id"] = None

# =========================
# Данные
# =========================
st.title("Подбор форматов")
st.caption("Каталог форматов, фильтры и скоринг в одном интерфейсе")

try:
    df = load_data()
except FileNotFoundError:
    st.error("Файл `DataLens - formats.csv` не найден рядом с `app.py`.")
    st.stop()
except Exception as e:
    st.error(f"Не удалось прочитать файл: {e}")
    st.stop()

if df.empty:
    st.warning("Файл прочитан, но в нем нет строк.")
    st.stop()

# =========================
# Фильтры и скоринг
# =========================
with st.sidebar:
    st.markdown('<div class="sidebar-section-title">Фильтры</div>', unsafe_allow_html=True)

    search_query = st.text_input(
        "Поиск",
        placeholder="Название, площадка, описание",
    )

    filtered_df = apply_text_search(df, search_query)

    for col in CATEGORY_FILTER_COLUMNS:
        if col in filtered_df.columns:
            values = sorted([x for x in filtered_df[col].dropna().unique().tolist()])
            st.markdown(f'<div class="sidebar-subtitle">{label(col)}</div>', unsafe_allow_html=True)
            selected = st.multiselect(
                label(col),
                values,
                label_visibility="collapsed",
                placeholder="Выбери",
                key=f"cat_{col}",
            )
            filtered_df = apply_categorical_filter(filtered_df, col, selected)

    st.markdown('<div class="sidebar-subtitle">Обязательные параметры</div>', unsafe_allow_html=True)

    for col in BOOLEAN_REQUIRE_COLUMNS:
        if col in filtered_df.columns:
            required = st.checkbox(label(col), value=False, key=f"required_{col}")
            filtered_df = apply_required_flag_filter(filtered_df, col, required)

    st.markdown('<div class="sidebar-subtitle">Пороговые значения</div>', unsafe_allow_html=True)

    for col, config in FILTER_CONFIG.items():
        if col not in filtered_df.columns:
            continue

        series = safe_to_numeric(filtered_df[col]).dropna()
        if series.empty:
            continue

        min_val = float(series.min())
        max_val = float(series.max())

        if min_val == max_val:
            continue

        is_percent = col in PERCENT_COLUMNS
        ui_min = round(internal_to_percent(min_val), 2) if is_percent else min_val
        ui_max = round(internal_to_percent(max_val), 2) if is_percent else max_val

        st.markdown(f'<div class="sidebar-subtitle">{label(col)}</div>', unsafe_allow_html=True)

        if config["mode"] == "max":
            value = st.number_input(
                f"{label(col)} до",
                value=ui_max,
                step=config["step"],
                label_visibility="collapsed",
                key=f"max_only_{col}",
            )
            internal_value = percent_to_internal(value) if is_percent else value
            filtered_df = apply_max_filter(filtered_df, col, internal_value)

        if config["mode"] == "min":
            value = st.number_input(
                f"{label(col)} от",
                value=ui_min,
                step=config["step"],
                label_visibility="collapsed",
                key=f"min_only_{col}",
            )
            internal_value = percent_to_internal(value) if is_percent else value
            filtered_df = apply_min_filter(filtered_df, col, internal_value)

    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">Скоринг</div>', unsafe_allow_html=True)

    scoring_enabled = st.checkbox("Включить скоринг", value=False, key="scoring_enabled")

    if scoring_enabled:
        st.markdown(
            '<div class="small-muted">Укажи важность параметров. Шаг — 5. Сумма должна быть 100.</div>',
            unsafe_allow_html=True,
        )

        for col in SCORING_COLUMNS:
            current_val = st.slider(
                label(col),
                min_value=0,
                max_value=100,
                step=5,
                key=f"score_{col}",
            )
            st.session_state["weights"][col] = current_val

        total_weights = sum(st.session_state["weights"].values())
        st.write(f"**Сумма:** {total_weights}")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Нормализовать", use_container_width=True):
                normalized = normalize_weights_to_100(st.session_state["weights"])
                st.session_state["weights"] = normalized.copy()
                for metric, value in normalized.items():
                    st.session_state[f"score_{metric}"] = value
                st.rerun()

        with c2:
            if st.button("Сбросить", use_container_width=True):
                st.session_state["weights"] = default_weights.copy()
                for metric, value in default_weights.items():
                    st.session_state[f"score_{metric}"] = value
                st.rerun()

        top_n = st.number_input(
            "Сколько форматов показать",
            min_value=1,
            max_value=max(1, len(filtered_df)),
            value=min(10, max(1, len(filtered_df))),
            step=1,
        )
    else:
        top_n = len(filtered_df)

# =========================
# Скоринг и выдача
# =========================
result_df = filtered_df.copy()

if scoring_enabled:
    result_df = add_scoring(result_df, st.session_state["weights"])
    result_df = result_df.sort_values(by="score", ascending=False, na_position="last")
    result_df = result_df.head(int(top_n))

# =========================
# Верхние метрики
# =========================
m1, m2, m3, m4 = st.columns(4)

m1.metric("Форматов в выдаче", len(result_df))
m2.metric("Площадок", int(result_df["platform"].nunique()) if "platform" in result_df.columns else 0)
m3.metric(
    "Средний eCPM со скидкой",
    format_number(result_df["ecpm_discounted"].mean()) if "ecpm_discounted" in result_df.columns else "—",
)
m4.metric(
    "Средний CTR",
    format_percent(result_df["ctr_avg"].mean()) if "ctr_avg" in result_df.columns else "—",
)

st.divider()

# =========================
# Таблица
# =========================
st.subheader("Форматы")

sort_candidates = [
    c for c in [
        "format_name",
        "platform",
        "min_budget",
        "max_reach",
        "ecpm_discounted",
        "ctr_avg",
        "vtr_avg",
        "viewability_avg",
        "commission",
    ]
    if c in result_df.columns
]

if scoring_enabled and "score" in result_df.columns:
    sort_candidates = ["score"] + sort_candidates

c_sort_1, c_sort_2 = st.columns([2, 1])

with c_sort_1:
    sort_by = st.selectbox(
        "Сортировать по",
        sort_candidates,
        format_func=label,
    )

with c_sort_2:
    sort_order = st.selectbox(
        "Порядок",
        ["По убыванию", "По возрастанию"],
    )

table_df = result_df.sort_values(
    by=sort_by,
    ascending=(sort_order == "По возрастанию"),
    na_position="last",
).copy()

raw_table_columns = TABLE_COLUMNS.copy()
if scoring_enabled and "score" in table_df.columns:
    raw_table_columns = ["score"] + raw_table_columns

display_df = build_display_table(table_df, raw_table_columns)

st.caption("Можно выбрать формат кликом по строке. Если строка не выделяется, используй поле выбора под таблицей.")

event = st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    key="formats_table",
)

selected_rows = event.selection.rows if event and event.selection else []

if selected_rows:
    selected_format_id = table_df.iloc[selected_rows[0]]["format_id"]
    st.session_state["selected_format_id"] = selected_format_id

selector_options_df = table_df.copy()
selector_options_df["selector_label"] = (
    selector_options_df["format_name"].fillna("Без названия").astype(str)
    + " | "
    + selector_options_df["format_id"].fillna("—").astype(str)
)

selected_label = st.selectbox(
    "Выбор формата для карточки",
    options=["—"] + selector_options_df["selector_label"].tolist(),
    index=0,
)

if selected_label != "—":
    selected_format_id_from_select = selector_options_df.loc[
        selector_options_df["selector_label"] == selected_label, "format_id"
    ].iloc[0]
    st.session_state["selected_format_id"] = selected_format_id_from_select

csv_bytes = table_df[[c for c in raw_table_columns if c in table_df.columns]].to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "Скачать текущую выборку CSV",
    data=csv_bytes,
    file_name="filtered_formats.csv",
    mime="text/csv",
)

# =========================
# Карточка
# =========================
selected_format_id = st.session_state.get("selected_format_id")

if selected_format_id is not None and selected_format_id in table_df["format_id"].values:
    selected_row = table_df.loc[table_df["format_id"] == selected_format_id].iloc[0]
    render_format_card(selected_row)
