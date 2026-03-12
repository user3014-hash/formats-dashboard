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
    "table_header_bg": "#3E20FF",
    "table_header_text": "#FFFFFF",
    "row_hover": "#F8F2FF",
    "row_selected": "#F8F2FF",
    "border": "#D7B8FF",
    "tag_bg": "#725BFF",
    "tag_text": "#FFFFFF",
    "tag_hover": "#3E20FF",
    "input_bg": "#FFFFFF",
    "input_text": "#070037",
    "muted_text": "#070037",
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

COLUMN_WIDTHS = {
    "score": 120,
    "format_name": 260,
    "format_type": 140,
    "platform": 140,
    "buy_model": 140,
    "min_budget": 120,
    "max_reach": 120,
    "ecpm_discounted": 120,
    "ctr_avg": 120,
    "vtr_avg": 120,
    "viewability_avg": 120,
    "discount": 120,
    "commission": 120,
}

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

CARD_TEXT_FIELDS = [
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
# Стили
# =========================
st.markdown(
    f"""
    <style>
        html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
            font-family: {FONT_FAMILY};
        }}

        [data-testid="stAppViewContainer"] {{
            background: {COLORS["bg"]};
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 2rem;
        }}

        section[data-testid="stSidebar"] {{
            background: {COLORS["sidebar_bg"]};
        }}

        section[data-testid="stSidebar"] .block-container {{
            padding-top: 1rem;
            padding-bottom: 1.2rem;
        }}

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {{
            color: #FFFFFF !important;
        }}

        section[data-testid="stSidebar"] [data-baseweb="select"] > div,
        section[data-testid="stSidebar"] [data-baseweb="input"] > div,
        section[data-testid="stSidebar"] [data-testid="stNumberInput"] > div {{
            background: {COLORS["input_bg"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 10px !important;
            box-shadow: none !important;
            color: {COLORS["input_text"]} !important;
            min-height: 48px !important;
        }}

        section[data-testid="stSidebar"] input {{
            color: {COLORS["input_text"]} !important;
            font-size: 14px !important;
            caret-color: {COLORS["input_text"]} !important;
        }}

        section[data-testid="stSidebar"] input::placeholder {{
            color: rgba(7, 0, 55, 0.55) !important;
        }}

        section[data-testid="stSidebar"] [data-baseweb="select"] * {{
            color: {COLORS["input_text"]} !important;
            font-size: 14px !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {{
            padding-right: 52px !important;
            padding-left: 14px !important;
            color: {COLORS["input_text"]} !important;
            font-size: 14px !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {{
            color: {COLORS["input_text"]} !important;
            background: transparent !important;
            border: none !important;
        }}

        section[data-testid="stSidebar"] [data-baseweb="tag"] {{
            background: {COLORS["tag_bg"]} !important;
            border: 1px solid {COLORS["tag_bg"]} !important;
            border-radius: 6px !important;
            color: {COLORS["tag_text"]} !important;
        }}

        section[data-testid="stSidebar"] [data-baseweb="tag"] span {{
            color: {COLORS["tag_text"]} !important;
        }}

        section[data-testid="stSidebar"] [data-baseweb="tag"]:hover {{
            background: {COLORS["tag_hover"]} !important;
            border-color: {COLORS["tag_hover"]} !important;
        }}

        section[data-testid="stSidebar"] [data-baseweb="popover"] *,
        div[data-baseweb="popover"] *,
        [role="listbox"] * {{
            color: {COLORS["text"]} !important;
        }}

        div[data-baseweb="popover"] {{
            background: #FFFFFF !important;
        }}

        div[data-baseweb="popover"] [role="option"] {{
            background: #FFFFFF !important;
        }}

        div[data-baseweb="popover"] [role="option"]:hover {{
            background: {COLORS["row_hover"]} !important;
        }}

        [data-testid="stSidebar"] input[type="checkbox"] {{
            accent-color: {COLORS["tag_bg"]} !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {{
            background: {COLORS["tag_bg"]} !important;
            border-color: {COLORS["tag_bg"]} !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="slider"] > div > div {{
            background: rgba(255,255,255,0.35) !important;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            background: #FFFFFF !important;
            color: {COLORS["text"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 10px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            height: 44px !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            border-color: #FFFFFF !important;
            background: #F8F2FF !important;
            color: {COLORS["text"]} !important;
        }}

        .sidebar-title {{
            font-size: 18px;
            font-weight: 600;
            color: #FFFFFF;
            margin: 0 0 16px 0;
        }}

        .sidebar-group {{
            font-size: 18px;
            font-weight: 600;
            color: #FFFFFF;
            margin: 32px 0 16px 0;
        }}

        .sidebar-field {{
            font-size: 14px;
            font-weight: 500;
            color: #FFFFFF;
            margin: 20px 0 8px 0;
        }}

        .page-title {{
            font-size: 32px;
            font-weight: 700;
            color: {COLORS["text"]};
            margin: 0 0 24px 0;
            line-height: 1.1;
        }}

        .divider {{
            height: 1px;
            background: {COLORS["border"]};
            margin: 32px 0;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }}

        .metric-card {{
            background: #FFFFFF;
            border: 1px solid {COLORS["border"]};
            border-radius: 16px;
            padding: 20px;
            min-height: 112px;
        }}

        .metric-label {{
            font-size: 14px;
            font-weight: 500;
            color: {COLORS["text"]};
            opacity: 0.85;
            line-height: 1.3;
            margin-bottom: 12px;
        }}

        .metric-value {{
            font-size: 32px;
            font-weight: 700;
            line-height: 1;
            color: {COLORS["text"]};
        }}

        .result-note {{
            font-size: 14px;
            color: {COLORS["text"]};
            margin-top: -16px;
            margin-bottom: 24px;
        }}

        .table-wrap {{
            width: 100%;
            overflow-x: auto;
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
        }}

        table.custom-table {{
            width: 100%;
            min-width: 1560px;
            border-collapse: collapse;
            background: #FFFFFF;
        }}

        table.custom-table thead th {{
            background: {COLORS["table_header_bg"]};
            color: {COLORS["table_header_text"]};
            font-size: 13px;
            font-weight: 600;
            text-align: left;
            padding: 14px 12px;
            border-right: 1px solid rgba(255,255,255,0.18);
            white-space: nowrap;
        }}

        table.custom-table thead th:last-child {{
            border-right: none;
        }}

        table.custom-table tbody td {{
            font-size: 13px;
            font-weight: 400;
            color: {COLORS["text"]};
            padding: 14px 12px;
            border-top: 1px solid {COLORS["border"]};
            vertical-align: top;
            white-space: nowrap;
            background: #FFFFFF;
        }}

        table.custom-table tbody tr.selected td {{
            background: {COLORS["row_selected"]};
        }}

        table.custom-table tbody tr:hover td {{
            background: {COLORS["row_hover"]};
        }}

        .card-block {{
            border: 1px solid {COLORS["border"]};
            border-radius: 16px;
            padding: 24px;
            background: #FFFFFF;
            margin-top: 32px;
        }}

        .card-title {{
            font-size: 32px;
            font-weight: 700;
            line-height: 1.1;
            color: {COLORS["text"]};
            margin-bottom: 24px;
        }}

        .card-section-title {{
            font-size: 18px;
            font-weight: 600;
            line-height: 1.2;
            color: {COLORS["text"]};
            margin: 0 0 16px 0;
        }}

        .card-text {{
            font-size: 16px;
            font-weight: 400;
            line-height: 1.65;
            color: {COLORS["text"]};
            margin-bottom: 24px;
        }}

        .field-label {{
            font-size: 14px;
            font-weight: 500;
            color: {COLORS["text"]};
            margin: 0 0 8px 0;
        }}

        .tag-cloud {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 8px 0 20px 0;
        }}

        .tag-pill {{
            display: inline-flex;
            align-items: center;
            padding: 6px 10px;
            border-radius: 6px;
            background: {COLORS["tag_bg"]};
            color: {COLORS["tag_text"]};
            font-size: 14px;
            font-weight: 400;
            line-height: 1.2;
            transition: background 0.15s ease;
        }}

        .tag-pill:hover {{
            background: {COLORS["tag_hover"]};
        }}

        @media (max-width: 1100px) {{
            .metrics-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
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

    return value


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

        if dict_id in {"other_markup", "production"} and str(item_unit).strip() == "%":
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


def build_display_table(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    visible_cols = [c for c in columns if c in df.columns]
    display_df = df[visible_cols].copy()

    rename_map = {c: label(c) for c in visible_cols}
    display_df = display_df.rename(columns=rename_map)

    for raw_col in visible_cols:
        pretty_col = rename_map[raw_col]
        display_df[pretty_col] = display_df[pretty_col].apply(lambda x: display_value(raw_col, x))

    return display_df


def make_tag_html(text: str) -> str:
    return f'<span class="tag-pill">{html.escape(text)}</span>'


def make_tag_cloud(values: list[str]) -> str:
    if not values:
        return ""
    return f'<div class="tag-cloud">{"".join(make_tag_html(v) for v in values)}</div>'


def render_metrics(result_df: pd.DataFrame):
    cards = [
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

    html_cards = []
    for title, value in cards:
        html_cards.append(
            f"""
            <div class="metric-card">
                <div class="metric-label">{html.escape(title)}</div>
                <div class="metric-value">{html.escape(value)}</div>
            </div>
            """
        )

    st.markdown(f'<div class="metrics-grid">{"".join(html_cards)}</div>', unsafe_allow_html=True)


def render_html_table(display_df: pd.DataFrame, raw_df: pd.DataFrame, selected_format_id: str | None):
    headers = []
    for col in display_df.columns:
        raw_col = next((k for k, v in LABELS.items() if v == col), None)
        width = COLUMN_WIDTHS.get(raw_col, 120)
        headers.append(f'<th style="min-width:{width}px;width:{width}px;">{html.escape(col)}</th>')

    rows_html = []
    for idx, (_, row) in enumerate(display_df.iterrows()):
        raw_row = raw_df.iloc[idx]
        row_class = "selected" if str(raw_row.get("format_id")) == str(selected_format_id) else ""
        cells = []
        for col in display_df.columns:
            raw_col = next((k for k, v in LABELS.items() if v == col), None)
            width = COLUMN_WIDTHS.get(raw_col, 120)
            value = "" if pd.isna(row[col]) else str(row[col])
            cells.append(f'<td style="min-width:{width}px;width:{width}px;">{html.escape(value)}</td>')
        rows_html.append(f'<tr class="{row_class}">{"".join(cells)}</tr>')

    table_html = f"""
    <div class="table-wrap">
        <table class="custom-table">
            <thead>
                <tr>{''.join(headers)}</tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)


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

    with right:
        status_tags = []
        if str(row.get("verification_pixel", "")).strip() == "Да":
            status_tags.append("Верификация пикселем")
        if str(row.get("verification_js", "")).strip() == "Да":
            status_tags.append("Верификация JS-кодом")
        if safe_scalar_to_bool(row.get("bls")):
            status_tags.append("BLS")
        if safe_scalar_to_bool(row.get("sales_lift")):
            status_tags.append("Sales Lift")

        if status_tags:
            st.markdown('<div class="card-section-title">Обязательные параметры</div>', unsafe_allow_html=True)
            st.markdown(make_tag_cloud(status_tags), unsafe_allow_html=True)

        text_values = []
        for field in CARD_TEXT_FIELDS:
            value = row.get(field)
            if pd.notna(value) and str(value).strip():
                text_values.append((label(field), str(value)))

        if text_values:
            st.markdown('<div class="card-section-title">Уточнения</div>', unsafe_allow_html=True)
            for field_label, value in text_values:
                st.markdown(f'<div class="field-label">{html.escape(field_label)}</div>', unsafe_allow_html=True)
                st.write(value)

    st.markdown('<div class="card-section-title">Материалы</div>', unsafe_allow_html=True)
    render_link_buttons(row)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# Коллбэки
# =========================
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


# =========================
# Загрузка данных
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


# =========================
# Состояние
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
# Данные
# =========================
try:
    df = load_data()
except Exception as e:
    st.error(f"Не удалось загрузить данные: {e}")
    st.stop()

if df.empty:
    st.warning("В данных нет строк.")
    st.stop()


# =========================
# Заголовок
# =========================
st.markdown('<div class="page-title">Подбор форматов</div>', unsafe_allow_html=True)


# =========================
# Левая панель
# =========================
with st.sidebar:
    st.markdown('<div class="sidebar-title">Поиск</div>', unsafe_allow_html=True)

    search_query = st.text_input(
        "Поиск",
        placeholder="Название, площадка, описание",
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
            st.markdown(f'<div class="sidebar-field">{label(col)}</div>', unsafe_allow_html=True)
            required = st.checkbox(label(col), value=False, key=f"required_{col}", label_visibility="collapsed")
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
        st.markdown('<div class="sidebar-field">Сколько форматов показать</div>', unsafe_allow_html=True)
        st.number_input(
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
        st.markdown(f'<div class="sidebar-field">Сумма: {total_weights}</div>', unsafe_allow_html=True)

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


# =========================
# Правая панель
# =========================
render_metrics(result_df)

if scoring_enabled and requested_top_n is not None and available_rows < requested_top_n:
    st.markdown(
        f'<div class="result-note">Показаны все доступные форматы: {available_rows}</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

table_columns = [c for c in TABLE_COLUMNS if c in result_df.columns]
if not scoring_enabled and "score" in table_columns:
    table_columns.remove("score")

display_df = build_display_table(result_df, table_columns)
selected_format_id = st.session_state.get("selected_format_id")

render_html_table(display_df, result_df, selected_format_id)

if not result_df.empty:
    options_df = result_df[["format_id", "format_name"]].copy()
    options_df["card_label"] = (
        options_df["format_name"].fillna("Без названия").astype(str)
        + " | "
        + options_df["format_id"].fillna("—").astype(str)
    )

    current_idx = 0
    if selected_format_id is not None and selected_format_id in options_df["format_id"].values:
        current_idx = int(options_df.index[options_df["format_id"] == selected_format_id][0])

    selected_label = st.selectbox(
        "Формат для карточки",
        options_df["card_label"].tolist(),
        index=min(current_idx, len(options_df) - 1),
        label_visibility="collapsed",
    )

    selected_format_id = options_df.loc[options_df["card_label"] == selected_label, "format_id"].iloc[0]
    st.session_state["selected_format_id"] = selected_format_id

if selected_format_id is not None and selected_format_id in result_df["format_id"].values:
    selected_row = result_df.loc[result_df["format_id"] == selected_format_id].iloc[0]
    render_card(selected_row)
