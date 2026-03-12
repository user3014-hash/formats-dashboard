import html
import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st
from streamlit.components.v1 import html as components_html


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
DEFAULT_TOP_N = 20

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

PILL_GROUP_ORDER = [
    "format_type",
    "device",
    "placement",
    "display",
    "dmp",
    "targeting",
    "instream_pos",
    "production",
    "other_markup",
    "targeting_markup",
    "seasonality_coeff",
]


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --white: #FFFFFF;
                --soft: #F8F2FF;
                --line: #E7DCF9;
                --line-strong: #D7B8FF;
                --accent: #3E20FF;
                --accent-soft: #725BFF;
                --ink: #070037;
                --muted: rgba(7, 0, 55, 0.62);
            }

            html, body, [class*="css"]  {
                font-feature-settings: "tnum" 1, "lnum" 1;
            }

            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stAppViewContainer"] > .main,
            [data-testid="stAppViewContainer"] > .main > div,
            .main .block-container {
                background: var(--white);
                color: var(--ink);
            }

            .main .block-container {
                padding-top: 1.3rem;
                padding-bottom: 3rem;
                max-width: 1320px;
            }

            [data-testid="stSidebar"],
            [data-testid="stSidebar"] > div,
            [data-testid="stSidebarContent"] {
                background: var(--soft);
                color: var(--ink) !important;
                border-right: 1px solid var(--line);
            }

            [data-testid="stSidebar"] *,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] div,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] h4 {
                color: var(--ink) !important;
            }

            .stApp,
            .stApp p,
            .stApp label,
            .stApp div,
            .stApp span,
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4,
            .stApp h5,
            .stApp h6,
            [data-testid="stMarkdownContainer"] * {
                color: var(--ink);
            }

            h1 {
                font-size: 2.05rem !important;
                line-height: 1.08 !important;
                letter-spacing: -0.02em !important;
                margin-bottom: 0.9rem !important;
                font-weight: 700 !important;
            }

            h2 {
                font-size: 1.25rem !important;
                line-height: 1.2 !important;
                letter-spacing: -0.01em !important;
                font-weight: 700 !important;
            }

            h3 {
                font-size: 0.98rem !important;
                line-height: 1.35 !important;
                font-weight: 700 !important;
            }

            p, li, label, .stCaption {
                font-size: 14px !important;
                line-height: 1.45 !important;
            }

            a, a:visited {
                color: var(--accent) !important;
                text-decoration: none !important;
            }

            a:hover {
                color: var(--accent-soft) !important;
            }

            .stButton > button,
            .stDownloadButton > button,
            button[kind="primary"] {
                background: var(--accent) !important;
                color: var(--white) !important;
                border: 1px solid var(--accent) !important;
                border-radius: 10px !important;
                box-shadow: none !important;
                font-weight: 500 !important;
            }

            .stButton > button:hover,
            .stDownloadButton > button:hover,
            button[kind="primary"]:hover {
                background: var(--accent-soft) !important;
                border-color: var(--accent-soft) !important;
                color: var(--white) !important;
            }

            .stTextInput input,
            .stNumberInput input,
            .stTextArea textarea {
                background: var(--white) !important;
                color: var(--ink) !important;
                border: 1px solid var(--line-strong) !important;
                border-radius: 10px !important;
            }

            div[data-baseweb="select"] > div {
                background: var(--white) !important;
                color: var(--ink) !important;
                border: 1px solid var(--line-strong) !important;
                border-radius: 10px !important;
                min-height: 42px !important;
            }

            div[data-baseweb="select"] input {
                color: var(--ink) !important;
            }

            [data-baseweb="tag"] {
                background: var(--white) !important;
                border: 1px solid var(--line-strong) !important;
                border-radius: 6px !important;
                color: var(--ink) !important;
                padding: 0 2px !important;
            }

            [data-baseweb="tag"] * {
                color: var(--ink) !important;
                font-size: 12px !important;
                line-height: 1.2 !important;
                font-weight: 500 !important;
            }

            .stCheckbox {
                margin-bottom: 0.15rem !important;
            }

            .stSlider [role="tooltip"],
            .stSlider div[data-baseweb="tooltip"],
            .stSlider div[data-baseweb="popover"],
            .stSlider [data-testid="stThumbValue"] {
                display: none !important;
                opacity: 0 !important;
                visibility: hidden !important;
            }

            .stAlert {
                background: var(--soft) !important;
                color: var(--ink) !important;
                border: 1px solid var(--line-strong) !important;
                border-radius: 12px !important;
            }

            [data-testid="stDataEditor"] {
                border-radius: 14px !important;
                overflow: hidden !important;
                border: 1px solid var(--line) !important;
                box-shadow: none !important;
            }

            [data-testid="stDataEditor"] * {
                color: var(--ink) !important;
            }

            .dashboard-card {
                background: var(--white);
                border: 1px solid var(--line);
                border-radius: 16px;
                padding: 20px;
                margin-top: 8px;
            }

            .dashboard-card__title {
                font-size: 28px;
                line-height: 1.12;
                font-weight: 700;
                letter-spacing: -0.02em;
                color: var(--ink);
                margin: 0 0 8px 0;
            }

            .dashboard-card__meta {
                font-size: 14px;
                line-height: 1.45;
                color: var(--muted);
                margin: 0 0 16px 0;
            }

            .dashboard-card__meta strong {
                color: var(--ink);
                font-weight: 500;
            }

            .stats-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 10px;
                margin-top: 6px;
            }

            .stat {
                background: var(--soft);
                border-radius: 12px;
                padding: 12px 14px;
                border: 1px solid transparent;
            }

            .stat-label {
                font-size: 12px;
                line-height: 1.25;
                color: var(--muted);
                margin-bottom: 5px;
            }

            .stat-value {
                font-size: 14px;
                line-height: 1.3;
                font-weight: 600;
                color: var(--ink);
            }

            .section {
                margin-top: 18px;
            }

            .section-title {
                font-size: 14px;
                line-height: 1.35;
                font-weight: 700;
                color: var(--ink);
                margin: 0 0 8px 0;
            }

            .section-text {
                font-size: 14px;
                line-height: 1.55;
                color: var(--ink);
                margin: 0;
                max-width: 980px;
            }

            .pill-group {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-top: 4px;
            }

            .pill {
                display: inline-flex;
                align-items: center;
                padding: 4px 8px;
                border-radius: 6px;
                background: var(--soft);
                border: 1px solid var(--line-strong);
                color: var(--ink);
                font-size: 12px;
                line-height: 1.2;
                font-weight: 500;
                white-space: nowrap;
            }

            .links-list {
                display: grid;
                gap: 6px;
                margin-top: 4px;
            }

            .links-list a {
                font-size: 14px;
                line-height: 1.4;
                font-weight: 500;
            }

            @media (max-width: 900px) {
                .stats-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_dom_fixes() -> None:
    components_html(
        """
        <script>
        (function() {
            const hideSliderTooltips = () => {
                const selectors = [
                    '[role="tooltip"]',
                    '[data-baseweb="tooltip"]',
                    '[data-baseweb="popover"]',
                    '[data-testid="stThumbValue"]'
                ];

                selectors.forEach((selector) => {
                    const nodes = window.parent.document.querySelectorAll(selector);
                    nodes.forEach((node) => {
                        const text = (node.textContent || '').trim();
                        if (text === '0' || text === '100' || text === '5' || text === '95' || node.closest('[data-baseweb="slider"]')) {
                            node.style.display = 'none';
                            node.style.visibility = 'hidden';
                            node.style.opacity = '0';
                            node.setAttribute('hidden', 'hidden');
                        }
                    });
                });
            };

            hideSliderTooltips();

            const observer = new MutationObserver(() => hideSliderTooltips());
            observer.observe(window.parent.document.body, {
                childList: true,
                subtree: true,
                attributes: true
            });
        })();
        </script>
        """,
        height=0,
    )


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
    if "top_n_formats" not in st.session_state:
        st.session_state["top_n_formats"] = DEFAULT_TOP_N


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


def render_sidebar(df: pd.DataFrame) -> Tuple[Dict, Dict[str, int], bool, int]:
    st.sidebar.header("Фильтры")

    filters: Dict[str, Optional[float] | List[str] | bool] = {}

    filters["platforms"] = st.sidebar.multiselect(
        "Площадка",
        options=sorted(df["platform"].dropna().unique().tolist()) if "platform" in df.columns else [],
        placeholder="Выбрать",
    )
    filters["service_types"] = st.sidebar.multiselect(
        "Тип сервиса",
        options=sorted(df["type_service"].dropna().unique().tolist()) if "type_service" in df.columns else [],
        placeholder="Выбрать",
    )
    filters["buy_models"] = st.sidebar.multiselect(
        "Модель закупки",
        options=sorted(df["buy_model"].dropna().unique().tolist()) if "buy_model" in df.columns else [],
        placeholder="Выбрать",
    )

    filters["need_verification_pixel"] = st.sidebar.checkbox("Пиксель отслеживания")
    filters["need_verification_js"] = st.sidebar.checkbox("JavaScript-трекинг")
    filters["need_bls"] = st.sidebar.checkbox("Brand Lift")
    filters["need_sales_lift"] = st.sidebar.checkbox("Sales Lift")

    st.sidebar.subheader("Параметры и таргетинги")

    filters["filter_format_type"] = st.sidebar.multiselect("Тип формата", get_all_tag_values(df, "format_type"), placeholder="Выбрать")
    filters["filter_device"] = st.sidebar.multiselect("Устройство", get_all_tag_values(df, "device"), placeholder="Выбрать")
    filters["filter_placement"] = st.sidebar.multiselect("Размещение", get_all_tag_values(df, "placement"), placeholder="Выбрать")
    filters["filter_display"] = st.sidebar.multiselect("Показ креатива", get_all_tag_values(df, "display"), placeholder="Выбрать")
    filters["filter_dmp"] = st.sidebar.multiselect("Данные и сегменты", get_all_tag_values(df, "dmp"), placeholder="Выбрать")
    filters["filter_targeting"] = st.sidebar.multiselect("Таргетинги", get_all_tag_values(df, "targeting"), placeholder="Выбрать")
    filters["filter_instream_pos"] = st.sidebar.multiselect("Позиция в потоке", get_all_tag_values(df, "instream_pos"), placeholder="Выбрать")

    st.sidebar.subheader("Пороговые значения")

    filters["min_reach"] = st.sidebar.number_input("Минимальный охват", min_value=0, value=0, step=10000)
    filters["min_ctr"] = st.sidebar.number_input("Минимальный CTR", min_value=0.0, value=0.0, step=0.001, format="%.3f")
    filters["min_vtr"] = st.sidebar.number_input("Минимальный VTR", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    filters["min_viewability"] = st.sidebar.number_input("Минимальный viewability", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    filters["max_ecpm"] = st.sidebar.number_input("Максимальный eCPM", min_value=0.0, value=0.0, step=10.0, format="%.2f")
    filters["max_commission"] = st.sidebar.number_input("Максимальная комиссия", min_value=0.0, value=0.0, step=0.01, format="%.2f")

    if filters["min_reach"] == 0:
        filters["min_reach"] = None
    for key in ["min_ctr", "min_vtr", "min_viewability", "max_ecpm", "max_commission"]:
        if filters[key] == 0:
            filters[key] = None

    st.sidebar.divider()
    st.sidebar.header("Скоринг")

    scoring_enabled = st.sidebar.checkbox("Включить скоринг", value=True)

    init_weight_state()

    top_n = st.sidebar.number_input(
        "Сколько топ форматов вывести",
        min_value=1,
        value=int(st.session_state["top_n_formats"]),
        step=1,
        key="top_n_formats",
    )

    st.sidebar.slider("Максимальный охват", min_value=0, max_value=100, step=5, key="weight_max_reach")
    st.sidebar.slider("eCPM с учетом скидки", min_value=0, max_value=100, step=5, key="weight_ecpm_discounted")
    st.sidebar.slider("CTR", min_value=0, max_value=100, step=5, key="weight_ctr_avg")
    st.sidebar.slider("VTR", min_value=0, max_value=100, step=5, key="weight_vtr_avg")
    st.sidebar.slider("Viewability", min_value=0, max_value=100, step=5, key="weight_viewability_avg")
    st.sidebar.slider("Комиссия", min_value=0, max_value=100, step=5, key="weight_commission")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.button("Нормализовать", key="normalize_weights_btn", on_click=normalize_weight_state)
    with col2:
        st.button("Сбросить", key="reset_weights_btn", on_click=reset_weights)

    weights = {
        "max_reach": int(st.session_state["weight_max_reach"]),
        "ecpm_discounted": int(st.session_state["weight_ecpm_discounted"]),
        "ctr_avg": int(st.session_state["weight_ctr_avg"]),
        "vtr_avg": int(st.session_state["weight_vtr_avg"]),
        "viewability_avg": int(st.session_state["weight_viewability_avg"]),
        "commission": int(st.session_state["weight_commission"]),
    }

    st.sidebar.caption(f"Сумма весов: {sum(weights.values())}")

    return filters, weights, scoring_enabled, int(top_n)


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
    return table_df.rename(columns=rename_map)


def render_table_selection(table_df: pd.DataFrame, source_df: pd.DataFrame) -> Optional[pd.Series]:
    disabled_columns = [col for col in table_df.columns if col != "Выбрать"]

    edited = st.data_editor(
        table_df,
        hide_index=True,
        use_container_width=True,
        disabled=disabled_columns,
        column_config={"Выбрать": st.column_config.CheckboxColumn("Выбрать")},
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


def render_pills(title: str, values: List[str]) -> None:
    clean_values = [str(v).strip() for v in values if str(v).strip()]
    if not clean_values:
        return

    pills_html = "".join(f'<span class="pill">{html.escape(value)}</span>' for value in clean_values)

    st.markdown(
        f"""
        <div class="section">
            <div class="section-title">{html.escape(title)}</div>
            <div class="pill-group">{pills_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats(row: pd.Series) -> None:
    stats = [
        ("Максимальный охват", format_number(row.get("max_reach"), 0)),
        ("Минимальный бюджет", format_number(row.get("min_budget"), 0)),
        ("eCPM с учетом скидки", format_number(row.get("ecpm_discounted"))),
        ("Комиссия", format_percent(row.get("commission"))),
        ("CTR, среднее", format_percent(row.get("ctr_avg"))),
        ("Viewability, среднее", format_percent(row.get("viewability_avg"))),
    ]

    stats_html = "".join(
        f"""
        <div class="stat">
            <div class="stat-label">{html.escape(label)}</div>
            <div class="stat-value">{html.escape(value)}</div>
        </div>
        """
        for label, value in stats
    )

    st.markdown(
        f"""
        <div class="section">
            <div class="section-title">Основные показатели</div>
            <div class="stats-grid">{stats_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    aux_values = [
        f"Скидка — {format_percent(row.get('discount'))}",
        f"VTR, среднее — {format_percent(row.get('vtr_avg'))}",
        f"Пиксель отслеживания — {format_bool(row.get('verification_pixel'))}",
        f"JavaScript-трекинг — {format_bool(row.get('verification_js'))}",
        f"Brand Lift — {format_bool(row.get('bls'))}",
        f"Sales Lift — {format_bool(row.get('sales_lift'))}",
    ]
    render_pills("Дополнительно", aux_values)


def render_text_block(title: str, value: Optional[str]) -> None:
    if pd.isna(value) or not str(value).strip():
        return

    st.markdown(
        f"""
        <div class="section">
            <div class="section-title">{html.escape(title)}</div>
            <p class="section-text">{html.escape(str(value).strip())}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_links(row: pd.Series) -> None:
    links = [
        ("Пример размещения", row.get("example_url")),
        ("Технические требования", row.get("technical_requirements_url")),
        ("Медиакит", row.get("mediakit_url")),
        ("Кейсы", row.get("cases_url")),
    ]

    link_items = [
        f'<a href="{html.escape(str(url))}" target="_blank">{html.escape(title)}</a>'
        for title, url in links
        if pd.notna(url) and str(url).strip()
    ]

    if not link_items:
        return

    st.markdown(
        f"""
        <div class="section">
            <div class="section-title">Полезные ссылки</div>
            <div class="links-list">{''.join(link_items)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_format_card(row: pd.Series) -> None:
    st.subheader("Карточка формата")

    title = str(row.get("format_name", "Без названия"))
    platform = str(row.get("platform", "—"))
    service = str(row.get("type_service", "—"))
    buy_model = str(row.get("buy_model", "—"))

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="dashboard-card__title">{html.escape(title)}</div>
            <div class="dashboard-card__meta">
                <strong>{html.escape(platform)}</strong> · {html.escape(service)} · {html.escape(buy_model)}
            </div>
        """,
        unsafe_allow_html=True,
    )

    render_text_block("Описание", row.get("description"))
    render_stats(row)

    for dict_id in PILL_GROUP_ORDER:
        rich_col = f"{dict_id}__rich"
        if rich_col in row.index and isinstance(row.get(rich_col), list) and row.get(rich_col):
            values = [format_item_badge(item) for item in row.get(rich_col)]
            render_pills(DICT_LABELS.get(dict_id, dict_id), values)
        elif dict_id in row.index and isinstance(row.get(dict_id), list) and row.get(dict_id):
            render_pills(DICT_LABELS.get(dict_id, dict_id), row.get(dict_id))

    render_text_block("Условия верификации", row.get("verification_terms"))
    render_text_block("Условия Brand Lift", row.get("bls_terms"))
    render_text_block("Условия Sales Lift", row.get("sales_lift_terms"))
    render_text_block("Условия сезонности", row.get("seasonality_terms"))
    render_links(row)

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    inject_styles()
    inject_dom_fixes()

    st.title("Подбор рекламных форматов")

    try:
        formats, dict_items, format_items = load_data()
        df = enrich_formats(formats, dict_items, format_items)
    except Exception as e:
        st.error(f"Ошибка загрузки данных: {e}")
        st.stop()

    filters, weights, scoring_enabled, top_n = render_sidebar(df)
    filtered_df = apply_filters(df, filters)

    weights_total = sum(weights.values())
    scoring_applied = scoring_enabled and weights_total == 100

    if scoring_enabled and weights_total != 100:
        st.warning("Скоринг не применен. Сумма весов должна быть равна 100.")

    if scoring_applied:
        filtered_df = compute_score(filtered_df, weights)
        sort_columns = [col for col in ["score", "ecpm_discounted"] if col in filtered_df.columns]
        ascending = [False, True][: len(sort_columns)]
        filtered_df = filtered_df.sort_values(by=sort_columns, ascending=ascending, na_position="last").head(top_n)
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


if __name__ == "__main__":
    main()
