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
            padding-top: 1.4rem;
            padding-bottom: 2rem;
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.1rem;
            padding-bottom: 1.2rem;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {
            font-size: 15px !important;
            line-height: 1.35 !important;
        }

        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea {
            font-size: 15px !important;
        }

        .sidebar-title {
            font-size: 21px;
            font-weight: 700;
            margin: 0 0 0.85rem 0;
        }

        .sidebar-group {
            font-size: 17px;
            font-weight: 700;
            margin: 1rem 0 0.45rem 0;
        }

        .sidebar-field {
            font-size: 15px;
            font-weight: 600;
            margin: 0.45rem 0 0.15rem 0;
        }

        .sidebar-compact-note {
            font-size: 13px;
            color: #6b7280;
            margin: 0.35rem 0 0 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# Файлы
# =========================
FORMATS_CANDIDATES = [
    "DataLens - formats.csv",
]

DICT_CANDIDATES = [
    "DataLens - dict_items.csv",
    "DataLens - dict_items (1).csv",
]

FORMAT_ITEMS_CANDIDATES = [
    "DataLens - format_items.csv",
]


# =========================
# Названия полей
# =========================
LABELS = {
    "format_id": "ID формата",
    "format_name": "Название формата",
    "format_type": "Тип формата",
    "type_service": "Тип сервиса",
    "platform": "Площадка",
    "buy_model": "Модель закупки",
    "device": "Устройства",
    "display": "Тип показа",
    "placement": "Размещение",
    "instream_pos": "Позиция в ролике",
    "dmp": "DMP",
    "production": "Продакшн",
    "other_markup": "Прочие надбавки",
    "targeting": "Таргетинги",
    "targeting_markup": "Надбавки за таргетинги",
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
    "verification_pixel": "Верификация пикселем",
    "verification_js": "Верификация JS-кодом",
    "verification_terms": "Условия верификации",
    "bls": "BLS",
    "sales_lift": "Sales Lift",
    "bls_terms": "Условия BLS",
    "sales_lift_terms": "Условия Sales Lift",
    "seasonality_terms": "Сезонность",
    "score": "Скоринг",
}


# =========================
# Конфиг интерфейса
# =========================
TEXT_SEARCH_COLUMNS = [
    "format_id",
    "format_name",
    "platform",
    "description",
    "type_service",
    "buy_model",
    "format_type",
]

MAIN_CATEGORY_FILTERS = [
    "format_type",
    "platform",
    "device",
    "placement",
    "buy_model",
    "type_service",
    "display",
    "instream_pos",
    "dmp",
]

TAG_FILTERS = [
    "targeting",
    "targeting_markup",
]

BOOLEAN_REQUIRE_COLUMNS = [
    "verification_pixel",
    "verification_js",
    "bls",
    "sales_lift",
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

# Сократила набор колонок в верхней таблице
TABLE_COLUMNS = [
    "score",
    "format_name",
    "format_type",
    "platform",
    "buy_model",
    "min_budget",
    "max_reach",
    "ecpm_discounted",
    "ctr_avg",
    "vtr_avg",
    "viewability_avg",
    "discount",
    "commission",
]

CARD_DETAIL_FIELDS = [
    "device",
    "display",
    "placement",
    "instream_pos",
    "dmp",
    "production",
    "other_markup",
    "verification_pixel",
    "verification_js",
]

CARD_TEXT_FIELDS = [
    "description",
    "verification_terms",
    "bls_terms",
    "sales_lift_terms",
    "seasonality_terms",
]

PERCENT_COLUMNS = {
    "discount",
    "commission",
    "ctr_avg",
    "vtr_avg",
    "viewability_avg",
    "score",
}

BOOL_TEXT_COLUMNS = {
    "verification_pixel",
    "verification_js",
}


# =========================
# Вспомогательные функции
# =========================
def label(column: str) -> str:
    return LABELS.get(column, column)


def find_existing_file(candidates: list[str]) -> str:
    for filename in candidates:
        try:
            with open(filename, "r", encoding="utf-8"):
                return filename
        except FileNotFoundError:
            continue
    raise FileNotFoundError(f"Не найден ни один файл из списка: {candidates}")


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


def safe_scalar_to_bool(value) -> bool:
    if pd.isna(value):
        return False

    if isinstance(value, str):
        return value.strip().lower() in {"да", "true", "1", "yes"}

    try:
        return float(value) > 0
    except Exception:
        return False


def trim_decimal_string(text: str) -> str:
    if "," not in text:
        return text
    text = text.rstrip("0").rstrip(",")
    return text


def format_number(value, digits: int = 2) -> str:
    if pd.isna(value):
        return ""
    formatted = f"{float(value):,.{digits}f}"
    formatted = formatted.replace(",", " ").replace(".", ",")
    formatted = trim_decimal_string(formatted)
    return formatted


def format_integer(value) -> str:
    if pd.isna(value):
        return ""
    return f"{int(round(float(value))):,}".replace(",", " ")


def format_percent(value, digits: int = 2) -> str:
    if pd.isna(value):
        return ""
    formatted = f"{float(value) * 100:.{digits}f}".replace(".", ",")
    formatted = trim_decimal_string(formatted)
    return f"{formatted}%"


def display_value(column: str, value):
    if pd.isna(value):
        return ""

    if column in PERCENT_COLUMNS:
        return format_percent(value)

    if column in ["min_budget", "max_reach"]:
        return format_integer(value)

    if column in ["ecpm_base", "ecpm_discounted"]:
        return format_number(value, 2)

    if column in BOOL_TEXT_COLUMNS:
        return str(value)

    if column in ["bls", "sales_lift"]:
        return "Да" if safe_scalar_to_bool(value) else ""

    return value


def percent_to_internal(value: float) -> float:
    return value / 100


def internal_to_percent(value: float) -> float:
    return value * 100


def split_tags(value) -> list[str]:
    if pd.isna(value):
        return []
    if isinstance(value, list):
        return value
    text = str(value).strip()
    if not text:
        return []
    return [x.strip() for x in text.split(",") if x.strip()]


def join_unique(values: list[str]) -> str:
    cleaned = []
    seen = set()
    for value in values:
        if pd.isna(value):
            continue
        text = str(value).strip()
        if not text:
            continue
        if text not in seen:
            seen.add(text)
            cleaned.append(text)
    return ", ".join(cleaned)


def apply_text_search(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query.strip():
        return df

    q = query.strip()
    search_cols = [c for c in TEXT_SEARCH_COLUMNS if c in df.columns]

    if not search_cols:
        return df

    mask = pd.Series(False, index=df.index)
    for col in search_cols:
        mask = mask | df[col].astype(str).str.contains(q, case=False, na=False)

    return df[mask]


def apply_categorical_filter(df: pd.DataFrame, column: str, selected_values: list[str]) -> pd.DataFrame:
    if column not in df.columns or not selected_values:
        return df

    def has_any_match(cell):
        values = split_tags(cell)
        return any(v in values for v in selected_values)

    return df[df[column].apply(has_any_match)]


def apply_required_flag_filter(df: pd.DataFrame, column: str, required: bool) -> pd.DataFrame:
    if column not in df.columns or not required:
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
            order = sorted(raw.keys(), key=lambda k: raw[k] - rounded[k], reverse=True)
            moved = False
            for key in order:
                if rounded[key] <= 95:
                    rounded[key] += 5
                    diff -= 5
                    moved = True
                    break
            if not moved:
                break
        else:
            order = sorted(raw.keys(), key=lambda k: raw[k] - rounded[k])
            moved = False
            for key in order:
                if rounded[key] >= 5:
                    rounded[key] -= 5
                    diff += 5
                    moved = True
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


def render_detail_line(field: str, value):
    shown = display_value(field, value)
    if shown != "":
        st.write(f"**{label(field)}:** {shown}")


def render_format_card(row: pd.Series):
    st.markdown("---")
    st.subheader(row.get("format_name", "Карточка формата"))

    left, right = st.columns([1.35, 1])

    with left:
        description = row.get("description")
        if pd.notna(description) and str(description).strip():
            st.markdown("### Описание")
            st.write(description)

        st.markdown("### Дополнительно")
        any_detail = False
        for field in CARD_DETAIL_FIELDS:
            if field in row.index:
                shown = display_value(field, row.get(field))
                if shown != "":
                    any_detail = True
                    st.write(f"**{label(field)}:** {shown}")

        if not any_detail:
            st.write("")

        st.markdown("### Ссылки")
        display_link("Пример", row.get("example_url"))
        display_link("Технические требования", row.get("technical_requirements_url"))
        display_link("Медиакит", row.get("mediakit_url"))
        display_link("Кейсы", row.get("cases_url"))

    with right:
        st.markdown("### Условия")
        any_text = False
        for field in CARD_TEXT_FIELDS:
            value = row.get(field)
            if pd.notna(value) and str(value).strip():
                any_text = True
                st.write(f"**{label(field)}:**")
                st.write(value)

        if not any_text:
            st.write("")


# =========================
# Коллбэки для скоринга
# =========================
def normalize_weight_state():
    weights = {
        metric: int(st.session_state.get(f"score_{metric}", 0))
        for metric in SCORING_COLUMNS
    }
    normalized = normalize_weights_to_100(weights)
    for metric, value in normalized.items():
        st.session_state[f"score_{metric}"] = value


def reset_weight_state():
    defaults = {
        "max_reach": 20,
        "ecpm_discounted": 25,
        "ctr_avg": 20,
        "vtr_avg": 10,
        "viewability_avg": 10,
        "commission": 15,
    }
    for metric, value in defaults.items():
        st.session_state[f"score_{metric}"] = value


# =========================
# Загрузка и сборка данных
# =========================
@st.cache_data
def load_data() -> pd.DataFrame:
    formats_path = find_existing_file(FORMATS_CANDIDATES)
    dict_path = find_existing_file(DICT_CANDIDATES)
    format_items_path = find_existing_file(FORMAT_ITEMS_CANDIDATES)

    formats = pd.read_csv(formats_path)
    dict_items = pd.read_csv(dict_path)
    format_items = pd.read_csv(format_items_path)

    formats.columns = [c.strip() for c in formats.columns]
    dict_items.columns = [c.strip() for c in dict_items.columns]
    format_items.columns = [c.strip() for c in format_items.columns]

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
        if col in formats.columns:
            formats[col] = safe_to_numeric(formats[col])

    for col in ["discount", "commission", "ctr_avg", "vtr_avg", "viewability_avg"]:
        if col in formats.columns:
            formats[col] = to_rate(formats[col])

    if "buy_model" in formats.columns:
        formats["buy_model"] = formats["buy_model"].astype(str).str.strip().str.upper()

    for col in ["verification_pixel", "verification_js"]:
        if col in formats.columns:
            formats[col] = clean_yes_no(formats[col])

    merged_items = format_items.merge(
        dict_items[["dict_id", "item_id", "item_name"]],
        on=["dict_id", "item_id"],
        how="left",
    )

    pivot_dict = {}
    for dict_id in merged_items["dict_id"].dropna().unique():
        grouped = (
            merged_items[merged_items["dict_id"] == dict_id]
            .groupby("format_id")["item_name"]
            .apply(lambda s: join_unique(sorted(pd.unique(s.dropna()))))
            .reset_index()
            .rename(columns={"item_name": dict_id})
        )
        pivot_dict[dict_id] = grouped

    df = formats.copy()

    for dict_id, part in pivot_dict.items():
        df = df.merge(part, on="format_id", how="left")

    if "format_type" not in df.columns:
        df["format_type"] = np.nan

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
# Инициализация состояния
# =========================
defaults = {
    "max_reach": 20,
    "ecpm_discounted": 25,
    "ctr_avg": 20,
    "vtr_avg": 10,
    "viewability_avg": 10,
    "commission": 15,
}

for metric, value in defaults.items():
    if f"score_{metric}" not in st.session_state:
        st.session_state[f"score_{metric}"] = value

if "selected_format_id" not in st.session_state:
    st.session_state["selected_format_id"] = None

if "top_n" not in st.session_state:
    st.session_state["top_n"] = 10


# =========================
# Основной экран
# =========================
st.title("Подбор форматов")

try:
    df = load_data()
except Exception as e:
    st.error(f"Не удалось загрузить данные: {e}")
    st.stop()

if df.empty:
    st.warning("В данных нет строк.")
    st.stop()


# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown('<div class="sidebar-title">Фильтры</div>', unsafe_allow_html=True)

    search_query = st.text_input(
        "Поиск",
        placeholder="Название, площадка, описание",
    )

    filtered_df = apply_text_search(df, search_query)

    for col in MAIN_CATEGORY_FILTERS:
        if col in filtered_df.columns:
            values = sorted(
                {
                    item
                    for cell in filtered_df[col].dropna().tolist()
                    for item in split_tags(cell)
                }
            )
            if values:
                st.markdown(f'<div class="sidebar-field">{label(col)}</div>', unsafe_allow_html=True)
                selected = st.multiselect(
                    label(col),
                    values,
                    label_visibility="collapsed",
                    placeholder="Выбери",
                    key=f"filter_{col}",
                )
                filtered_df = apply_categorical_filter(filtered_df, col, selected)

    for col in TAG_FILTERS:
        if col in filtered_df.columns:
            values = sorted(
                {
                    item
                    for cell in filtered_df[col].dropna().tolist()
                    for item in split_tags(cell)
                }
            )
            if values:
                st.markdown(f'<div class="sidebar-field">{label(col)}</div>', unsafe_allow_html=True)
                selected = st.multiselect(
                    label(col),
                    values,
                    label_visibility="collapsed",
                    placeholder="Выбери",
                    key=f"tag_{col}",
                )
                filtered_df = apply_categorical_filter(filtered_df, col, selected)

    for col in BOOLEAN_REQUIRE_COLUMNS:
        if col in filtered_df.columns:
            required = st.checkbox(label(col), value=False, key=f"required_{col}")
            filtered_df = apply_required_flag_filter(filtered_df, col, required)

    numeric_filter_pairs = [
        ("min_budget", "max_reach"),
        ("ecpm_discounted", "ctr_avg"),
        ("vtr_avg", "viewability_avg"),
        ("commission", "discount"),
    ]

    for left_col, right_col in numeric_filter_pairs:
        c1, c2 = st.columns(2)

        for col, container in [(left_col, c1), (right_col, c2)]:
            if col not in filtered_df.columns or col not in FILTER_CONFIG:
                continue

            series = safe_to_numeric(filtered_df[col]).dropna()
            if series.empty:
                continue

            min_val = float(series.min())
            max_val = float(series.max())

            if min_val == max_val:
                continue

            config = FILTER_CONFIG[col]
            is_percent = col in PERCENT_COLUMNS
            ui_min = round(internal_to_percent(min_val), 2) if is_percent else min_val
            ui_max = round(internal_to_percent(max_val), 2) if is_percent else max_val

            with container:
                st.markdown(f'<div class="sidebar-field">{label(col)}</div>', unsafe_allow_html=True)

                if config["mode"] == "max":
                    value = st.number_input(
                        f"{label(col)} до",
                        value=ui_max,
                        step=config["step"],
                        label_visibility="collapsed",
                        key=f"max_{col}",
                    )
                    internal = percent_to_internal(value) if is_percent else value
                    filtered_df = apply_max_filter(filtered_df, col, internal)

                if config["mode"] == "min":
                    value = st.number_input(
                        f"{label(col)} от",
                        value=ui_min,
                        step=config["step"],
                        label_visibility="collapsed",
                        key=f"min_{col}",
                    )
                    internal = percent_to_internal(value) if is_percent else value
                    filtered_df = apply_min_filter(filtered_df, col, internal)

    st.markdown('<div class="sidebar-group">Скоринг</div>', unsafe_allow_html=True)

    scoring_enabled = st.checkbox("Включить скоринг", value=False, key="scoring_enabled")

    if scoring_enabled:
        st.markdown(f'<div class="sidebar-field">Сколько форматов показать</div>', unsafe_allow_html=True)
        top_n_input = st.number_input(
            "Сколько форматов показать",
            min_value=1,
            value=int(st.session_state.get("top_n", 10)),
            step=1,
            label_visibility="collapsed",
            key="top_n",
        )

        for col in SCORING_COLUMNS:
            st.markdown(f'<div class="sidebar-field">{label(col)}</div>', unsafe_allow_html=True)
            st.slider(
                label(col),
                min_value=0,
                max_value=100,
                step=5,
                label_visibility="collapsed",
                key=f"score_{col}",
            )

        total_weights = sum(int(st.session_state.get(f"score_{metric}", 0)) for metric in SCORING_COLUMNS)
        st.write(f"**Сумма:** {total_weights}")

        c1, c2 = st.columns([1.15, 1])
        with c1:
            st.button("Нормализовать", use_container_width=True, on_click=normalize_weight_state)
        with c2:
            st.button("Сбросить", use_container_width=True, on_click=reset_weight_state)


# =========================
# Скоринг
# =========================
result_df = filtered_df.copy()

if scoring_enabled:
    current_weights = {
        metric: int(st.session_state.get(f"score_{metric}", 0))
        for metric in SCORING_COLUMNS
    }
    result_df = add_scoring(result_df, current_weights)
    result_df = result_df.sort_values(by="score", ascending=False, na_position="last")

    requested_top_n = max(1, int(st.session_state.get("top_n", 10)))
    available_rows = len(result_df)
    actual_top_n = min(requested_top_n, available_rows)

    result_df = result_df.head(actual_top_n)
else:
    if "score" not in result_df.columns:
        result_df["score"] = np.nan
    requested_top_n = None
    available_rows = len(result_df)
    actual_top_n = len(result_df)


# =========================
# Верхние метрики
# =========================
m1, m2, m3, m4 = st.columns(4)
m1.metric("Форматов в выдаче", len(result_df))
m2.metric("Площадок", int(result_df["platform"].nunique()) if "platform" in result_df.columns else 0)
m3.metric(
    "Средний eCPM со скидкой",
    format_number(result_df["ecpm_discounted"].mean(), 2) if "ecpm_discounted" in result_df.columns else "",
)
m4.metric(
    "Средний CTR",
    format_percent(result_df["ctr_avg"].mean()) if "ctr_avg" in result_df.columns else "",
)

if scoring_enabled and requested_top_n is not None and available_rows < requested_top_n:
    st.caption(f"Показаны все доступные форматы: {available_rows}")

st.divider()


# =========================
# Таблица
# =========================
table_columns = [c for c in TABLE_COLUMNS if c in result_df.columns]
if not scoring_enabled and "score" in table_columns:
    table_columns.remove("score")

display_df = build_display_table(result_df, table_columns)

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
    st.session_state["selected_format_id"] = result_df.iloc[selected_rows[0]]["format_id"]


# =========================
# Карточка
# =========================
selected_format_id = st.session_state.get("selected_format_id")

if selected_format_id is not None and selected_format_id in result_df["format_id"].values:
    selected_row = result_df.loc[result_df["format_id"] == selected_format_id].iloc[0]
    render_format_card(selected_row)
