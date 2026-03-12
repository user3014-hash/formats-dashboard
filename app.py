import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Подбор рекламных форматов", layout="wide")

APP_DIR = Path(__file__).resolve().parent

FORMATS_CSV = "DataLens - formats.csv"
DICT_ITEMS_CSV = "DataLens - dict_items.csv"
FORMAT_ITEMS_CSV = "DataLens - format_items.csv"
FALLBACK_XLSX = "DataLens.xlsx"

DEFAULT_WEIGHTS = {
    "max_reach": 25,
    "ecpm_discounted": 25,
    "ctr_avg": 15,
    "vtr_avg": 15,
    "viewability_avg": 10,
    "commission": 10,
}

DICT_LABELS = {
    "format_type": "Тип формата",
    "device": "Устройство",
    "display": "Показ креатива",
    "dmp": "Данные и сегменты",
    "instream_pos": "Позиция в потоке",
    "other_markup": "Дополнительные наценки",
    "placement": "Размещение",
    "production": "Продакшн",
    "targeting": "Таргетинги",
    "targeting_markup": "Таргетинги с наценкой",
    "seasonality_coeff": "Сезонность",
}

COLUMN_LABELS = {
    "format_id": "ID формата",
    "type_service": "Тип сервиса",
    "platform": "Площадка",
    "format_name": "Формат",
    "example_url": "Пример размещения",
    "description": "Описание",
    "max_reach": "Максимальный охват",
    "min_budget": "Минимальный бюджет",
    "discount": "Скидка",
    "buy_model": "Модель закупки",
    "cpm_min": "CPM, минимум",
    "cpm_max": "CPM, максимум",
    "cpm_avg": "CPM, среднее",
    "cpc_min": "CPC, минимум",
    "cpc_max": "CPC, максимум",
    "cpc_avg": "CPC, среднее",
    "cpv_min": "CPV, минимум",
    "cpv_max": "CPV, максимум",
    "cpv_avg": "CPV, среднее",
    "ctr_min": "CTR, минимум",
    "ctr_max": "CTR, максимум",
    "ctr_avg": "CTR, среднее",
    "vtr_min": "VTR, минимум",
    "vtr_max": "VTR, максимум",
    "vtr_avg": "VTR, среднее",
    "viewability_min": "Viewability, минимум",
    "viewability_max": "Viewability, максимум",
    "viewability_avg": "Viewability, среднее",
    "verification_pixel": "Поддержка Pixel",
    "verification_js": "Поддержка JS",
    "verification_terms": "Условия верификации",
    "commission": "Комиссия",
    "bls": "BLS",
    "sales_lift": "Sales Lift",
    "bls_terms": "Условия BLS",
    "sales_lift_terms": "Условия Sales Lift",
    "seasonality_terms": "Условия сезонности",
    "technical_requirements_url": "Технические требования",
    "mediakit_url": "Медиакит",
    "cases_url": "Кейсы",
    "ecpm_discounted": "eCPM с учетом скидки",
    "score": "Скоринг",
}


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


def safe_read_table(path_csv: Path, fallback_xlsx: Path, sheet_name: str) -> pd.DataFrame:
    if path_csv.exists():
        return pd.read_csv(path_csv)
    if fallback_xlsx.exists():
        return pd.read_excel(fallback_xlsx, sheet_name=sheet_name)
    raise FileNotFoundError(
        f"Не найден источник данных: {path_csv.name} или лист {sheet_name} в {fallback_xlsx.name}"
    )


def to_float(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .replace(
            {
                "": np.nan,
                "nan": np.nan,
                "None": np.nan,
                "null": np.nan,
                "NULL": np.nan,
            }
        )
    )
    return pd.to_numeric(cleaned, errors="coerce")


def to_bool(series: pd.Series) -> pd.Series:
    true_values = {"true", "1", "да", "yes", "y", "истина"}
    false_values = {"false", "0", "нет", "no", "n", "ложь"}

    def convert(value):
        if pd.isna(value):
            return False
        if isinstance(value, bool):
            return value
        text = str(value).strip().lower()
        if text in true_values:
            return True
        if text in false_values:
            return False
        return False

    return series.apply(convert).astype(bool)


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
    return "Да" if bool(value) else "Нет"


def get_label(column_name: str) -> str:
    return COLUMN_LABELS.get(column_name, DICT_LABELS.get(column_name, column_name))


def normalize_weights(weights: Dict[str, float]) -> Dict[str, int]:
    total = sum(max(0.0, float(v)) for v in weights.values())
    if total <= 0:
        return DEFAULT_WEIGHTS.copy()

    scaled = {k: (max(0.0, float(v)) / total) * 100 for k, v in weights.items()}
    rounded = {k: int(math.floor(v)) for k, v in scaled.items()}

    remainder = 100 - sum(rounded.values())
    if remainder > 0:
        order = sorted(
            scaled.keys(),
            key=lambda key: scaled[key] - math.floor(scaled[key]),
            reverse=True,
        )
        for i in range(remainder):
            rounded[order[i % len(order)]] += 1

    return rounded


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

    possible_name_cols = ["item_name", "name", "value", "title"]
    item_name_col = next((col for col in possible_name_cols if col in dict_df.columns), None)
    if item_name_col is None:
        raise KeyError("В dict_items не найден столбец с названием элемента словаря")

    merged = fi_df.merge(
        dict_df[["dict_id", "item_id", item_name_col]].rename(columns={item_name_col: "item_name"}),
        on=["dict_id", "item_id"],
        how="left",
    )

    grouped = (
        merged.groupby(["format_id", "dict_id"], dropna=False)["item_name"]
        .apply(lambda s: sorted({str(x).strip() for x in s.dropna() if str(x).strip()}))
        .reset_index()
    )

    pivot = grouped.pivot(index="format_id", columns="dict_id", values="item_name").reset_index()

    for col in pivot.columns:
        if col != "format_id":
            pivot[col] = pivot[col].apply(lambda x: x if isinstance(x, list) else [])

    return pivot


def calculate_ecpm(row: pd.Series) -> float:
    discount = row.get("discount", 0)
    cpm = row.get("cpm_avg")
    cpc = row.get("cpc_avg")
    cpv = row.get("cpv_avg")
    ctr = row.get("ctr_avg")
    vtr = row.get("vtr_avg")

    discount_val = pd.to_numeric(pd.Series([discount]), errors="coerce").fillna(0).iloc[0]
    cpm_val = pd.to_numeric(pd.Series([cpm]), errors="coerce").iloc[0]
    cpc_val = pd.to_numeric(pd.Series([cpc]), errors="coerce").iloc[0]
    cpv_val = pd.to_numeric(pd.Series([cpv]), errors="coerce").iloc[0]
    ctr_val = pd.to_numeric(pd.Series([ctr]), errors="coerce").iloc[0]
    vtr_val = pd.to_numeric(pd.Series([vtr]), errors="coerce").iloc[0]

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
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x if isinstance(x, list) else [])
        else:
            df[col] = [[] for _ in range(len(df))]

    df["ecpm_discounted"] = df.apply(calculate_ecpm, axis=1)

    return df


def get_all_tag_values(df: pd.DataFrame, column_name: str) -> List[str]:
    if column_name not in df.columns:
        return []
    values = set()
    for items in df[column_name]:
        if isinstance(items, list):
            values.update([str(x) for x in items if str(x).strip()])
    return sorted(values)


def apply_filters(df: pd.DataFrame, state: Dict) -> pd.DataFrame:
    result = df.copy()

    category_filters = {
        "platform": state.get("platforms", []),
        "type_service": state.get("service_types", []),
        "buy_model": state.get("buy_models", []),
    }
    for col, values in category_filters.items():
        if col in result.columns and values:
            result = result[result[col].isin(values)]

    bool_filters = {
        "verification_pixel": state.get("need_verification_pixel", False),
        "verification_js": state.get("need_verification_js", False),
        "bls": state.get("need_bls", False),
        "sales_lift": state.get("need_sales_lift", False),
    }
    for col, enabled in bool_filters.items():
        if col in result.columns and enabled:
            result = result[result[col] == True]

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

    numeric_thresholds = {
        "min_reach": state.get("min_reach"),
        "min_ctr": state.get("min_ctr"),
        "min_vtr": state.get("min_vtr"),
        "min_viewability": state.get("min_viewability"),
        "max_ecpm": state.get("max_ecpm"),
        "max_commission": state.get("max_commission"),
    }

    if numeric_thresholds["min_reach"] is not None and "max_reach" in result.columns:
        result = result[result["max_reach"].fillna(-np.inf) >= numeric_thresholds["min_reach"]]

    if numeric_thresholds["min_ctr"] is not None and "ctr_avg" in result.columns:
        result = result[result["ctr_avg"].fillna(-np.inf) >= numeric_thresholds["min_ctr"]]

    if numeric_thresholds["min_vtr"] is not None and "vtr_avg" in result.columns:
        result = result[result["vtr_avg"].fillna(-np.inf) >= numeric_thresholds["min_vtr"]]

    if numeric_thresholds["min_viewability"] is not None and "viewability_avg" in result.columns:
        result = result[result["viewability_avg"].fillna(-np.inf) >= numeric_thresholds["min_viewability"]]

    if numeric_thresholds["max_ecpm"] is not None and "ecpm_discounted" in result.columns:
        result = result[result["ecpm_discounted"].fillna(np.inf) <= numeric_thresholds["max_ecpm"]]

    if numeric_thresholds["max_commission"] is not None and "commission" in result.columns:
        result = result[result["commission"].fillna(np.inf) <= numeric_thresholds["max_commission"]]

    return result


def compute_score(df: pd.DataFrame, weights: Dict[str, float]) -> pd.DataFrame:
    result = df.copy()

    reach_score = safe_ratio_minmax(result["max_reach"]) if "max_reach" in result.columns else 0
    ecpm_score = safe_inverse_minmax(result["ecpm_discounted"]) if "ecpm_discounted" in result.columns else 0
    ctr_score = safe_ratio_minmax(result["ctr_avg"]) if "ctr_avg" in result.columns else 0
    vtr_score = safe_ratio_minmax(result["vtr_avg"]) if "vtr_avg" in result.columns else 0
    viewability_score = safe_ratio_minmax(result["viewability_avg"]) if "viewability_avg" in result.columns else 0
    commission_score = safe_ratio_minmax(result["commission"]) if "commission" in result.columns else 0

    result["score"] = (
        reach_score * weights["max_reach"]
        + ecpm_score * weights["ecpm_discounted"]
        + ctr_score * weights["ctr_avg"]
        + vtr_score * weights["vtr_avg"]
        + viewability_score * weights["viewability_avg"]
        + commission_score * weights["commission"]
    )

    return result


def init_weight_state() -> None:
    for key, value in DEFAULT_WEIGHTS.items():
        session_key = f"weight_{key}"
        if session_key not in st.session_state:
            st.session_state[session_key] = value


def reset_weights() -> None:
    for key, value in DEFAULT_WEIGHTS.items():
        st.session_state[f"weight_{key}"] = value


def normalize_weight_state() -> None:
    current = {
        "max_reach": st.session_state.get("weight_max_reach", 0),
        "ecpm_discounted": st.session_state.get("weight_ecpm_discounted", 0),
        "ctr_avg": st.session_state.get("weight_ctr_avg", 0),
        "vtr_avg": st.session_state.get("weight_vtr_avg", 0),
        "viewability_avg": st.session_state.get("weight_viewability_avg", 0),
        "commission": st.session_state.get("weight_commission", 0),
    }
    normalized = normalize_weights(current)
    for key, value in normalized.items():
        st.session_state[f"weight_{key}"] = value


def render_sidebar(df: pd.DataFrame) -> Tuple[Dict, Dict[str, int], bool]:
    st.sidebar.header("Фильтры")

    filters: Dict[str, Optional[float] | List[str] | bool] = {}

    filters["platforms"] = st.sidebar.multiselect(
        "Площадка",
        options=sorted(df["platform"].dropna().unique().tolist()) if "platform" in df.columns else [],
        placeholder="",
    )

    filters["service_types"] = st.sidebar.multiselect(
        "Тип сервиса",
        options=sorted(df["type_service"].dropna().unique().tolist()) if "type_service" in df.columns else [],
        placeholder="",
    )

    filters["buy_models"] = st.sidebar.multiselect(
        "Модель закупки",
        options=sorted(df["buy_model"].dropna().unique().tolist()) if "buy_model" in df.columns else [],
        placeholder="",
    )

    st.sidebar.subheader("Дополнительные требования")

    filters["need_verification_pixel"] = st.sidebar.checkbox("Нужна поддержка Pixel")
    filters["need_verification_js"] = st.sidebar.checkbox("Нужна поддержка JS")
    filters["need_bls"] = st.sidebar.checkbox("Нужен BLS")
    filters["need_sales_lift"] = st.sidebar.checkbox("Нужен Sales Lift")

    st.sidebar.subheader("Параметры и таргетинги")

    filters["filter_format_type"] = st.sidebar.multiselect(
        "Тип формата",
        options=get_all_tag_values(df, "format_type"),
        placeholder="",
    )
    filters["filter_device"] = st.sidebar.multiselect(
        "Устройство",
        options=get_all_tag_values(df, "device"),
        placeholder="",
    )
    filters["filter_placement"] = st.sidebar.multiselect(
        "Размещение",
        options=get_all_tag_values(df, "placement"),
        placeholder="",
    )
    filters["filter_display"] = st.sidebar.multiselect(
        "Показ креатива",
        options=get_all_tag_values(df, "display"),
        placeholder="",
    )
    filters["filter_dmp"] = st.sidebar.multiselect(
        "Данные и сегменты",
        options=get_all_tag_values(df, "dmp"),
        placeholder="",
    )
    filters["filter_targeting"] = st.sidebar.multiselect(
        "Таргетинги",
        options=get_all_tag_values(df, "targeting"),
        placeholder="",
    )
    filters["filter_targeting_markup"] = st.sidebar.multiselect(
        "Таргетинги с наценкой",
        options=get_all_tag_values(df, "targeting_markup"),
        placeholder="",
    )
    filters["filter_production"] = st.sidebar.multiselect(
        "Продакшн",
        options=get_all_tag_values(df, "production"),
        placeholder="",
    )
    filters["filter_other_markup"] = st.sidebar.multiselect(
        "Дополнительные наценки",
        options=get_all_tag_values(df, "other_markup"),
        placeholder="",
    )
    filters["filter_instream_pos"] = st.sidebar.multiselect(
        "Позиция в потоке",
        options=get_all_tag_values(df, "instream_pos"),
        placeholder="",
    )

    st.sidebar.subheader("Пороговые значения")

    filters["min_reach"] = st.sidebar.number_input(
        "Минимальный охват",
        min_value=0,
        value=0,
        step=10000,
    )
    filters["min_ctr"] = st.sidebar.number_input(
        "Минимальный CTR",
        min_value=0.0,
        value=0.0,
        step=0.001,
        format="%.3f",
    )
    filters["min_vtr"] = st.sidebar.number_input(
        "Минимальный VTR",
        min_value=0.0,
        value=0.0,
        step=0.01,
        format="%.2f",
    )
    filters["min_viewability"] = st.sidebar.number_input(
        "Минимальный Viewability",
        min_value=0.0,
        value=0.0,
        step=0.01,
        format="%.2f",
    )
    filters["max_ecpm"] = st.sidebar.number_input(
        "Максимальный eCPM",
        min_value=0.0,
        value=0.0,
        step=10.0,
        format="%.2f",
    )
    filters["max_commission"] = st.sidebar.number_input(
        "Максимальная комиссия",
        min_value=0.0,
        value=0.0,
        step=0.01,
        format="%.2f",
    )

    if filters["min_reach"] == 0:
        filters["min_reach"] = None
    for key in ["min_ctr", "min_vtr", "min_viewability", "max_ecpm", "max_commission"]:
        if filters[key] == 0:
            filters[key] = None

    st.sidebar.divider()
    st.sidebar.header("Скоринг")

    scoring_enabled = st.sidebar.checkbox("Включить скоринг", value=True)

    init_weight_state()

    st.sidebar.number_input("Вес: максимальный охват", min_value=0, max_value=100, key="weight_max_reach")
    st.sidebar.number_input("Вес: eCPM с учетом скидки", min_value=0, max_value=100, key="weight_ecpm_discounted")
    st.sidebar.number_input("Вес: CTR", min_value=0, max_value=100, key="weight_ctr_avg")
    st.sidebar.number_input("Вес: VTR", min_value=0, max_value=100, key="weight_vtr_avg")
    st.sidebar.number_input("Вес: Viewability", min_value=0, max_value=100, key="weight_viewability_avg")
    st.sidebar.number_input("Вес: комиссия", min_value=0, max_value=100, key="weight_commission")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Нормализовать"):
            normalize_weight_state()
    with col2:
        if st.button("Сбросить"):
            reset_weights()

    weights = {
        "max_reach": int(st.session_state["weight_max_reach"]),
        "ecpm_discounted": int(st.session_state["weight_ecpm_discounted"]),
        "ctr_avg": int(st.session_state["weight_ctr_avg"]),
        "vtr_avg": int(st.session_state["weight_vtr_avg"]),
        "viewability_avg": int(st.session_state["weight_viewability_avg"]),
        "commission": int(st.session_state["weight_commission"]),
    }

    st.sidebar.caption(f"Сумма весов: {sum(weights.values())}")

    return filters, weights, scoring_enabled


def build_table_view(df: pd.DataFrame, scoring_applied: bool) -> pd.DataFrame:
    columns = [
        "format_id",
        "platform",
        "format_name",
        "type_service",
        "buy_model",
        "max_reach",
        "ecpm_discounted",
        "ctr_avg",
        "vtr_avg",
        "viewability_avg",
        "commission",
    ]

    if scoring_applied and "score" in df.columns:
        columns = ["score"] + columns

    existing_columns = [col for col in columns if col in df.columns]

    table_df = df[existing_columns].copy()
    table_df.insert(0, "Выбрать", False)

    rename_map = {col: get_label(col) for col in existing_columns}
    table_df = table_df.rename(columns=rename_map)

    return table_df


def render_table_selection(table_df: pd.DataFrame, source_df: pd.DataFrame) -> Optional[pd.Series]:
    disabled_columns = [col for col in table_df.columns if col != "Выбрать"]

    edited = st.data_editor(
        table_df,
        hide_index=True,
        use_container_width=True,
        disabled=disabled_columns,
        column_config={
            "Выбрать": st.column_config.CheckboxColumn("Выбрать"),
        },
    )

    selected_rows = edited[edited["Выбрать"] == True]

    if selected_rows.empty:
        return None

    format_id_label = get_label("format_id")
    selected_format_id = selected_rows.iloc[0][format_id_label]

    match = source_df[source_df["format_id"] == selected_format_id]
    if match.empty:
        return None

    return match.iloc[0]


def render_tag_line(title: str, values: List[str]) -> None:
    if values:
        st.markdown(f"**{title}:** {', '.join(values)}")


def render_format_card(row: pd.Series) -> None:
    st.subheader("Карточка формата")

    st.markdown(f"### {row.get('format_name', 'Без названия')}")
    st.markdown(f"**ID:** {row.get('format_id', '—')}")
    st.markdown(f"**Площадка:** {row.get('platform', '—')}")
    st.markdown(f"**Тип сервиса:** {row.get('type_service', '—')}")
    st.markdown(f"**Модель закупки:** {row.get('buy_model', '—')}")

    st.markdown("#### Описание")
    st.write(row.get("description") or "—")

    st.markdown("#### Основные показатели")
    metrics = pd.DataFrame(
        [
            ("Максимальный охват", format_number(row.get("max_reach"), 0)),
            ("Минимальный бюджет", format_number(row.get("min_budget"), 0)),
            ("Скидка", format_percent(row.get("discount"))),
            ("eCPM с учетом скидки", format_number(row.get("ecpm_discounted"))),
            ("Комиссия", format_percent(row.get("commission"))),
            ("CTR, среднее", format_percent(row.get("ctr_avg"))),
            ("VTR, среднее", format_percent(row.get("vtr_avg"))),
            ("Viewability, среднее", format_percent(row.get("viewability_avg"))),
            ("Поддержка Pixel", format_bool(row.get("verification_pixel"))),
            ("Поддержка JS", format_bool(row.get("verification_js"))),
            ("BLS", format_bool(row.get("bls"))),
            ("Sales Lift", format_bool(row.get("sales_lift"))),
        ],
        columns=["Параметр", "Значение"],
    )
    st.dataframe(metrics, hide_index=True, use_container_width=True)

    st.markdown("#### Параметры формата")
    for dict_id, title in DICT_LABELS.items():
        if dict_id in row.index:
            values = row.get(dict_id, [])
            if isinstance(values, list) and values:
                render_tag_line(title, values)

    st.markdown("#### Условия")
    info_fields = {
        "Условия верификации": row.get("verification_terms"),
        "Условия BLS": row.get("bls_terms"),
        "Условия Sales Lift": row.get("sales_lift_terms"),
        "Условия сезонности": row.get("seasonality_terms"),
    }
    for title, value in info_fields.items():
        if pd.notna(value) and str(value).strip():
            st.markdown(f"**{title}:** {value}")

    st.markdown("#### Полезные ссылки")
    link_fields = {
        "Пример размещения": row.get("example_url"),
        "Технические требования": row.get("technical_requirements_url"),
        "Медиакит": row.get("mediakit_url"),
        "Кейсы": row.get("cases_url"),
    }
    for title, url in link_fields.items():
        if pd.notna(url) and str(url).strip():
            st.markdown(f"- [{title}]({url})")


def main() -> None:
    st.title("Подбор рекламных форматов")
    st.caption("Фильтры применяются раньше скоринга.")

    try:
        formats, dict_items, format_items = load_data()
        df = enrich_formats(formats, dict_items, format_items)
    except Exception as e:
        st.error(f"Ошибка загрузки данных: {e}")
        st.stop()

    filters, weights, scoring_enabled = render_sidebar(df)

    filtered_df = apply_filters(df, filters)

    weights_total = sum(weights.values())
    scoring_applied = scoring_enabled and weights_total == 100

    if scoring_enabled and weights_total != 100:
        st.warning("Скоринг не применен. Сумма весов должна быть равна 100.")

    if scoring_applied:
        filtered_df = compute_score(filtered_df, weights)
        sort_columns = [col for col in ["score", "ecpm_discounted"] if col in filtered_df.columns]
        ascending = [False, True][: len(sort_columns)]
        filtered_df = filtered_df.sort_values(by=sort_columns, ascending=ascending, na_position="last")
    else:
        sort_columns = [col for col in ["platform", "format_name"] if col in filtered_df.columns]
        if sort_columns:
            filtered_df = filtered_df.sort_values(by=sort_columns, ascending=True, na_position="last")

    st.caption(f"Найдено форматов: {len(filtered_df)}")

    if filtered_df.empty:
        st.info("По заданным условиям ничего не найдено.")
        return

    table_df = build_table_view(filtered_df, scoring_applied=scoring_applied)
    selected_row = render_table_selection(table_df, filtered_df)

    if selected_row is not None:
        render_format_card(selected_row)
    else:
        st.info("Выберите формат в таблице, чтобы открыть карточку.")

    with st.expander("Как считается eCPM"):
        st.write(
            """
            - В расчете eCPM учитывается скидка.
            - Комиссия в eCPM не входит.
            - Для CPM используется средний CPM с учетом скидки.
            - Для CPC используется формула: CPC × CTR × 1000 с учетом скидки.
            - Для CPV используется формула: CPV × VTR × 1000 с учетом скидки.
            """
        )


if __name__ == "__main__":
    main()
