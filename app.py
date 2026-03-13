import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Подбор рекламных форматов",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    "verification_pixel": "Пиксель отслеживания",
    "verification_js": "JavaScript-трекинг",
    "verification_terms": "Условия верификации",
    "commission": "Комиссия",
    "bls": "Brand Lift",
    "sales_lift": "Sales Lift",
    "bls_terms": "Условия Brand Lift",
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
        .replace({"": np.nan, "nan": np.nan, "None": np.nan, "null": np.nan, "NULL": np.nan})
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


def format_item_badge(item: Dict) -> str:
    name = str(item.get("item_name", "")).strip()
    item_value = item.get("item_value")
    item_unit = item.get("item_unit")

    if pd.notna(item_value):
        if isinstance(item_value, (int, float, np.integer, np.floating)):
            numeric_value = float(item_value)
            if pd.notna(item_unit) and str(item_unit).strip():
                return f"{name} — {format_number(numeric_value)} {str(item_unit).strip()}"
            if abs(numeric_value) <= 1:
                return f"{name} — {format_percent(numeric_value)}"
            return f"{name} — {format_number(numeric_value)}"
        return f"{name} — {str(item_value).strip()}"

    return name


def normalize_weights(weights: Dict[str, float]) -> Dict[str, int]:
    total = sum(max(0.0, float(v)) for v in weights.values())
    if total <= 0:
        return DEFAULT_WEIGHTS.copy()

    scaled = {k: (max(0.0, float(v)) / total) * 100 for k, v in weights.items()}
    rounded = {k: int(math.floor(v / 5.0) * 5) for k, v in scaled.items()}

    remainder = 100 - sum(rounded.values())
    if remainder > 0:
        order = sorted(
            scaled.keys(),
            key=lambda key: scaled[key] - rounded[key],
            reverse=True,
        )
        for i in range(remainder // 5):
            rounded[order[i % len(order)]] += 5

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
        dict_df.rename(columns={item_name_col: "item_name"}),
        on=["dict_id", "item_id"],
        how="left",
        suffixes=("_format", "_dict"),
    )

    value_candidate_cols = []
    for col in merged.columns:
        low = col.lower()
        if low in {"format_id", "dict_id", "item_id", "is_active"}:
            continue
        if "name" in low or "title" in low:
            continue
        if any(token in low for token in ["markup", "percent", "coef", "coefficient", "value", "amount", "price", "rate", "surcharge"]):
            value_candidate_cols.append(col)

    unit_candidate_cols = []
    for col in merged.columns:
        low = col.lower()
        if any(token in low for token in ["unit", "currency", "measure"]):
            unit_candidate_cols.append(col)

    def extract_item_value(row: pd.Series):
        for col in value_candidate_cols:
            val = row.get(col)
            if pd.isna(val) or str(val).strip() in {"", "nan", "None"}:
                continue
            numeric = pd.to_numeric(pd.Series([val]), errors="coerce").iloc[0]
            if not pd.isna(numeric):
                return float(numeric)
            return str(val).strip()
        return np.nan

    def extract_item_unit(row: pd.Series):
        for col in unit_candidate_cols:
            val = row.get(col)
            if pd.notna(val) and str(val).strip():
                return str(val).strip()
        return np.nan

    merged["item_value_extracted"] = merged.apply(extract_item_value, axis=1)
    merged["item_unit_extracted"] = merged.apply(extract_item_unit, axis=1)

    grouped_names = (
        merged.groupby(["format_id", "dict_id"], dropna=False)["item_name"]
        .apply(lambda s: sorted({str(x).strip() for x in s.dropna() if str(x).strip()}))
        .reset_index()
    )
    pivot_names = grouped_names.pivot(index="format_id", columns="dict_id", values="item_name").reset_index()

    grouped_rich = (
        merged.groupby(["format_id", "dict_id"], dropna=False)
        .apply(
            lambda group: [
                {
                    "item_id": item["item_id"],
                    "item_name": str(item["item_name"]).strip() if pd.notna(item["item_name"]) else "",
                    "item_value": item["item_value_extracted"],
                    "item_unit": item["item_unit_extracted"],
                }
                for _, item in group.drop_duplicates(subset=["item_id"]).iterrows()
                if pd.notna(item["item_name"]) and str(item["item_name"]).strip()
            ],
            include_groups=False,
        )
        .reset_index(name="items_rich")
    )
    pivot_rich = grouped_rich.pivot(index="format_id", columns="dict_id", values="items_rich").reset_index()
    pivot_rich = pivot_rich.rename(columns={col: f"{col}__rich" for col in pivot_rich.columns if col != "format_id"})

    merged_pivot = pivot_names.merge(pivot_rich, on="format_id", how="left")

    for col in merged_pivot.columns:
        if col != "format_id":
            merged_pivot[col] = merged_pivot[col].apply(lambda x: x if isinstance(x, list) else [])

    return merged_pivot


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


def enrich_formats(formats: pd.DataFrame, dict_items: pd.DataFrame, format_items: pd.DataFrame) -> pd.DataFrame:
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
    if "selected_format_id" not in st.session_state:
        st.session_state["selected_format_id"] = None


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

    rename_map = {col: get_label(col) for col in existing_columns}
    return table_df.rename(columns=rename_map)


def get_top_formats(df: pd.DataFrame, scoring_applied: bool, n: int = 3) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    base = df.copy()
    if scoring_applied and "score" in base.columns:
        return base.sort_values(by=["score", "ecpm_discounted"], ascending=[False, True], na_position="last").head(n)

    sort_cols = [col for col in ["max_reach", "ctr_avg"] if col in base.columns]
    if sort_cols:
        return base.sort_values(by=sort_cols, ascending=[False] * len(sort_cols), na_position="last").head(n)

    return base.head(n)


def get_selected_format_by_id(df: pd.DataFrame, format_id) -> Optional[pd.Series]:
    if "format_id" not in df.columns:
        return None
    match = df[df["format_id"] == format_id]
    if match.empty:
        return None
    return match.iloc[0]


def build_format_card_data(row: pd.Series) -> Dict:
    data = {
        "title": str(row.get("format_name", "Без названия")),
        "meta": {
            "platform": str(row.get("platform", "—")),
            "type_service": str(row.get("type_service", "—")),
            "buy_model": str(row.get("buy_model", "—")),
        },
        "stats": {
            "max_reach": format_number(row.get("max_reach"), 0),
            "min_budget": format_number(row.get("min_budget"), 0),
            "ecpm_discounted": format_number(row.get("ecpm_discounted")),
            "commission": format_percent(row.get("commission")),
            "ctr_avg": format_percent(row.get("ctr_avg")),
            "viewability_avg": format_percent(row.get("viewability_avg")),
            "discount": format_percent(row.get("discount")),
            "vtr_avg": format_percent(row.get("vtr_avg")),
            "verification_pixel": format_bool(row.get("verification_pixel")),
            "verification_js": format_bool(row.get("verification_js")),
            "bls": format_bool(row.get("bls")),
            "sales_lift": format_bool(row.get("sales_lift")),
        },
        "description": row.get("description"),
        "dict_groups": {},
        "conditions": {
            "verification_terms": row.get("verification_terms"),
            "bls_terms": row.get("bls_terms"),
            "sales_lift_terms": row.get("sales_lift_terms"),
            "seasonality_terms": row.get("seasonality_terms"),
        },
        "links": {
            "example_url": row.get("example_url"),
            "technical_requirements_url": row.get("technical_requirements_url"),
            "mediakit_url": row.get("mediakit_url"),
            "cases_url": row.get("cases_url"),
        },
    }

    for dict_id, label in DICT_LABELS.items():
        rich_col = f"{dict_id}__rich"
        if rich_col in row.index and isinstance(row.get(rich_col), list) and row.get(rich_col):
            values = [format_item_badge(item) for item in row.get(rich_col)]
            data["dict_groups"][label] = values
        elif dict_id in row.index and isinstance(row.get(dict_id), list) and row.get(dict_id):
            data["dict_groups"][label] = row.get(dict_id)

    return data


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #ffffff;
            --page-wash: rgba(248, 242, 255, 0.42);
            --card: #ffffff;
            --text: #070037;
            --muted: rgba(7, 0, 55, 0.62);
            --muted-2: rgba(7, 0, 55, 0.48);
            --line: rgba(7, 0, 55, 0.08);
            --line-soft: rgba(7, 0, 55, 0.05);
            --accent: #3E20FF;
            --accent-hover: #A35AFF;
            --soft: #D7B8FF;
            --soft-bg: rgba(248, 242, 255, 0.82);
            --soft-bg-2: rgba(248, 242, 255, 0.48);
            --radius-card: 18px;
            --radius-sm: 14px;
            --radius-pill: 999px;
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: var(--text);
            font-variant-numeric: tabular-nums;
        }

        .stApp {
            background:
                radial-gradient(1200px 400px at 15% 0%, rgba(248, 242, 255, 0.95) 0%, rgba(248, 242, 255, 0.28) 35%, rgba(255,255,255,0) 70%),
                linear-gradient(180deg, rgba(255,255,255,0.98) 0%, #ffffff 100%);
        }

        .block-container {
            max-width: 1320px;
            padding-top: 24px;
            padding-bottom: 44px;
            padding-left: 24px;
            padding-right: 24px;
        }

        section[data-testid="stSidebar"] {
            background: rgba(255,255,255,0.72);
            border-right: 1px solid rgba(7, 0, 55, 0.06);
            backdrop-filter: blur(8px);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 18px;
            padding-bottom: 20px;
            padding-left: 14px;
            padding-right: 14px;
        }

        .sidebar-shell {
            padding: 4px 2px 0 2px;
        }

        .sidebar-title {
            font-size: 17px;
            font-weight: 700;
            line-height: 1.2;
            color: var(--text);
            margin: 0 0 14px 0;
        }

        .sidebar-section-title {
            font-size: 13px;
            font-weight: 700;
            line-height: 1.3;
            color: var(--text);
            margin: 20px 0 10px 0;
        }

        .sidebar-divider {
            height: 1px;
            background: rgba(7, 0, 55, 0.06);
            margin: 18px 0;
        }

        .sidebar-note {
            font-size: 12px;
            color: var(--muted);
            line-height: 1.45;
            margin-top: 8px;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        .stNumberInput > div > div,
        .stTextInput > div > div {
            min-height: 42px !important;
            background: rgba(255,255,255,0.96) !important;
            border: 1px solid rgba(7, 0, 55, 0.08) !important;
            border-radius: 10px !important;
            box-shadow: none !important;
        }

        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="input"] > div:hover,
        .stNumberInput > div > div:hover,
        .stTextInput > div > div:hover {
            border-color: rgba(163, 90, 255, 0.55) !important;
        }

        div[data-baseweb="tag"] {
            border-radius: 999px !important;
            background: rgba(248,242,255,0.9) !important;
            border: 1px solid rgba(215,184,255,0.6) !important;
            color: var(--text) !important;
        }

        .stCheckbox label {
            font-size: 14px !important;
        }

        div[data-testid="stSlider"] [data-baseweb="slider"] > div > div:nth-child(1) {
            background: rgba(215,184,255,0.75) !important;
            height: 4px !important;
        }

        div[data-testid="stSlider"] [data-baseweb="slider"] > div > div:nth-child(2) {
            background: #3E20FF !important;
            height: 4px !important;
        }

        div[data-testid="stSlider"] [role="slider"] {
            width: 16px !important;
            height: 16px !important;
            background: #3E20FF !important;
            border: 2px solid #FFFFFF !important;
            box-shadow: none !important;
        }

        div[data-testid="stSlider"] [data-testid="stThumbValue"] {
            display: none !important;
        }

        .stButton > button,
        .stDownloadButton > button {
            height: 40px;
            border-radius: 10px;
            border: 1px solid #3E20FF;
            background: #3E20FF;
            color: #FFFFFF;
            font-size: 14px;
            font-weight: 600;
            box-shadow: none;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background: #A35AFF;
            border-color: #A35AFF;
            color: #FFFFFF;
        }

        .ghost-btn button {
            background: #FFFFFF !important;
            color: #3E20FF !important;
            border: 1px solid rgba(7, 0, 55, 0.08) !important;
        }

        .ghost-btn button:hover {
            border-color: rgba(163, 90, 255, 0.55) !important;
            color: #A35AFF !important;
        }

        .ui-gap-16 { height: 16px; }
        .ui-gap-18 { height: 18px; }
        .ui-gap-20 { height: 20px; }

        .surface,
        .table-surface,
        .detail-surface {
            background: rgba(255,255,255,0.96);
            border: 1px solid rgba(7, 0, 55, 0.06);
            border-radius: 18px;
        }

        .hero {
            padding: 18px 22px;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto;
            gap: 16px;
            align-items: center;
        }

        .hero-title {
            margin: 0;
            font-size: 29px;
            line-height: 1.06;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text);
        }

        .hero-subtitle {
            margin: 7px 0 0 0;
            max-width: 620px;
            font-size: 14px;
            line-height: 1.48;
            color: var(--muted);
        }

        .hero-pills {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            justify-content: flex-end;
            align-items: center;
        }

        .hero-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            height: 32px;
            padding: 0 11px;
            border-radius: 999px;
            background: #FFFFFF;
            border: 1px solid rgba(7, 0, 55, 0.08);
            font-size: 12px;
            font-weight: 600;
            color: rgba(7, 0, 55, 0.82);
            white-space: nowrap;
        }

        .summary-strip {
            padding: 8px;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
        }

        .summary-card {
            padding: 14px 16px;
            border-radius: 14px;
            background: #FFFFFF;
            border: 1px solid rgba(7, 0, 55, 0.05);
            min-height: 92px;
        }

        .summary-label {
            font-size: 12px;
            font-weight: 600;
            line-height: 1.35;
            color: var(--muted-2);
            margin-bottom: 14px;
        }

        .summary-value {
            font-size: 30px;
            line-height: 1.04;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text);
        }

        .block-head {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 10px;
        }

        .block-title {
            margin: 0;
            font-size: 17px;
            line-height: 1.2;
            font-weight: 700;
            color: var(--text);
        }

        .block-note {
            margin: 0;
            font-size: 12px;
            line-height: 1.4;
            color: var(--muted-2);
        }

        .recommend-grid {
            display: grid;
            gap: 12px;
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }

        .recommend-card {
            background: rgba(255,255,255,0.98);
            border: 1px solid rgba(7, 0, 55, 0.06);
            border-radius: 16px;
            padding: 15px;
            min-height: 150px;
        }

        .recommend-top {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 8px;
        }

        .recommend-title {
            margin: 0;
            font-size: 19px;
            line-height: 1.14;
            font-weight: 700;
            color: var(--text);
        }

        .score-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 58px;
            height: 29px;
            padding: 0 10px;
            border-radius: 999px;
            background: rgba(62, 32, 255, 0.06);
            border: 1px solid rgba(62, 32, 255, 0.14);
            color: #3E20FF;
            font-size: 13px;
            font-weight: 700;
            flex: 0 0 auto;
        }

        .recommend-meta {
            margin: 0 0 11px 0;
            font-size: 13px;
            line-height: 1.42;
            color: var(--muted);
        }

        .recommend-stats {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
        }

        .recommend-stat {
            padding: 10px 11px;
            border-radius: 12px;
            background: rgba(248,242,255,0.46);
            border: 1px solid rgba(7, 0, 55, 0.03);
        }

        .recommend-stat-label {
            font-size: 11px;
            line-height: 1.3;
            color: var(--muted-2);
            margin-bottom: 5px;
        }

        .recommend-stat-value {
            font-size: 15px;
            line-height: 1.15;
            font-weight: 700;
            color: var(--text);
        }

        .table-surface {
            overflow: hidden;
        }

        .table-head {
            padding: 18px 20px;
            border-bottom: 1px solid rgba(7, 0, 55, 0.05);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            background: rgba(255,255,255,0.96);
        }

        .table-wrap {
            padding-top: 2px;
        }

        div[data-testid="stDataFrame"] {
            border: none !important;
            background: transparent !important;
        }

        div[data-testid="stDataFrame"] [role="table"] {
            border: none !important;
        }

        div[data-testid="stDataFrame"] [data-testid="stDataFrameResizable"] {
            border: none !important;
        }

        .detail-title {
            margin: 0 0 10px 0;
            font-size: 17px;
            line-height: 1.2;
            font-weight: 700;
            color: var(--text);
        }

        .detail-surface {
            padding: 22px;
        }

        .format-hero {
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(7, 0, 55, 0.05);
            margin-bottom: 18px;
        }

        .format-name {
            margin: 0 0 8px 0;
            font-size: 29px;
            line-height: 1.06;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text);
        }

        .format-meta {
            font-size: 14px;
            line-height: 1.5;
            color: var(--muted);
        }

        .section-block {
            margin-top: 18px;
        }

        .section-block:first-child {
            margin-top: 0;
        }

        .section-title {
            margin: 0 0 8px 0;
            font-size: 14px;
            line-height: 1.32;
            font-weight: 700;
            color: var(--text);
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
        }

        .metric-card {
            padding: 12px 14px;
            border-radius: 12px;
            background: rgba(248,242,255,0.54);
            border: 1px solid rgba(7, 0, 55, 0.03);
        }

        .metric-label {
            font-size: 12px;
            line-height: 1.3;
            color: var(--muted-2);
            margin-bottom: 5px;
        }

        .metric-value {
            font-size: 17px;
            line-height: 1.15;
            font-weight: 700;
            color: var(--text);
        }

        .body-text {
            margin: 0;
            font-size: 14px;
            line-height: 1.6;
            color: var(--text);
        }

        .muted-empty {
            margin: 0;
            font-size: 14px;
            line-height: 1.5;
            color: var(--muted);
        }

        .pill-group {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            min-height: 24px;
            padding: 3px 8px;
            border-radius: 999px;
            background: rgba(248,242,255,0.56);
            border: 1px solid rgba(7, 0, 55, 0.05);
            font-size: 11px;
            line-height: 1.2;
            font-weight: 500;
            color: rgba(7, 0, 55, 0.84);
        }

        .link-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .link-list a {
            font-size: 14px;
            line-height: 1.45;
            font-weight: 600;
            color: #3E20FF;
            text-decoration: none;
        }

        .link-list a:hover {
            color: #A35AFF;
            text-decoration: none;
        }

        .empty-state {
            padding: 18px 20px;
            border-radius: 16px;
            background: rgba(255,255,255,0.96);
            border: 1px dashed rgba(7, 0, 55, 0.08);
            color: var(--muted);
            font-size: 14px;
            line-height: 1.5;
        }

        @media (max-width: 1180px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }

            .hero-pills {
                justify-content: flex-start;
            }

            .summary-grid,
            .recommend-grid,
            .metric-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 760px) {
            .summary-grid,
            .recommend-grid,
            .metric-grid {
                grid-template-columns: 1fr;
            }

            .hero-title,
            .format-name {
                font-size: 24px;
            }

            .summary-value {
                font-size: 26px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_title() -> None:
    st.sidebar.markdown('<div class="sidebar-shell"><div class="sidebar-title">Панель управления</div></div>', unsafe_allow_html=True)


def render_sidebar_section_title(title: str) -> None:
    st.sidebar.markdown(f'<div class="sidebar-section-title">{title}</div>', unsafe_allow_html=True)


def render_sidebar_divider() -> None:
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)


def unique_options(df: pd.DataFrame, column: str) -> List:
    if column not in df.columns:
        return []
    values = df[column].dropna().astype(str)
    return sorted(values.unique().tolist())


def unique_tag_options(df: pd.DataFrame, column: str) -> List[str]:
    if column not in df.columns:
        return []
    values = set()
    for items in df[column]:
        if isinstance(items, list):
            for item in items:
                text = str(item).strip()
                if text:
                    values.add(text)
    return sorted(values)


def build_sidebar_state(df: pd.DataFrame) -> Tuple[Dict, bool, Dict[str, int]]:
    render_sidebar_title()

    render_sidebar_section_title("Фильтры")
    platforms = st.sidebar.multiselect("Площадка", options=unique_options(df, "platform"), placeholder="Все площадки")
    service_types = st.sidebar.multiselect("Тип сервиса", options=unique_options(df, "type_service"), placeholder="Все типы")
    buy_models = st.sidebar.multiselect("Модель закупки", options=unique_options(df, "buy_model"), placeholder="Все модели")

    need_verification_pixel = st.sidebar.checkbox("Нужен пиксель отслеживания", value=False)
    need_verification_js = st.sidebar.checkbox("Нужен JavaScript-трекинг", value=False)
    need_bls = st.sidebar.checkbox("Требуется Brand Lift", value=False)
    need_sales_lift = st.sidebar.checkbox("Требуется Sales Lift", value=False)

    render_sidebar_divider()

    render_sidebar_section_title("Параметры и таргетинги")
    filter_format_type = st.sidebar.multiselect("Тип формата", options=unique_tag_options(df, "format_type"), placeholder="Все значения")
    filter_device = st.sidebar.multiselect("Устройство", options=unique_tag_options(df, "device"), placeholder="Все значения")
    filter_placement = st.sidebar.multiselect("Размещение", options=unique_tag_options(df, "placement"), placeholder="Все значения")
    filter_display = st.sidebar.multiselect("Показ креатива", options=unique_tag_options(df, "display"), placeholder="Все значения")
    filter_dmp = st.sidebar.multiselect("Данные и сегменты", options=unique_tag_options(df, "dmp"), placeholder="Все значения")
    filter_targeting = st.sidebar.multiselect("Таргетинги", options=unique_tag_options(df, "targeting"), placeholder="Все значения")
    filter_instream_pos = st.sidebar.multiselect("Позиция в потоке", options=unique_tag_options(df, "instream_pos"), placeholder="Все значения")

    render_sidebar_divider()

    render_sidebar_section_title("Пороговые значения")
    min_reach = st.sidebar.number_input("Минимальный охват", min_value=0.0, value=0.0, step=1000.0)
    min_ctr = st.sidebar.number_input("Минимальный CTR", min_value=0.0, value=0.0, step=0.01, format="%.4f")
    min_vtr = st.sidebar.number_input("Минимальный VTR", min_value=0.0, value=0.0, step=0.01, format="%.4f")
    min_viewability = st.sidebar.number_input("Минимальный Viewability", min_value=0.0, value=0.0, step=0.01, format="%.4f")

    max_ecpm_value = float(df["ecpm_discounted"].dropna().max()) if "ecpm_discounted" in df.columns and not df["ecpm_discounted"].dropna().empty else 1000.0
    max_commission_value = float(df["commission"].dropna().max()) if "commission" in df.columns and not df["commission"].dropna().empty else 1.0

    max_ecpm = st.sidebar.number_input("Максимальный eCPM", min_value=0.0, value=max_ecpm_value, step=10.0)
    max_commission = st.sidebar.number_input("Максимальная комиссия", min_value=0.0, value=max_commission_value, step=0.01, format="%.4f")

    render_sidebar_divider()

    render_sidebar_section_title("Скоринг")
    scoring_applied = st.sidebar.toggle("Использовать скоринг", value=True)

    st.sidebar.slider("Вес охвата", min_value=0, max_value=100, step=5, key="weight_max_reach")
    st.sidebar.slider("Вес eCPM", min_value=0, max_value=100, step=5, key="weight_ecpm_discounted")
    st.sidebar.slider("Вес CTR", min_value=0, max_value=100, step=5, key="weight_ctr_avg")
    st.sidebar.slider("Вес VTR", min_value=0, max_value=100, step=5, key="weight_vtr_avg")
    st.sidebar.slider("Вес Viewability", min_value=0, max_value=100, step=5, key="weight_viewability_avg")
    st.sidebar.slider("Вес комиссии", min_value=0, max_value=100, step=5, key="weight_commission")

    weights_col1, weights_col2 = st.sidebar.columns(2)
    with weights_col1:
        if st.button("Нормализовать", use_container_width=True):
            normalize_weight_state()
    with weights_col2:
        st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
        if st.button("Сбросить", use_container_width=True):
            reset_weights()
        st.markdown("</div>", unsafe_allow_html=True)

    current_weights = {
        "max_reach": st.session_state.get("weight_max_reach", DEFAULT_WEIGHTS["max_reach"]),
        "ecpm_discounted": st.session_state.get("weight_ecpm_discounted", DEFAULT_WEIGHTS["ecpm_discounted"]),
        "ctr_avg": st.session_state.get("weight_ctr_avg", DEFAULT_WEIGHTS["ctr_avg"]),
        "vtr_avg": st.session_state.get("weight_vtr_avg", DEFAULT_WEIGHTS["vtr_avg"]),
        "viewability_avg": st.session_state.get("weight_viewability_avg", DEFAULT_WEIGHTS["viewability_avg"]),
        "commission": st.session_state.get("weight_commission", DEFAULT_WEIGHTS["commission"]),
    }

    st.sidebar.markdown(
        f'<div class="sidebar-note">Сумма весов: <strong>{sum(current_weights.values())}</strong></div>',
        unsafe_allow_html=True,
    )

    state = {
        "platforms": platforms,
        "service_types": service_types,
        "buy_models": buy_models,
        "need_verification_pixel": need_verification_pixel,
        "need_verification_js": need_verification_js,
        "need_bls": need_bls,
        "need_sales_lift": need_sales_lift,
        "filter_format_type": filter_format_type,
        "filter_device": filter_device,
        "filter_placement": filter_placement,
        "filter_display": filter_display,
        "filter_dmp": filter_dmp,
        "filter_targeting": filter_targeting,
        "filter_instream_pos": filter_instream_pos,
        "min_reach": None if min_reach == 0 else min_reach,
        "min_ctr": None if min_ctr == 0 else min_ctr,
        "min_vtr": None if min_vtr == 0 else min_vtr,
        "min_viewability": None if min_viewability == 0 else min_viewability,
        "max_ecpm": None if max_ecpm == max_ecpm_value else max_ecpm,
        "max_commission": None if max_commission == max_commission_value else max_commission,
    }

    return state, scoring_applied, current_weights


def render_header(found_count: int, scoring_applied: bool) -> None:
    status_text = "Скоринг включен" if scoring_applied else "Скоринг выключен"
    st.markdown(
        f"""
        <div class="surface hero">
            <div class="hero-grid">
                <div>
                    <h1 class="hero-title">Подбор рекламных форматов</h1>
                    <p class="hero-subtitle">
                        Рабочий интерфейс выбора: фильтрация, веса скоринга, ранжированный список и детальная карточка формата в одной сцене.
                    </p>
                </div>
                <div class="hero-pills">
                    <div class="hero-pill">Найдено: {found_count}</div>
                    <div class="hero-pill">{status_text}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_row(df: pd.DataFrame, scoring_applied: bool) -> None:
    found_count = len(df)
    best_score = format_number(df["score"].max()) if scoring_applied and "score" in df.columns and not df.empty else "—"
    max_reach = format_number(df["max_reach"].max(), 0) if "max_reach" in df.columns and not df.empty else "—"
    min_ecpm = format_number(df["ecpm_discounted"].min()) if "ecpm_discounted" in df.columns and not df.empty else "—"

    st.markdown(
        f"""
        <div class="surface summary-strip">
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-label">Найдено форматов</div>
                    <div class="summary-value">{found_count}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-label">Лучший скоринг</div>
                    <div class="summary-value">{best_score}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-label">Максимальный охват</div>
                    <div class="summary-value">{max_reach}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-label">Минимальный eCPM</div>
                    <div class="summary-value">{min_ecpm}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_top_card_html(row: pd.Series, scoring_applied: bool, mode_label: str) -> str:
    title = str(row.get("format_name", "")).strip()
    if not title or title.lower() == "nan":
        return ""

    meta_parts = [
        str(row.get("platform", "")).strip(),
        str(row.get("type_service", "")).strip(),
        str(row.get("buy_model", "")).strip(),
    ]
    meta_parts = [x for x in meta_parts if x and x.lower() != "nan"]
    meta_text = " · ".join(meta_parts) if meta_parts else mode_label

    if scoring_applied and "score" in row.index and pd.notna(row.get("score")):
        badge = format_number(row.get("score"))
    else:
        badge = ""

    stats = [
        ("Охват", format_number(row.get("max_reach"), 0)),
        ("eCPM", format_number(row.get("ecpm_discounted"))),
        ("CTR", format_percent(row.get("ctr_avg"))),
        ("Viewability", format_percent(row.get("viewability_avg"))),
    ]

    valid_stats = [(label, value) for label, value in stats if value and value != "—"]
    if len(valid_stats) < 2:
        return ""

    badge_html = f'<div class="score-pill">{badge}</div>' if badge else ""

    stats_html = "".join(
        [
            f"""
            <div class="recommend-stat">
                <div class="recommend-stat-label">{label}</div>
                <div class="recommend-stat-value">{value}</div>
            </div>
            """
            for label, value in valid_stats[:4]
        ]
    )

    return f"""
    <div class="recommend-card">
        <div class="recommend-top">
            <h3 class="recommend-title">{title}</h3>
            {badge_html}
        </div>
        <p class="recommend-meta">{meta_text}</p>
        <div class="recommend-stats">
            {stats_html}
        </div>
    </div>
    """


def render_top_formats(top_df: pd.DataFrame, scoring_applied: bool) -> None:
    if top_df.empty:
        return

    title = "Топ форматы" if scoring_applied else "Первые форматы в текущей выдаче"
    note = "Лучшие варианты по скорингу" if scoring_applied else "Первые позиции в текущем порядке сортировки"

    cards = []
    for _, row in top_df.iterrows():
        html = build_top_card_html(row, scoring_applied, note)
        if html:
            cards.append(html)

    if not cards:
        return

    st.markdown(
        f"""
        <div class="block-head">
            <h2 class="block-title">{title}</h2>
            <p class="block-note">{note}</p>
        </div>
        <div class="recommend-grid">
            {"".join(cards)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def prepare_display_table(df: pd.DataFrame, scoring_applied: bool) -> pd.DataFrame:
    table = build_table_view(df, scoring_applied).copy()

    numeric_source_map = {
        "Скоринг": "score",
        "Максимальный охват": "max_reach",
        "eCPM с учетом скидки": "ecpm_discounted",
        "CTR, среднее": "ctr_avg",
        "VTR, среднее": "vtr_avg",
        "Viewability, среднее": "viewability_avg",
        "Комиссия": "commission",
    }

    for display_col, source_col in numeric_source_map.items():
        if display_col in table.columns and source_col in df.columns:
            if source_col in {"ctr_avg", "vtr_avg", "viewability_avg", "commission"}:
                table[display_col] = df[source_col].apply(format_percent)
            elif source_col == "max_reach":
                table[display_col] = df[source_col].apply(lambda x: format_number(x, 0))
            else:
                table[display_col] = df[source_col].apply(format_number)

    return table


def render_results_table(df: pd.DataFrame, scoring_applied: bool) -> None:
    st.markdown(
        """
        <div class="table-surface">
            <div class="table-head">
                <h2 class="block-title">Результаты</h2>
                <p class="block-note">Выберите один формат для просмотра карточки</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.markdown('<div class="empty-state">По текущим фильтрам форматы не найдены.</div>', unsafe_allow_html=True)
        return

    render_df = prepare_display_table(df, scoring_applied)

    selection_event = st.dataframe(
        render_df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        height=min(44 * (len(render_df) + 1), 620),
    )

    selected_rows = []
    if isinstance(selection_event, dict):
        selected_rows = selection_event.get("selection", {}).get("rows", [])
    else:
        try:
            selected_rows = selection_event.selection.rows
        except Exception:
            selected_rows = []

    if selected_rows:
        selected_idx = selected_rows[0]
        if 0 <= selected_idx < len(df):
            st.session_state["selected_format_id"] = df.iloc[selected_idx]["format_id"]
    elif st.session_state.get("selected_format_id") is None and not df.empty:
        st.session_state["selected_format_id"] = df.iloc[0]["format_id"]


def render_pill_group(values: List[str]) -> None:
    clean = [str(v).strip() for v in values if pd.notna(v) and str(v).strip()]
    if not clean:
        st.markdown('<p class="muted-empty">Нет данных</p>', unsafe_allow_html=True)
        return
    html = "".join([f'<span class="pill">{value}</span>' for value in clean])
    st.markdown(f'<div class="pill-group">{html}</div>', unsafe_allow_html=True)


def render_text_section(title: str, text: Optional[str]) -> None:
    if pd.isna(text) or text is None or str(text).strip() == "":
        return
    st.markdown(
        f"""
        <div class="section-block">
            <h3 class="section-title">{title}</h3>
            <p class="body-text">{str(text).strip()}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_selected_format_card(row: Optional[pd.Series]) -> None:
    st.markdown('<h2 class="detail-title">Карточка формата</h2>', unsafe_allow_html=True)

    if row is None:
        st.markdown('<div class="empty-state">Выберите формат в таблице, чтобы открыть карточку.</div>', unsafe_allow_html=True)
        return

    data = build_format_card_data(row)
    title = str(data.get("title", "")).strip()
    if not title:
        return

    meta_text = " · ".join(
        [
            data["meta"].get("platform", "—"),
            data["meta"].get("type_service", "—"),
            data["meta"].get("buy_model", "—"),
        ]
    )

    st.markdown(
        f"""
        <div class="detail-surface">
            <div class="format-hero">
                <h3 class="format-name">{title}</h3>
                <div class="format-meta">{meta_text}</div>
            </div>

            <div class="section-block">
                <h4 class="section-title">Основные показатели</h4>
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-label">Максимальный охват</div>
                        <div class="metric-value">{data["stats"]["max_reach"]}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Минимальный бюджет</div>
                        <div class="metric-value">{data["stats"]["min_budget"]}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">eCPM с учетом скидки</div>
                        <div class="metric-value">{data["stats"]["ecpm_discounted"]}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Комиссия</div>
                        <div class="metric-value">{data["stats"]["commission"]}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">CTR, среднее</div>
                        <div class="metric-value">{data["stats"]["ctr_avg"]}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Viewability, среднее</div>
                        <div class="metric-value">{data["stats"]["viewability_avg"]}</div>
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    additional_values = [
        f"Скидка: {data['stats']['discount']}",
        f"VTR: {data['stats']['vtr_avg']}",
        f"Пиксель: {data['stats']['verification_pixel']}",
        f"JS-трекинг: {data['stats']['verification_js']}",
        f"Brand Lift: {data['stats']['bls']}",
        f"Sales Lift: {data['stats']['sales_lift']}",
    ]

    st.markdown('<div class="section-block"><h4 class="section-title">Дополнительно</h4></div>', unsafe_allow_html=True)
    render_pill_group(additional_values)

    render_text_section("Описание", data.get("description"))
    render_text_section("Условия верификации", data["conditions"].get("verification_terms"))
    render_text_section("Условия Brand Lift", data["conditions"].get("bls_terms"))
    render_text_section("Условия Sales Lift", data["conditions"].get("sales_lift_terms"))
    render_text_section("Условия сезонности", data["conditions"].get("seasonality_terms"))

    if data["dict_groups"]:
        for label, values in data["dict_groups"].items():
            clean_values = [v for v in values if pd.notna(v) and str(v).strip()]
            if not clean_values:
                continue
            st.markdown(f'<div class="section-block"><h4 class="section-title">{label}</h4></div>', unsafe_allow_html=True)
            render_pill_group(clean_values)

    links_map = {
        "Пример размещения": data["links"].get("example_url"),
        "Технические требования": data["links"].get("technical_requirements_url"),
        "Медиакит": data["links"].get("mediakit_url"),
        "Кейсы": data["links"].get("cases_url"),
    }
    valid_links = {label: url for label, url in links_map.items() if pd.notna(url) and str(url).strip()}
    if valid_links:
        links_html = "".join([f'<a href="{str(url).strip()}" target="_blank">{label}</a>' for label, url in valid_links.items()])
        st.markdown(
            f"""
            <div class="section-block">
                <h4 class="section-title">Ссылки</h4>
                <div class="link-list">{links_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    inject_styles()
    init_weight_state()

    formats, dict_items, format_items = load_data()
    df = enrich_formats(formats, dict_items, format_items)

    filter_state, scoring_applied, weights = build_sidebar_state(df)

    filtered = apply_filters(df, filter_state)

    if scoring_applied:
        result_df = compute_score(filtered, weights).sort_values(
            by=["score", "ecpm_discounted"],
            ascending=[False, True],
            na_position="last",
        )
    else:
        result_df = filtered.copy()
        sort_cols = [col for col in ["max_reach", "ctr_avg"] if col in result_df.columns]
        if sort_cols:
            result_df = result_df.sort_values(
                by=sort_cols,
                ascending=[False] * len(sort_cols),
                na_position="last",
            )

    if not result_df.empty:
        valid_ids = set(result_df["format_id"].tolist())
        if st.session_state.get("selected_format_id") not in valid_ids:
            st.session_state["selected_format_id"] = result_df.iloc[0]["format_id"]

    render_header(len(result_df), scoring_applied)
    st.markdown('<div class="ui-gap-16"></div>', unsafe_allow_html=True)

    render_kpi_row(result_df, scoring_applied)
    st.markdown('<div class="ui-gap-18"></div>', unsafe_allow_html=True)

    top_df = get_top_formats(result_df, scoring_applied, n=3)
    render_top_formats(top_df, scoring_applied)
    if not top_df.empty:
        st.markdown('<div class="ui-gap-18"></div>', unsafe_allow_html=True)

    render_results_table(result_df, scoring_applied)
    st.markdown('<div class="ui-gap-20"></div>', unsafe_allow_html=True)

    selected_row = get_selected_format_by_id(result_df, st.session_state.get("selected_format_id"))
    render_selected_format_card(selected_row)


if __name__ == "__main__":
    main()
