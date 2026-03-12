import html
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Подбор форматов", layout="wide")


# =========================
# Константы
# =========================
COLORS = {
    "sidebar_bg": "#3E20FF",
    "bg": "#FFFFFF",
    "text": "#070037",
    "muted": "#070037",
    "soft": "#F8F2FF",
    "border": "#D7B8FF",
    "header_bg": "#3E20FF",
    "header_text": "#FFFFFF",
    "tag_bg": "#725BFF",
    "tag_hover": "#3E20FF",
    "tag_text": "#FFFFFF",
    "input_bg": "#FFFFFF",
    "input_text": "#070037",
}

FONT_FAMILY = 'Inter, system-ui, -apple-system, "Segoe UI", Arial, sans-serif'

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
    "seasonality_coeff": "Сезонные коэффициенты",
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

TABLE_RATIOS = [
    1.0,
    1.2,
    2.7,
    1.5,
    1.5,
    1.4,
    1.4,
    1.5,
    1.5,
    1.1,
    1.1,
    1.4,
    1.1,
    1.1,
]

CARD_META_FIELDS = [
    "device",
    "display",
    "placement",
    "instream_pos",
    "dmp",
]

CARD_TAG_FIELDS = [
    "production",
    "other_markup",
    "seasonality_coeff",
    "targeting",
    "targeting_markup",
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
# Стили
# =========================
st.markdown(
    f"""
    <style>
        :root {{
            --bg: {COLORS["bg"]};
            --sidebar-bg: {COLORS["sidebar_bg"]};
            --text: {COLORS["text"]};
            --soft: {COLORS["soft"]};
            --border: {COLORS["border"]};
            --header-bg: {COLORS["header_bg"]};
            --header-text: {COLORS["header_text"]};
            --tag-bg: {COLORS["tag_bg"]};
            --tag-hover: {COLORS["tag_hover"]};
            --tag-text: {COLORS["tag_text"]};
            --input-bg: {COLORS["input_bg"]};
            --input-text: {COLORS["input_text"]};
        }}

        html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
            font-family: {FONT_FAMILY};
        }}

        [data-testid="stAppViewContainer"] {{
            background: var(--bg);
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .block-container {{
            padding-top: 1rem;
            padding-bottom: 1.25rem;
        }}

        section[data-testid="stSidebar"] {{
            background: var(--sidebar-bg);
        }}

        section[data-testid="stSidebar"] .block-container {{
            padding-top: 24px;
            padding-left: 24px;
            padding-right: 20px;
            padding-bottom: 16px;
        }}

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {{
            color: #FFFFFF !important;
        }}

        .page-title {{
            font-size: 32px;
            line-height: 1.1;
            font-weight: 700;
            color: var(--text);
            margin: 0 0 20px 0;
        }}

        .sidebar-title,
        .sidebar-group,
        .card-section-title,
        .metric-title {{
            font-size: 20px;
            line-height: 1.2;
            font-weight: 600;
        }}

        .sidebar-title {{
            margin: 0 0 10px 0;
            color: #FFFFFF;
        }}

        .sidebar-group {{
            margin: 20px 0 10px 0;
            color: #FFFFFF;
        }}

        .sidebar-field,
        .metric-label,
        .field-label,
        .custom-cell,
        .custom-header,
        .card-text,
        .research-text,
        .stButton > button,
        .stLinkButton > a,
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] [data-baseweb="select"] *,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input,
        [data-testid="stSidebar"] [data-baseweb="tag"] span {{
            font-size: 18px !important;
            line-height: 1.45 !important;
        }}

        .sidebar-field {{
            font-weight: 500;
            color: #FFFFFF;
            margin: 10px 0 6px 0;
        }}

        .sidebar-count {{
            font-size: 18px;
            line-height: 1.45;
            font-weight: 500;
            color: #FFFFFF;
            margin: 16px 0 0 0;
        }}

        /* Единый стиль белых полей слева */
        [data-testid="stSidebar"] [data-baseweb="input"] > div,
        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] > div {{
            background: #FFFFFF !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            border-radius: 8px !important;
            min-height: 44px !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="input"] > div:hover,
        [data-testid="stSidebar"] [data-baseweb="select"] > div:hover,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] > div:hover,
        [data-testid="stSidebar"] [data-baseweb="input"] > div:focus-within,
        [data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] > div:focus-within {{
            background: #F8F2FF !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="input"] input,
        [data-testid="stSidebar"] [data-baseweb="select"] input,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input {{
            background: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            color: #070037 !important;
            caret-color: #070037 !important;
            font-size: 18px !important;
            font-weight: 400 !important;
            height: 44px !important;
            line-height: 44px !important;
            padding: 0 12px !important;
            margin: 0 !important;
            -webkit-appearance: none !important;
            appearance: none !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="input"] input:focus,
        [data-testid="stSidebar"] [data-baseweb="input"] input:focus-visible,
        [data-testid="stSidebar"] [data-baseweb="input"] input:active,
        [data-testid="stSidebar"] [data-baseweb="select"] input:focus,
        [data-testid="stSidebar"] [data-baseweb="select"] input:focus-visible,
        [data-testid="stSidebar"] [data-baseweb="select"] input:active,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input:focus,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input:focus-visible,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input:active {{
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] input::placeholder {{
            color: rgba(7, 0, 55, 0.45) !important;
        }}

        [data-testid="stSidebar"] input::selection {{
            background: #D7B8FF !important;
            color: #070037 !important;
        }}

        /* Убираем внутренние серые подложки */
        [data-testid="stSidebar"] [data-baseweb="select"] > div > div,
        [data-testid="stSidebar"] [data-baseweb="input"] > div > div,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] > div > div {{
            background: transparent !important;
            box-shadow: none !important;
            outline: none !important;
            border: none !important;
        }}

        /* Иконки в полях */
        [data-testid="stSidebar"] [data-baseweb="select"] svg,
        [data-testid="stSidebar"] [data-baseweb="input"] svg,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] svg {{
            opacity: 1 !important;
            color: #070037 !important;
            fill: #070037 !important;
            stroke: #070037 !important;
        }}

        /* Убираем пунктир и служебные рамки */
        [data-testid="stSidebar"] *:focus,
        [data-testid="stSidebar"] *:focus-visible {{
            outline: none !important;
            box-shadow: none !important;
        }}

        /* Выпадающие меню */
        [data-baseweb="popover"] {{
            background: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 8px 24px rgba(7, 0, 55, 0.12) !important;
        }}

        [data-baseweb="popover"] * {{
            color: #070037 !important;
            font-size: 18px !important;
            outline: none !important;
            box-shadow: none !important;
        }}

        [data-baseweb="popover"] [role="option"] {{
            background: #FFFFFF !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }}

        [data-baseweb="popover"] [role="option"]:hover,
        [data-baseweb="popover"] [role="option"][aria-selected="true"] {{
            background: #F8F2FF !important;
        }}

        /* Убираем Select all и No results */
        [data-baseweb="popover"] [aria-label="Select all"],
        [data-baseweb="popover"] div:has(> [aria-label="Select all"]),
        [data-baseweb="popover"] [aria-disabled="true"] {{
            display: none !important;
        }}

        /* Плашки внутри multiselect */
        [data-testid="stSidebar"] [data-baseweb="tag"] {{
            background: var(--tag-bg) !important;
            color: var(--tag-text) !important;
            border: none !important;
            border-radius: 6px !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="tag"]:hover {{
            background: var(--tag-hover) !important;
            color: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="tag"] svg {{
            opacity: 1 !important;
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
        }}

        /* Чекбоксы */
        [data-testid="stSidebar"] [data-testid="stCheckbox"] label {{
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            margin: 0 !important;
        }}

        [data-testid="stSidebar"] input[type="checkbox"] {{
            appearance: none !important;
            -webkit-appearance: none !important;
            width: 18px !important;
            height: 18px !important;
            margin: 0 !important;
            border-radius: 4px !important;
            border: 1px solid var(--border) !important;
            background: #FFFFFF !important;
            position: relative !important;
            box-shadow: none !important;
            outline: none !important;
        }}

        [data-testid="stSidebar"] input[type="checkbox"]:hover {{
            border-color: var(--tag-bg) !important;
        }}

        [data-testid="stSidebar"] input[type="checkbox"]:checked {{
            background: var(--tag-bg) !important;
            border-color: var(--tag-bg) !important;
        }}

        [data-testid="stSidebar"] input[type="checkbox"]:checked::after {{
            content: "✓";
            position: absolute;
            left: 3px;
            top: -1px;
            color: #FFFFFF;
            font-size: 14px;
            font-weight: 700;
        }}

        /* Number input */
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input {{
            padding-left: 14px !important;
            padding-right: 34px !important;
            color: var(--input-text) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stNumberInput"] button {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            width: 28px !important;
            min-width: 28px !important;
            color: var(--input-text) !important;
        }}

        /* Slider */
        [data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {{
            background: var(--header-bg) !important;
            border-color: var(--header-bg) !important;
            box-shadow: none !important;
            outline: none !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="slider"] > div > div {{
            background: var(--border) !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="slider"] [data-testid="stThumbValue"] {{
            display: none !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="slider"] *:focus {{
            box-shadow: none !important;
            outline: none !important;
        }}

        /* Кнопки */
        .stButton > button {{
            height: 40px !important;
            border-radius: 10px !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
            background: #FFFFFF !important;
            color: var(--text) !important;
            font-weight: 500 !important;
            white-space: nowrap !important;
        }}

        .stButton > button:hover {{
            background: var(--soft) !important;
            color: var(--text) !important;
            border: none !important;
        }}

        .stButton > button:disabled {{
            background: rgba(255,255,255,0.55) !important;
            color: rgba(7, 0, 55, 0.45) !important;
            opacity: 1 !important;
        }}

        .stLinkButton > a {{
            border-radius: 6px !important;
            border: 1px solid var(--border) !important;
            color: var(--text) !important;
            background: #FFFFFF !important;
            text-decoration: none !important;
            padding: 8px 12px !important;
            min-height: 40px !important;
        }}

        .stLinkButton > a:hover {{
            background: var(--soft) !important;
            border-color: var(--border) !important;
            color: var(--text) !important;
        }}

        .metric-card {{
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            min-height: 92px;
        }}

        .metric-label {{
            font-size: 18px;
            font-weight: 500;
            color: var(--text);
            margin-bottom: 10px;
        }}

        .metric-value {{
            font-size: 32px;
            line-height: 1;
            font-weight: 700;
            color: var(--text);
        }}

        .divider {{
            height: 1px;
            background: var(--border);
            margin: 20px 0;
        }}

        .result-note {{
            font-size: 18px;
            line-height: 1.45;
            color: var(--text);
            margin: 0 0 16px 0;
        }}

        .table-wrap {{
            width: 100%;
            overflow-x: auto;
        }}

        .table-min {{
            min-width: 1480px;
        }}

        .custom-header {{
            color: var(--header-text);
            font-weight: 500;
            padding: 12px 10px;
            border-right: 1px solid rgba(255,255,255,0.18);
            white-space: nowrap;
            font-size: 18px;
        }}

        .custom-cell {{
            color: var(--text);
            font-weight: 400;
            padding: 12px 10px;
            white-space: nowrap;
            display: flex;
            align-items: center;
            font-size: 18px;
        }}

        .card-block {{
            margin-top: 20px;
            background: #FFFFFF;
            border: none;
            border-radius: 0;
            padding: 0;
        }}

        .card-title {{
            font-size: 32px;
            line-height: 1.1;
            font-weight: 700;
            color: var(--text);
            margin: 0 0 16px 0;
        }}

        .card-section-title {{
            color: var(--text);
            margin: 0 0 10px 0;
        }}

        .card-text {{
            color: var(--text);
            font-weight: 400;
            margin: 0 0 16px 0;
            font-size: 18px;
        }}

        .field-label {{
            color: var(--text);
            font-weight: 500;
            margin: 0 0 6px 0;
            font-size: 18px;
        }}

        .tag-cloud {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 6px 0 16px 0;
        }}

        .tag-pill {{
            display: inline-flex;
            align-items: center;
            padding: 6px 10px;
            border-radius: 6px;
            background: var(--tag-bg);
            color: var(--tag-text);
            font-size: 18px;
            line-height: 1.45;
            font-weight: 400;
        }}

        .tag-pill:hover {{
            background: var(--tag-hover);
        }}

        .research-card {{
            margin: 0 0 16px 0;
        }}

        .research-text {{
            color: var(--text);
            font-weight: 400;
            margin: 6px 0 0 0;
            font-size: 18px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# Вспомогательные функции
# =========================
def label(column: str) -> str:
    return LABELS.get(column, column)


def find_existing_file(candidates: list[str]) -> str:
    for filename in candidates:
        if Path(filename).exists():
            return filename
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
    return text.rstrip("0").rstrip(",")


def format_number(value, digits: int = 2) -> str:
    if pd.isna(value):
        return ""
    formatted = f"{float(value):,.{digits}f}"
    formatted = formatted.replace(",", " ").replace(".", ",")
    return trim_decimal_string(formatted)


def format_integer(value) -> str:
    if pd.isna(value):
        return ""
    return f"{int(round(float(value))):,}".replace(",", " ")


def format_percent(value, digits: int = 2) -> str:
    if pd.isna(value):
        return ""
    formatted = f"{float(value) * 100:.{digits}f}".replace(".", ",")
    return f"{trim_decimal_string(formatted)}%"


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

    return str(value)


def percent_to_internal(value: float) -> float:
    return value / 100


def internal_to_percent(value: float) -> float:
    return value * 100


def split_tags(value) -> list[str]:
    if pd.isna(value):
        return []
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
        if not text or text in seen:
            continue
        seen.add(text)
        cleaned.append(text)
    return ", ".join(cleaned)


def format_item_for_dict(dict_id: str, item_name: str, item_value, item_unit) -> str:
    name = str(item_name).strip()

    if pd.notna(item_value):
        value_text = format_number(item_value, 2)

        if dict_id == "seasonality_coeff":
            return f"{name} ×{value_text}"

        if dict_id in {"other_markup", "production", "targeting_markup"} and str(item_unit).strip() == "%":
            return f"{name} +{value_text}%"

        if str(item_unit).strip() == "%":
            return f"{name} +{value_text}%"

    return name


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

    if total_weight != 100:
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


def make_tag_html(text: str) -> str:
    return f'<span class="tag-pill">{html.escape(text)}</span>'


def make_tag_cloud(values: list[str]) -> str:
    if not values:
        return ""
    return f'<div class="tag-cloud">{"".join(make_tag_html(v) for v in values)}</div>'


def render_metrics(result_df: pd.DataFrame):
    metrics = [
        ("Форматов в выдаче", str(len(result_df))),
        ("Площадок", str(int(result_df["platform"].nunique()) if "platform" in result_df.columns else 0)),
        (
            "Средний eCPM со скидкой",
            format_number(result_df["ecpm_discounted"].mean(), 2) if "ecpm_discounted" in result_df.columns else "",
        ),
        (
            "Средний CTR",
            format_percent(result_df["ctr_avg"].mean()) if "ctr_avg" in result_df.columns else "",
        ),
    ]

    cols = st.columns(4)
    for col, (title, value) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{html.escape(title)}</div>
                    <div class="metric-value">{html.escape(value)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_table_cell(text: str, header: bool = False):
    css_class = "custom-header" if header else "custom-cell"
    st.markdown(f'<div class="{css_class}">{html.escape(text)}</div>', unsafe_allow_html=True)


def render_results_table(result_df: pd.DataFrame):
    st.markdown('<div class="table-wrap"><div class="table-min">', unsafe_allow_html=True)

    header_cols = st.columns(TABLE_RATIOS)
    headers = [
        "",
        "Скоринг",
        "Название формата",
        "Тип формата",
        "Площадка",
        "Модель закупки",
        "Минимальный бюджет",
        "Максимальный охват",
        "eCPM со скидкой",
        "CTR",
        "VTR",
        "Viewability",
        "Скидка",
        "Комиссия",
    ]

    for col, title in zip(header_cols, headers):
        with col:
            render_table_cell(title, header=True)

    for _, row in result_df.iterrows():
        selected = st.session_state.get("selected_format_id") == row["format_id"]
        row_cols = st.columns(TABLE_RATIOS)

        with row_cols[0]:
            if st.button(
                "Открыть",
                key=f"open_{row['format_id']}",
                use_container_width=True,
            ):
                st.session_state["selected_format_id"] = row["format_id"]
                st.rerun()

        row_values = [
            display_value("score", row.get("score")),
            str(row.get("format_name", "")),
            str(row.get("format_type", "")),
            str(row.get("platform", "")),
            str(row.get("buy_model", "")),
            display_value("min_budget", row.get("min_budget")),
            display_value("max_reach", row.get("max_reach")),
            display_value("ecpm_discounted", row.get("ecpm_discounted")),
            display_value("ctr_avg", row.get("ctr_avg")),
            display_value("vtr_avg", row.get("vtr_avg")),
            display_value("viewability_avg", row.get("viewability_avg")),
            display_value("discount", row.get("discount")),
            display_value("commission", row.get("commission")),
        ]

        for col, value in zip(row_cols[1:], row_values):
            with col:
                bg = COLORS["soft"] if selected else "#FFFFFF"
                st.markdown(
                    f'<div class="custom-cell" style="background:{bg};">{html.escape(value)}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("</div></div>", unsafe_allow_html=True)


def render_link_buttons(row: pd.Series):
    links = [
        ("Пример", row.get("example_url")),
        ("Технические требования", row.get("technical_requirements_url")),
        ("Медиакит", row.get("mediakit_url")),
        ("Кейсы", row.get("cases_url")),
    ]
    active_links = [(title, url) for title, url in links if pd.notna(url) and str(url).strip()]
    if not active_links:
        return

    cols = st.columns(len(active_links))
    for idx, (title, url) in enumerate(active_links):
        with cols[idx]:
            st.link_button(title, str(url), use_container_width=True)


def render_card(row: pd.Series):
    st.markdown('<div class="card-block">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="card-title">{html.escape(str(row.get("format_name", "Карточка формата")))}</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.2, 1])

    with left:
        description = row.get("description")
        if pd.notna(description) and str(description).strip():
            st.markdown('<div class="card-section-title">Описание</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-text">{html.escape(str(description))}</div>', unsafe_allow_html=True)

        meta_values = []
        for field in CARD_META_FIELDS:
            values = split_tags(row.get(field))
            if values:
                meta_values.append((label(field), values))

        if meta_values:
            st.markdown('<div class="card-section-title">Параметры формата</div>', unsafe_allow_html=True)
            for field_label, values in meta_values:
                st.markdown(f'<div class="field-label">{html.escape(field_label)}</div>', unsafe_allow_html=True)
                st.markdown(make_tag_cloud(values), unsafe_allow_html=True)

        tag_values = []
        for field in CARD_TAG_FIELDS:
            values = split_tags(row.get(field))
            if values:
                tag_values.append((label(field), values))

        if tag_values:
            st.markdown('<div class="card-section-title">Условия и надбавки</div>', unsafe_allow_html=True)
            for field_label, values in tag_values:
                st.markdown(f'<div class="field-label">{html.escape(field_label)}</div>', unsafe_allow_html=True)
                st.markdown(make_tag_cloud(values), unsafe_allow_html=True)

        st.markdown('<div class="card-section-title">Материалы</div>', unsafe_allow_html=True)
        render_link_buttons(row)

    with right:
        research_items = []

        if safe_scalar_to_bool(row.get("bls")):
            research_items.append(("BLS", row.get("bls_terms")))
        if safe_scalar_to_bool(row.get("sales_lift")):
            research_items.append(("Sales Lift", row.get("sales_lift_terms")))

        verification_items = []
        if str(row.get("verification_pixel", "")).strip() == "Да":
            verification_items.append("Верификация пикселем")
        if str(row.get("verification_js", "")).strip() == "Да":
            verification_items.append("Верификация JS-кодом")

        if verification_items:
            st.markdown('<div class="card-section-title">Верификация</div>', unsafe_allow_html=True)
            st.markdown(make_tag_cloud(verification_items), unsafe_allow_html=True)

        if research_items:
            st.markdown('<div class="card-section-title">Исследования</div>', unsafe_allow_html=True)
            for title, details in research_items:
                st.markdown('<div class="research-card">', unsafe_allow_html=True)
                st.markdown(make_tag_cloud([title]), unsafe_allow_html=True)
                if pd.notna(details) and str(details).strip():
                    st.markdown(
                        f'<div class="research-text">{html.escape(str(details))}</div>',
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        verification_terms = row.get("verification_terms")
        seasonality_terms = row.get("seasonality_terms")

        if (pd.notna(verification_terms) and str(verification_terms).strip()) or (
            pd.notna(seasonality_terms) and str(seasonality_terms).strip()
        ):
            st.markdown('<div class="card-section-title">Уточнения</div>', unsafe_allow_html=True)
            if pd.notna(verification_terms) and str(verification_terms).strip():
                st.markdown('<div class="field-label">Условия верификации</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="research-text">{html.escape(str(verification_terms))}</div>',
                    unsafe_allow_html=True,
                )
            if pd.notna(seasonality_terms) and str(seasonality_terms).strip():
                st.markdown('<div class="field-label" style="margin-top:10px;">Сезонность</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="research-text">{html.escape(str(seasonality_terms))}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)


def normalize_weight_state():
    weights = {metric: int(st.session_state.get(f"score_{metric}", 0)) for metric in SCORING_COLUMNS}
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
        dict_items[["dict_id", "item_id", "item_name", "item_value", "item_unit"]],
        on=["dict_id", "item_id"],
        how="left",
    )

    pivot_dict = {}
    for dict_id in merged_items["dict_id"].dropna().unique():
        grouped = (
            merged_items[merged_items["dict_id"] == dict_id]
            .assign(
                display_item=lambda x: x.apply(
                    lambda row: format_item_for_dict(
                        row["dict_id"],
                        row["item_name"],
                        row["item_value"],
                        row["item_unit"],
                    ),
                    axis=1,
                )
            )
            .groupby("format_id")["display_item"]
            .apply(lambda s: join_unique(sorted(pd.unique(s.dropna()))))
            .reset_index()
            .rename(columns={"display_item": dict_id})
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


try:
    df = load_data()
except Exception as e:
    st.error(f"Не удалось загрузить данные: {e}")
    st.stop()

if df.empty:
    st.warning("В данных нет строк.")
    st.stop()


st.markdown('<div class="page-title">Подбор форматов</div>', unsafe_allow_html=True)


with st.sidebar:
    st.markdown('<div class="sidebar-title">Поиск</div>', unsafe_allow_html=True)

    search_query = st.text_input(
        "Поиск",
        value="",
        label_visibility="collapsed",
    )

    filtered_df = apply_text_search(df, search_query)

    st.markdown('<div class="sidebar-group">Фильтры</div>', unsafe_allow_html=True)

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

    st.markdown(
        f'<div class="sidebar-count">Найдено форматов: {len(filtered_df)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-group">Скоринг</div>', unsafe_allow_html=True)

    scoring_enabled = st.checkbox("Включить скоринг", value=False, key="scoring_enabled")

    if scoring_enabled:
        st.markdown('<div class="sidebar-field">Сколько форматов показать</div>', unsafe_allow_html=True)
        st.number_input(
            "Сколько форматов показать",
            min_value=1,
            max_value=max(1, len(filtered_df)),
            value=min(int(st.session_state.get("top_n", 10)), max(1, len(filtered_df))),
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
        sum_color = "#FFFFFF" if total_weights == 100 else "#F8F2FF"
        st.markdown(
            f'<div class="sidebar-field" style="color:{sum_color};">Сумма: {total_weights}</div>',
            unsafe_allow_html=True,
        )

        if total_weights != 100:
            st.markdown(
                '<div class="sidebar-count">Сумма параметров должна быть равна 100</div>',
                unsafe_allow_html=True,
            )

        c1, c2 = st.columns(2)
        with c1:
            st.button("Нормализовать", use_container_width=True, on_click=normalize_weight_state)
        with c2:
            st.button("Сбросить", use_container_width=True, on_click=reset_weight_state)


result_df = filtered_df.copy()

if scoring_enabled:
    current_weights = {
        metric: int(st.session_state.get(f"score_{metric}", 0))
        for metric in SCORING_COLUMNS
    }
    result_df = add_scoring(result_df, current_weights)

    if sum(current_weights.values()) == 100:
        result_df = result_df.sort_values(by="score", ascending=False, na_position="last")
    else:
        result_df["score"] = np.nan

    requested_top_n = max(1, int(st.session_state.get("top_n", 10)))
    available_rows = len(result_df)
    actual_top_n = min(requested_top_n, available_rows)
    result_df = result_df.head(actual_top_n)
else:
    if "score" not in result_df.columns:
        result_df["score"] = np.nan
    available_rows = len(result_df)


render_metrics(result_df)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if scoring_enabled and sum(int(st.session_state.get(f"score_{metric}", 0)) for metric in SCORING_COLUMNS) != 100:
    st.markdown(
        '<div class="result-note">Скоринг не применен: сумма весов должна быть равна 100.</div>',
        unsafe_allow_html=True,
    )
elif scoring_enabled and available_rows < int(st.session_state.get("top_n", 10)):
    st.markdown(
        f'<div class="result-note">Показаны все доступные форматы: {available_rows}</div>',
        unsafe_allow_html=True,
    )

render_results_table(result_df)

selected_format_id = st.session_state.get("selected_format_id")
if selected_format_id is None and not result_df.empty:
    st.session_state["selected_format_id"] = result_df.iloc[0]["format_id"]
    selected_format_id = st.session_state["selected_format_id"]

if selected_format_id is not None and selected_format_id in result_df["format_id"].values:
    selected_row = result_df.loc[result_df["format_id"] == selected_format_id].iloc[0]
    render_card(selected_row)
