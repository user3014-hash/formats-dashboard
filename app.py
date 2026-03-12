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

        /* Поля и селекты */
        [data-testid="stSidebar"] [data-baseweb="input"] > div,
        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] > div {{
            background: #FFFFFF !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            outline: none !important;
            border-radius: 8px !important;
            min-height: 44px !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 !important;
            transition: border-color 0.15s ease !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="input"] > div:hover,
        [data-testid="stSidebar"] [data-baseweb="select"] > div:hover,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] > div:hover {{
            border: 1px solid #070037 !important;
            box-shadow: none !important;
            outline: none !important;
            background: #FFFFFF !important;
        }}

        [data-testid="stSidebar"] [data-baseweb="input"] > div:focus-within,
        [data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within,
        [data-testid="stSidebar"] [
