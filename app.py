import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st


# =========================
# Константы и настройки
# =========================

st.set_page_config(page_title="Подбор рекламных форматов", layout="wide")

APP_DIR = Path(__file__).resolve().parent

FORMATS_CSV = "DataLens - formats.csv"
DICT_ITEMS_CSV = "DataLens - dict_items.csv"
FORMAT_ITEMS_CSV = "DataLens - format_items.csv"
FALLBACK_XLSX = "DataLens.xlsx"

DICT_LABELS = {
    "format_type": "Тип формата",
    "device": "Устроиство",
    "display": "Тип размещения креатива",
    "dmp": "DMP / данные",
    "instream_pos": "Позиция в потоке",
    "other_markup": "Дополнительные надбавки",
    "placement": "Размещение",
    "production": "Продакшн",
    "targeting": "Таргетинги",
    "targeting_markup": "Таргетинги с наценкой",
    "seasonality_coeff": "Сезонность",
}

BASE_COLUMN_LABELS = {
    "format_id": "ID формата",
    "type_service": "Тип сервиса",
    "platform": "Платформа",
    "format_name": "Название формата",
    "example_url": "Пример",
    "description": "Описание",
    "max_reach": "Максимальный охват",
    "min_budget": "Минимальныи бюджет",
    "discount": "Скидка",
    "buy_model": "Модель закупки",
    "cpm_min": "CPM min",
    "cpm_max": "CPM max",
    "cpm_avg": "CPM avg",
    "cpc_min": "CPC min",
    "cpc_max": "CPC max",
    "cpc_avg": "CPC avg",
    "cpv_min": "CPV min",
    "cpv_max": "CPV max",
    "cpv_avg": "CPV avg",
    "ctr_min": "CTR min",
    "ctr_max": "CTR max",
    "ctr_avg": "CTR avg",
    "vtr_min": "VTR min",
    "vtr_max": "VTR max",
    "vtr_avg": "VTR avg",
    "viewability_min": "Viewability min",
    "viewability_max": "Viewability max",
    "viewability_avg": "Viewability avg",
    "verification_pixel": "Верификация Pixel",
    "verification_js": "Верификация JS",
    "verification_terms": "Условия верификации",
    "commission": "Commission",
    "bls": "BLS",
    "sales_lift": "Sales Lift",
    "bls_terms": "Условия BLS",
    "sales_lift_terms": "Условия Sales Lift",
    "seasonality_terms": "Условия сезонности",
    "technical_requirements_url": "Технические требования",
    "mediakit_url": "Медиакит",
    "cases_url": "Кейсы",
    "ecpm_discounted": "eCPM с учетом скидки",
    "score": "Скоринг",
}

DEFAULT_WEIGHTS = {
    "max_reach": 25,
    "ecpm_discounted": 25,
    "ctr_avg": 15,
    "vtr_avg": 15,
    "viewability_avg": 10,
    "commission": 10,
}


# =========================
# Утилиты
# =========================

def safe_read_table(path_csv: Path, fallback_xlsx: Path, sheet_name: str) -> pd.DataFrame:
    if path_csv.exists():
        return pd.read_csv(path_csv)
    if fallback_xlsx.exists():
        return pd.read_excel(fallback_xlsx, sheet_name=sheet_name)
    raise FileNotFoundError(f"Не наиден источник данных: {path_csv.name} / {fallback_xlsx.name}:{sheet_name}")


def find_data_file(filename: str) -> Path:
    candidates = [
        APP_DIR / filename,
        Path.cwd() / filename,
        Path("/mnt/data") / filename,
    ]
    for path in candidates:
        if path.exists():
            return path
    return APP_DIR / filename


def to_float(series: pd.Series) -> pd.Series:
    if series is None:
        return pd.Series(dtype="float64")
    cleaned = (
        series.astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .replace({"None": np.nan, "nan": np.nan, "": np.nan})
    )
    return pd.to_numeric(cleaned, errors="coerce")


def to_bool(series: pd.Series) -> pd.Series:
    mapping = {
        True: True,
        False: False,
        "TRUE": True,
        "FALSE": False,
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        1: True,
        0: False,
        "Да": True,
        "Нет": False,
        "да": True,
        "нет": False,
    }
    return series.map(lambda x: mapping.get(x, x)).fillna(False).astype(bool)


def safe_ratio_minmax(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    valid = s.dropna()
    if valid.empty:
        return pd.Series(np.zeros(len(s)), index=s.index)
    min_v = valid.min()
    max_v = valid.max()
    if pd.isna(min_v) or pd.isna(max_v) or math.isclose(min_v, max_v):
        return pd.Series(np.ones(len(s)), index=s.index)
    return (s - min_v) / (max_v - min_v)


def safe_inverse_minmax(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    valid = s.dropna()
    if valid.empty:
        return pd.Series(np.zeros(len(s)), index=s.index)
    min_v = valid.min()
    max_v = valid.max()
    if pd.isna(min_v) or pd.isna(max_v) or math.isclose(min_v, max_v):
        return pd.Series(np.ones(len(s)), index=s.index)
    return (max_v - s) / (max_v - min_v)


def format_number(value, digits: int = 2) -> str:
    if pd.isna(value):
        return "—"
    if isinstance(value, (int, np.integer)):
        return f"{int(value):,}".replace(",", " ")
    if isinstance(value, (float, np.floating)):
        return f"{value:,.{digits}f}".replace(",", " ").replace(".", ",")
    return str(value)


def format_percent(value) -> str:
    if pd.isna(value):
        return "—"
    return f"{float(value) * 100:.1f}%".replace(".", ",")


def format_bool(value) -> str:
    if pd.isna(value):
        return "—"
    return "Да" if bool(value) else "Нет"


def normalize_weights(weights: Dict[str, float]) -> Dict[str, int]:
    total = sum(max(0.0, float(v)) for v in weights.values())
    if total <= 0:
        return DEFAULT_WEIGHTS.copy()

    scaled = {k: (max(0.0, float(v)) / total) * 100 for k, v in weights.items()}
    rounded = {k: int(round(v)) for k, v in scaled.items()}

    diff = 100 - sum(rounded.values())
    if diff != 0:
        remainders = sorted(
            scaled.items(),
            key=lambda kv: kv[1] - math.floor(kv[1]),
            reverse=(diff > 0),
        )
        idx = 0
        while diff != 0 and remainders:
            key = remainders[idx % len(remainders)][0]
            rounded[key] += 1 if diff > 0 else -1
            diff += -1 if diff > 0 else 1
            idx += 1

    return rounded


def get_column_label(column_name: str) -> str:
    return BASE_COLUMN_LABELS.get(column_name, DICT_LABELS.get(column_name, column_name))


# =========================
# Загрузка и подготовка
# =========================

@st.cache_data
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    formats_path = find_data_file(FORMATS_CSV)
    dict_items_path = find_data_file(DICT_ITEMS_CSV)
    format_items_path = find_data_file(FORMAT_ITEMS_CSV)
    fallback_xlsx_path = find_data_file(FALLBACK_XLSX)

    formats = safe_read_table(formats_path, fallback_xlsx_path, "formats")
    dict_items = safe_read_table(dict_items_path, fallback_xlsx_path, "dict_items")
    format_items = safe_read_table(format_items_path, fallback_xlsx_path, "format_items")

    return formats, dict_items, format_items


def preprocess_formats(formats: pd.DataFrame) -> pd.DataFrame:
    df = formats.copy()

    numeric_cols = [
        "max_reach", "min_budget", "discount", "commission",
        "cpm_min", "cpm_max", "cpm_avg",
        "cpc_min", "cpc_max", "cpc_avg",
        "cpv_min", "cpv_max", "cpv_avg",
        "ctr_min", "ctr_max", "ctr_avg",
        "vtr_min", "vtr_max", "vtr_avg",
        "viewability_min", "viewability_max", "viewability_avg",
    ]
    bool_cols = ["verification_pixel", "verification_js", "bls", "sales_lift"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = to_float(df[col])

    for col in bool_cols:
        if col in df.columns:
            df[col] = to_bool(df[col])

    return df


def build_dict_aggregates(format_items: pd.DataFrame, dict_items: pd.DataFrame) -> pd.DataFrame:
    dict_df = dict_items.copy()
    fi_df = format_items.copy()

    if "is_active" in dict_df.columns:
        dict_df["is_active"] = to_bool(dict_df["is_active"])
        dict_df = dict_df[dict_df["is_active"]]

    merged = fi_df.merge(
        dict_df[["dict_id", "item_id", "item_name"]],
        on=["dict_id", "item_id"],
        how="left",
    )

    agg = (
        merged.groupby(["format_id", "dict_id"], dropna=False)["item_name"]
        .apply(lambda s: sorted({str(x).strip() for x in s.dropna() if str(x).strip()}))
        .reset_index()
    )

    pivot = agg.pivot(index="format_id", columns="dict_id", values="item_name").reset_index()

    for col in pivot.columns:
        if col != "format_id":
            pivot[col] = pivot[col].apply(lambda x: x if isinstance(x, list) else [])

    return pivot


def calc_discounted_price(price_series: pd.Series, discount_series: pd.Series) -> pd.Series:
    price = pd.to_numeric(price_series, errors="coerce")
    discount = pd.to_numeric(discount_series, errors="coerce").fillna(0)
    return price * (1 - discount)


def calculate_ecpm(row: pd.Series) -> Optional[float]:
    discount = row.get("discount", 0)
    cpm = row.get("cpm_avg")
    cpc = row.get("cpc_avg")
    cpv = row.get("cpv_avg")
    ctr = row.get("ctr_avg")
    vtr = row.get("vtr_avg")

    cpm_val = pd.to_numeric(pd.Series([cpm]), errors="coerce").iloc[0]
    cpc_val = pd.to_numeric(pd.Series([cpc]), errors="coerce").iloc[0]
    cpv_val = pd.to_numeric(pd.Series([cpv]), errors="coerce").iloc[0]
    ctr_val = pd.to_numeric(pd.Series([ctr]), errors="coerce").iloc[0]
    vtr_val = pd.to_numeric(pd.Series([vtr]), errors="coerce").iloc[0]
    discount_val = pd.to_numeric(pd.Series([discount]), errors="coerce").fillna(0).iloc[0]

    if not pd.isna(cpm_val):
        return float(cpm_val * (1 - discount_val))

    if not pd.isna(cpc_val) and not pd.isna(ctr_val):
        return float(cpc_val * (1 - discount_val) * ctr_val * 1000)

    if not pd.isna(cpv_val) and not pd.isna(vtr_val):
        return float(cpv_val * (1 - discount_val) * vtr_val * 1000)

    return np.nan


def enrich_formats(
    formats: pd.DataFrame,
    dict_items: pd.DataFrame,
    format_items: pd.DataFrame,
) -> pd.DataFrame:
    base = preprocess_formats(formats)
    dict_pivot = build_dict_aggregates(format_items, dict_items)

    df = base.merge(dict_pivot, on="format_id", how="left")

    dict_columns = [col for col in dict_pivot.columns if col != "format_id"]
    for col in dict_columns:
        if col not in df.columns:
            df[col] = [[] for _ in range(len(df))]
        else:
            df[col] = df[col].apply(lambda x: x if isinstance(x, list) else [])

    df["ecpm_discounted"] = df.apply(calculate_ecpm, axis=1)

    return df


# =========================
# Фильтрация
# =========================

def apply_filters(df: pd.DataFrame, state: Dict) -> pd.DataFrame:
    result = df.copy()

    # Категориальные
    category_filters = {
        "platform": state.get("platforms", []),
        "type_service": state.get("service_types", []),
        "buy_model": state.get("buy_models", []),
    }
    for col, values in category_filters.items():
        if values:
            result = result[result[col].isin(values)]

    # Булевы ограничения
    bool_filters = {
        "verification_pixel": state.get("need_verification_pixel", False),
        "verification_js": state.get("need_verification_js", False),
        "bls": state.get("need_bls", False),
        "sales_lift": state.get("need_sales_lift", False),
    }
    for col, enabled in bool_filters.items():
        if enabled:
            result = result[result[col] == True]

    # Теги из словареи
    tag_filter_map = {
        "format_type": state.get("filter_format_type", []),
        "device": state.get("filter_device", []),
        "placement": state.get("filter_placement", []),
        "display": state.get("filter_display", []),
        "dmp": state.get("filter_dmp", []),
        "targeting": state.get("filter_targeting", []),
        "targeting_markup": state.get("filter_targeting_markup", []),
        "production": state.get("filter_production", []),
        "other_markup": state.get("filter_other_markup", []),
        "instream_pos": state.get("filter_instream_pos", []),
    }

    for col, selected_tags in tag_filter_map.items():
        if col in result.columns and selected_tags:
            selected_set = set(selected_tags)
            result = result[result[col].apply(lambda tags: selected_set.issubset(set(tags or [])))]

    # Числовые пороги
    numeric_thresholds = {
        "max_reach": state.get("min_reach"),
        "min_budget": state.get("max_budget"),
        "ctr_avg": state.get("min_ctr"),
        "vtr_avg": state.get("min_vtr"),
        "viewability_avg": state.get("min_viewability"),
        "ecpm_discounted": state.get("max_ecpm"),
        "commission": state.get("max_commission"),
    }

    if numeric_thresholds["max_reach"] is not None:
        result = result[result["max_reach"].fillna(-np.inf) >= numeric_thresholds["max_reach"]]

    if numeric_thresholds["max_budget"] is not None:
        result = result[result["min_budget"].fillna(np.inf) <= numeric_thresholds["max_budget"]]

    if numeric_thresholds["min_ctr"] is not None:
        result = result[result["ctr_avg"].fillna(-np.inf) >= numeric_thresholds["min_ctr"]]

    if numeric_thresholds["min_vtr"] is not None:
        result = result[result["vtr_avg"].fillna(-np.inf) >= numeric_thresholds["min_vtr"]]

    if numeric_thresholds["min_viewability"] is not None:
        result = result[result["viewability_avg"].fillna(-np.inf) >= numeric_thresholds["min_viewability"]]

    if numeric_thresholds["max_ecpm"] is not None:
        result = result[result["ecpm_discounted"].fillna(np.inf) <= numeric_thresholds["max_ecpm"]]

    if numeric_thresholds["max_commission"] is not None:
        result = result[result["commission"].fillna(np.inf) <= numeric_thresholds["max_commission"]]

    return result


# =========================
# Скоринг
# =========================

def compute_score(df: pd.DataFrame, weights: Dict[str, float]) -> pd.DataFrame:
    result = df.copy()

    norm_reach = safe_ratio_minmax(result["max_reach"])
    norm_ecpm = safe_inverse_minmax(result["ecpm_discounted"])
    norm_ctr = safe_ratio_minmax(result["ctr_avg"])
    norm_vtr = safe_ratio_minmax(result["vtr_avg"])
    norm_viewability = safe_ratio_minmax(result["viewability_avg"])
    norm_commission = safe_ratio_minmax(result["commission"])

    result["score"] = (
        norm_reach.fillna(0) * weights["max_reach"] +
        norm_ecpm.fillna(0) * weights["ecpm_discounted"] +
        norm_ctr.fillna(0) * weights["ctr_avg"] +
        norm_vtr.fillna(0) * weights["vtr_avg"] +
        norm_viewability.fillna(0) * weights["viewability_avg"] +
        norm_commission.fillna(0) * weights["commission"]
    )

    return result


# =========================
# UI: сайдбар и состояние
# =========================

def get_all_tag_values(df: pd.DataFrame, column_name: str) -> List[str]:
    if column_name not in df.columns:
        return []
    values = set()
    for items in df[column_name]:
        if isinstance(items, list):
            values.update([str(x) for x in items if str(x).strip()])
    return sorted(values)


def init_weight_state():
    for key, value in DEFAULT_WEIGHTS.items():
        if f"weight_{key}" not in st.session_state:
            st.session_state[f"weight_{key}"] = value


def reset_weights():
    for key, value in DEFAULT_WEIGHTS.items():
        st.session_state[f"weight_{key}"] = value


def normalize_weight_state():
    current = {
        "max_reach": st.session_state.get("weight_max_reach", 0),
        "ecpm_discounted": st.session_state.get("weight_ecpm_discounted", 0),
        "ctr_avg": st.session_state.get("weight_ctr_avg", 0),
        "vtr_avg": st.session_state.get("weight_vtr_avg", 0),
        "viewability_avg": st.session_state.get("weight_viewability_avg", 0),
        "commission": st.session_state.get("weight_commission", 0),
    }
    normalized = normalize_weights(current)
    st.session_state["weight_max_reach"] = normalized["max_reach"]
    st.session_state["weight_ecpm_discounted"] = normalized["ecpm_discounted"]
    st.session_state["weight_ctr_avg"] = normalized["ctr_avg"]
    st.session_state["weight_vtr_avg"] = normalized["vtr_avg"]
    st.session_state["weight_viewability_avg"] = normalized["viewability_avg"]
    st.session_state["weight_commission"] = normalized["commission"]


def render_sidebar(df: pd.DataFrame) -> Tuple[Dict, Dict[str, int], bool]:
    st.sidebar.header("Фильтры")

    filters = {}

    filters["platforms"] = st.sidebar.multiselect(
        "Платформа",
        options=sorted(df["platform"].dropna().unique().tolist()),
    )

    filters["service_types"] = st.sidebar.multiselect(
        "Тип сервиса",
        options=sorted(df["type_service"].dropna().unique().tolist()),
    )

    filters["buy_models"] = st.sidebar.multiselect(
        "Модель закупки",
        options=sorted(df["buy_model"].dropna().unique().tolist()),
    )

    st.sidebar.subheader("Логические ограничения")
    filters["need_verification_pixel"] = st.sidebar.checkbox("Нужна верификация Pixel")
    filters["need_verification_js"] = st.sidebar.checkbox("Нужна верификация JS")
    filters["need_bls"] = st.sidebar.checkbox("Требуется BLS")
    filters["need_sales_lift"] = st.sidebar.checkbox("Требуется Sales Lift")

    st.sidebar.subheader("Таргетинги и параметры")
    filters["filter_format_type"] = st.sidebar.multiselect(
        "Тип формата",
        options=get_all_tag_values(df, "format_type"),
    )
    filters["filter_device"] = st.sidebar.multiselect(
        "Устроиство",
        options=get_all_tag_values(df, "device"),
    )
    filters["filter_placement"] = st.sidebar.multiselect(
        "Размещение",
        options=get_all_tag_values(df, "placement"),
    )
    filters["filter_display"] = st.sidebar.multiselect(
        "Тип размещения креатива",
        options=get_all_tag_values(df, "display"),
    )
    filters["filter_dmp"] = st.sidebar.multiselect(
        "DMP / данные",
        options=get_all_tag_values(df, "dmp"),
    )
    filters["filter_targeting"] = st.sidebar.multiselect(
        "Таргетинги",
        options=get_all_tag_values(df, "targeting"),
    )
    filters["filter_targeting_markup"] = st.sidebar.multiselect(
        "Таргетинги с наценкой",
        options=get_all_tag_values(df, "targeting_markup"),
    )
    filters["filter_production"] = st.sidebar.multiselect(
        "Продакшн",
        options=get_all_tag_values(df, "production"),
    )
    filters["filter_other_markup"] = st.sidebar.multiselect(
        "Дополнительные надбавки",
        options=get_all_tag_values(df, "other_markup"),
    )
    filters["filter_instream_pos"] = st.sidebar.multiselect(
        "Позиция в потоке",
        options=get_all_tag_values(df, "instream_pos"),
    )

    st.sidebar.subheader("Числовые пороги")
    filters["min_reach"] = st.sidebar.number_input("Минимальныи охват", min_value=0, value=0, step=10000)
    filters["max_budget"] = st.sidebar.number_input("Максимальныи минимальныи бюджет", min_value=0, value=0, step=10000)
    filters["min_ctr"] = st.sidebar.number_input("Минимальныи CTR", min_value=0.0, value=0.0, step=0.001, format="%.3f")
    filters["min_vtr"] = st.sidebar.number_input("Минимальныи VTR", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    filters["min_viewability"] = st.sidebar.number_input("Минимальныи Viewability", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    filters["max_ecpm"] = st.sidebar.number_input("Максимальныи eCPM", min_value=0.0, value=0.0, step=10.0, format="%.2f")
    filters["max_commission"] = st.sidebar.number_input("Максимальныи Commission", min_value=0.0, value=0.0, step=0.01, format="%.2f")

    for key in ["max_budget", "min_ctr", "min_vtr", "min_viewability", "max_ecpm", "max_commission"]:
        if filters[key] == 0:
            filters[key] = None
    if filters["min_reach"] == 0:
        filters["min_reach"] = None

    st.sidebar.divider()
    st.sidebar.header("Скоринг")

    scoring_enabled = st.sidebar.checkbox("Включить скоринг", value=True)

    init_weight_state()

    st.sidebar.number_input("Вес: максимальныи охват", min_value=0, max_value=100, key="weight_max_reach")
    st.sidebar.number_input("Вес: eCPM со скидкои", min_value=0, max_value=100, key="weight_ecpm_discounted")
    st.sidebar.number_input("Вес: CTR", min_value=0, max_value=100, key="weight_ctr_avg")
    st.sidebar.number_input("Вес: VTR", min_value=0, max_value=100, key="weight_vtr_avg")
    st.sidebar.number_input("Вес: Viewability", min_value=0, max_value=100, key="weight_viewability_avg")
    st.sidebar.number_input("Вес: Commission", min_value=0, max_value=100, key="weight_commission")

    col_a, col_b = st.sidebar.columns(2)
    with col_a:
        if st.button("Нормализовать веса"):
            normalize_weight_state()
    with col_b:
        if st.button("Сбросить веса"):
            reset_weights()

    weights = {
        "max_reach": int(st.session_state["weight_max_reach"]),
        "ecpm_discounted": int(st.session_state["weight_ecpm_discounted"]),
        "ctr_avg": int(st.session_state["weight_ctr_avg"]),
        "vtr_avg": int(st.session_state["weight_vtr_avg"]),
        "viewability_avg": int(st.session_state["weight_viewability_avg"]),
        "commission": int(st.session_state["weight_commission"]),
    }

    total_weight = sum(weights.values())
    st.sidebar.caption(f"Сумма весов: {total_weight}")

    return filters, weights, scoring_enabled


# =========================
# UI: таблица и карточка
# =========================

def build_table_view(df: pd.DataFrame, scoring_applied: bool) -> pd.DataFrame:
    table_df = df.copy()

    show_columns = [
        "format_id",
        "platform",
        "format_name",
        "type_service",
        "buy_model",
        "max_reach",
        "min_budget",
        "ecpm_discounted",
        "ctr_avg",
        "vtr_avg",
        "viewability_avg",
        "commission",
    ]

    if scoring_applied:
        show_columns.insert(0, "score")

    table_df = table_df[show_columns].copy()
    table_df.insert(0, "Выбрать", False)

    rename_map = {col: get_column_label(col) for col in table_df.columns if col != "Выбрать"}
    table_df = table_df.rename(columns=rename_map)

    return table_df


def render_table_selection(table_df: pd.DataFrame, source_df: pd.DataFrame) -> Optional[pd.Series]:
    edited = st.data_editor(
        table_df,
        hide_index=True,
        use_container_width=True,
        disabled=[col for col in table_df.columns if col != "Выбрать"],
        column_config={
            "Выбрать": st.column_config.CheckboxColumn(required=False),
        },
    )

    selected_rows = edited[edited["Выбрать"] == True]

    if selected_rows.empty:
        return None

    selected_format_id = selected_rows.iloc[0][get_column_label("format_id")]
    match = source_df[source_df["format_id"] == selected_format_id]

    if match.empty:
        return None

    return match.iloc[0]


def render_tag_section(title: str, values: List[str]):
    if values:
        st.markdown(f"**{title}:** {', '.join(values)}")


def render_format_card(row: pd.Series):
    st.subheader("Карточка формата")

    st.markdown(f"### {row.get('format_name', 'Без названия')}")
    st.markdown(f"**ID:** {row.get('format_id', '—')}")
    st.markdown(f"**Платформа:** {row.get('platform', '—')}")
    st.markdown(f"**Тип сервиса:** {row.get('type_service', '—')}")
    st.markdown(f"**Модель закупки:** {row.get('buy_model', '—')}")

    st.markdown("#### Описание")
    st.write(row.get("description") or "—")

    st.markdown("#### Ключевые параметры")
    metrics = pd.DataFrame(
        [
            ("Максимальныи охват", format_number(row.get("max_reach"), 0)),
            ("Минимальныи бюджет", format_number(row.get("min_budget"), 0)),
            ("Скидка", format_percent(row.get("discount"))),
            ("eCPM с учетом скидки", format_number(row.get("ecpm_discounted"))),
            ("Commission", format_percent(row.get("commission"))),
            ("CTR avg", format_percent(row.get("ctr_avg"))),
            ("VTR avg", format_percent(row.get("vtr_avg"))),
            ("Viewability avg", format_percent(row.get("viewability_avg"))),
            ("Верификация Pixel", format_bool(row.get("verification_pixel"))),
            ("Верификация JS", format_bool(row.get("verification_js"))),
            ("BLS", format_bool(row.get("bls"))),
            ("Sales Lift", format_bool(row.get("sales_lift"))),
        ],
        columns=["Параметр", "Значение"],
    )
    st.dataframe(metrics, hide_index=True, use_container_width=True)

    st.markdown("#### Параметры словареи")
    for dict_id, title in DICT_LABELS.items():
        if dict_id in row.index:
            values = row.get(dict_id, [])
            if isinstance(values, list):
                render_tag_section(title, values)

    st.markdown("#### Условия и надбавки")
    info_fields = {
        "Условия верификации": row.get("verification_terms"),
        "Условия BLS": row.get("bls_terms"),
        "Условия Sales Lift": row.get("sales_lift_terms"),
        "Условия сезонности": row.get("seasonality_terms"),
    }
    for title, value in info_fields.items():
        if pd.notna(value) and str(value).strip():
            st.markdown(f"**{title}:** {value}")

    st.markdown("#### Ссылки")
    link_fields = {
        "Пример": row.get("example_url"),
        "Технические требования": row.get("technical_requirements_url"),
        "Медиакит": row.get("mediakit_url"),
        "Кейсы": row.get("cases_url"),
    }
    for title, url in link_fields.items():
        if pd.notna(url) and str(url).strip():
            st.markdown(f"- [{title}]({url})")


# =========================
# Основнои сценарии
# =========================

def main():
    st.title("Подбор рекламных форматов")

    try:
        formats, dict_items, format_items = load_data()
        df = enrich_formats(formats, dict_items, format_items)
    except Exception as e:
        st.error(f"Ошибка загрузки данных: {e}")
        st.stop()

    filters, weights, scoring_enabled = render_sidebar(df)

    filtered_df = apply_filters(df, filters)

    total_weight = sum(weights.values())
    scoring_applied = scoring_enabled and total_weight == 100

    if scoring_enabled and total_weight != 100:
        st.warning("Скоринг не применен: сумма весов должна быть равна 100.")

    if scoring_applied:
        filtered_df = compute_score(filtered_df, weights).sort_values(
            by=["score", "ecpm_discounted"],
            ascending=[False, True],
            na_position="last",
        )
    else:
        filtered_df = filtered_df.sort_values(
            by=["platform", "format_name"],
            ascending=[True, True],
            na_position="last",
        )

    st.caption(f"Наидено форматов: {len(filtered_df)}")

    table_df = build_table_view(filtered_df, scoring_applied=scoring_applied)
    selected_row = render_table_selection(table_df, filtered_df)

    if selected_row is not None:
        render_format_card(selected_row)
    else:
        st.info("Выберите один формат в таблице, чтобы открыть карточку.")

    with st.expander("Технические примечания"):
        st.write(
            """
            - eCPM считает скидку, но не учитывает commission.
            - Для CPM используется discounted CPM.
            - Для CPC используется формула: CPC × CTR × 1000 с учетом скидки.
            - Для CPV добавлена поддержка на случаи, если в данных есть такая модель: CPV × VTR × 1000 с учетом скидки.
            - Фильтры применяются раньше скоринга.
            """
        )


if __name__ == "__main__":
    main()
