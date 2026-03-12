import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Подбор форматов", layout="wide")


# =========================
# Настройки
# =========================
DEFAULT_CSV_NAME = "DataLens - formats.csv"

TEXT_COLUMNS_FOR_SEARCH = [
    "format_id",
    "format_name",
    "platform",
    "type_service",
    "description",
    "buy_model",
]

PRIMARY_CATEGORICAL_FILTERS = [
    "type_service",
    "platform",
    "buy_model",
    "verification_pixel",
    "verification_js",
]

PRIMARY_NUMERIC_FILTERS = [
    "min_budget",
    "max_reach",
    "ecpm_discounted",
    "ctr_avg",
    "vtr_avg",
    "viewability_avg",
    "commission",
    "discount",
]

DETAIL_COLUMNS = [
    "format_id",
    "format_name",
    "type_service",
    "platform",
    "buy_model",
    "description",
    "max_reach",
    "min_budget",
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
    "example_url",
    "technical_requirements_url",
    "mediakit_url",
    "cases_url",
    "seasonality_terms",
    "bls_terms",
    "sales_lift_terms",
]

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
]


# =========================
# Вспомогательные функции
# =========================
def safe_to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def to_rate(series: pd.Series) -> pd.Series:
    """
    Приводит значения к долям:
    0.15 -> 0.15
    15 -> 0.15
    """
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


@st.cache_data
def load_data(uploaded_file) -> pd.DataFrame:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(DEFAULT_CSV_NAME)

    df.columns = [c.strip() for c in df.columns]

    # Приводим известные числовые поля
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

    # Чистим да/нет поля
    for col in ["verification_pixel", "verification_js"]:
        if col in df.columns:
            df[col] = clean_yes_no(df[col])

    # Нормализуем доли
    for col in ["discount", "commission", "ctr_avg", "vtr_avg", "viewability_avg", "bls", "sales_lift"]:
        if col in df.columns:
            df[col] = to_rate(df[col])

    # Приводим модель закупки к верхнему регистру
    if "buy_model" in df.columns:
        df["buy_model"] = df["buy_model"].astype(str).str.strip().str.upper()

    # Считаем eCPM
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


def format_percent(value) -> str:
    if pd.isna(value):
        return "—"
    return f"{value * 100:.2f}%"


def format_number(value, digits: int = 2) -> str:
    if pd.isna(value):
        return "—"
    return f"{value:,.{digits}f}".replace(",", " ")


def apply_text_search(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query.strip():
        return df

    search_cols = [c for c in TEXT_COLUMNS_FOR_SEARCH if c in df.columns]
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


def apply_numeric_range_filter(df: pd.DataFrame, column: str, min_value: float, max_value: float) -> pd.DataFrame:
    if column not in df.columns:
        return df
    return df[df[column].between(min_value, max_value, inclusive="both") | df[column].isna()]


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


def add_scoring(df: pd.DataFrame, weights: dict) -> pd.DataFrame:
    scored = df.copy()

    metrics_config = {
        "max_reach": {"weight": weights.get("max_reach", 0), "reverse": False},
        "ecpm_discounted": {"weight": weights.get("ecpm_discounted", 0), "reverse": True},
        "ctr_avg": {"weight": weights.get("ctr_avg", 0), "reverse": False},
        "vtr_avg": {"weight": weights.get("vtr_avg", 0), "reverse": False},
        "viewability_avg": {"weight": weights.get("viewability_avg", 0), "reverse": False},
        "commission": {"weight": weights.get("commission", 0), "reverse": False},
    }

    total_weight = sum(v["weight"] for v in metrics_config.values() if v["weight"] > 0)

    if total_weight == 0:
        scored["score"] = np.nan
        return scored

    score = pd.Series(0.0, index=scored.index)

    for metric, config in metrics_config.items():
        if metric in scored.columns and config["weight"] > 0:
            normalized = normalize_series(scored[metric], reverse=config["reverse"])
            score += normalized * config["weight"]

    scored["score"] = score / total_weight
    return scored


def display_link(label: str, url: str):
    if pd.notna(url) and str(url).strip():
        st.markdown(f"**{label}:** [открыть]({url})")


# =========================
# Загрузка данных
# =========================
st.title("Подбор форматов")
st.caption("Каталог, фильтры, сортировка и скоринг форматов в одном интерфейсе")

with st.sidebar:
    st.header("Данные")

    uploaded_file = st.file_uploader(
        "Загрузи CSV с форматами",
        type=["csv"],
        help="Если файл не загружен, приложение попробует прочитать DataLens - formats.csv из репозитория.",
    )

try:
    df = load_data(uploaded_file)
except FileNotFoundError:
    st.error(
        "Файл с данными не найден. Либо загрузи CSV через sidebar, либо добавь файл "
        "`DataLens - formats.csv` в репозиторий рядом с app.py."
    )
    st.stop()
except Exception as e:
    st.error(f"Не удалось прочитать файл: {e}")
    st.stop()

if df.empty:
    st.warning("Файл прочитан, но в нем нет строк.")
    st.stop()


# =========================
# Sidebar: фильтры и скоринг
# =========================
with st.sidebar:
    st.header("Поиск и фильтры")

    search_query = st.text_input("Поиск по названию, платформе, описанию")

    filtered_df = apply_text_search(df, search_query)

    st.subheader("Основные фильтры")
    for col in PRIMARY_CATEGORICAL_FILTERS:
        if col in filtered_df.columns:
            options = sorted([x for x in filtered_df[col].dropna().unique().tolist()])
            selected = st.multiselect(f"{col}", options)
            filtered_df = apply_categorical_filter(filtered_df, col, selected)

    with st.expander("Дополнительные категориальные фильтры"):
        extra_categorical_cols = [
            c for c in filtered_df.columns
            if (
                filtered_df[c].dtype == "object"
                and c not in PRIMARY_CATEGORICAL_FILTERS
                and c not in ["description", "example_url", "technical_requirements_url", "mediakit_url", "cases_url"]
            )
        ]

        for col in sorted(extra_categorical_cols):
            values = sorted([x for x in filtered_df[col].dropna().unique().tolist()])
            if 1 <= len(values) <= 50:
                selected = st.multiselect(col, values, key=f"extra_cat_{col}")
                filtered_df = apply_categorical_filter(filtered_df, col, selected)

    st.subheader("Числовые фильтры")
    for col in PRIMARY_NUMERIC_FILTERS:
        if col in filtered_df.columns:
            numeric_series = safe_to_numeric(filtered_df[col]).dropna()
            if numeric_series.empty:
                continue

            min_val = float(numeric_series.min())
            max_val = float(numeric_series.max())

            if min_val == max_val:
                continue

            selected_range = st.slider(
                col,
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val),
                key=f"slider_{col}",
            )
            filtered_df = apply_numeric_range_filter(
                filtered_df,
                col,
                selected_range[0],
                selected_range[1],
            )

    with st.expander("Скоринг"):
        scoring_enabled = st.checkbox("Включить скоринг", value=False)

        weights = {
            "max_reach": 0,
            "ecpm_discounted": 0,
            "ctr_avg": 0,
            "vtr_avg": 0,
            "viewability_avg": 0,
            "commission": 0,
        }
        top_n = 10

        if scoring_enabled:
            st.caption("0 — параметр не учитывается, 5 — очень важен")
            weights["max_reach"] = st.slider("Вес max_reach", 0, 5, 3)
            weights["ecpm_discounted"] = st.slider("Вес eCPM after discount", 0, 5, 4)
            weights["ctr_avg"] = st.slider("Вес CTR", 0, 5, 3)
            weights["vtr_avg"] = st.slider("Вес VTR", 0, 5, 2)
            weights["viewability_avg"] = st.slider("Вес viewability", 0, 5, 2)
            weights["commission"] = st.slider("Вес commission", 0, 5, 3)
            top_n = st.slider("Сколько форматов показать в топе", 3, 30, 10)

# Применяем скоринг после всех фильтров
result_df = filtered_df.copy()
if "score" in result_df.columns:
    result_df = result_df.drop(columns=["score"])

if "buy_model" in result_df.columns:
    result_df["buy_model"] = result_df["buy_model"].fillna("—")

if "scoring_enabled" in locals() and scoring_enabled:
    result_df = add_scoring(result_df, weights)
    result_df = result_df.sort_values(by="score", ascending=False, na_position="last")


# =========================
# Верхние метрики
# =========================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Всего форматов после фильтров", len(result_df))
col2.metric(
    "Платформ",
    int(result_df["platform"].nunique()) if "platform" in result_df.columns else 0
)
col3.metric(
    "Средний eCPM after discount",
    format_number(result_df["ecpm_discounted"].mean()) if "ecpm_discounted" in result_df.columns else "—"
)
col4.metric(
    "Средний CTR",
    format_percent(result_df["ctr_avg"].mean()) if "ctr_avg" in result_df.columns else "—"
)

st.divider()


# =========================
# Основная зона
# =========================
tab1, tab2, tab3 = st.tabs(["Каталог", "Топ по скорингу", "Карточка формата"])

with tab1:
    st.subheader("Каталог форматов")

    table_df = result_df.copy()

    visible_table_cols = [c for c in TABLE_COLUMNS if c in table_df.columns]
    if "score" in table_df.columns:
        visible_table_cols = ["score"] + visible_table_cols

    sort_options = visible_table_cols.copy()
    if not sort_options:
        st.warning("Нет столбцов для показа.")
    else:
        sort_col_1, sort_col_2 = st.columns([2, 1])
        with sort_col_1:
            sort_by = st.selectbox("Сортировать по", sort_options, index=0)
        with sort_col_2:
            ascending = st.selectbox("Порядок", ["По убыванию", "По возрастанию"])

        table_df = table_df.sort_values(
            by=sort_by,
            ascending=(ascending == "По возрастанию"),
            na_position="last",
        )

        display_df = table_df[visible_table_cols].copy()

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        csv_bytes = display_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "Скачать текущую выборку CSV",
            data=csv_bytes,
            file_name="filtered_formats.csv",
            mime="text/csv",
        )

with tab2:
    st.subheader("Топ форматов")

    if "scoring_enabled" not in locals() or not scoring_enabled:
        st.info("Включи скоринг в sidebar, чтобы увидеть рейтинг.")
    elif "score" not in result_df.columns or result_df["score"].notna().sum() == 0:
        st.warning("Скоринг включен, но итоговый score не получился. Проверь веса и данные.")
    else:
        top_df = result_df[result_df["score"].notna()].head(top_n).copy()

        if top_df.empty:
            st.warning("После фильтров не осталось форматов для топа.")
        else:
            top_cols = ["score"] + [c for c in TABLE_COLUMNS if c in top_df.columns]
            st.dataframe(
                top_df[top_cols],
                use_container_width=True,
                hide_index=True,
            )

with tab3:
    st.subheader("Карточка формата")

    if result_df.empty:
        st.info("После фильтров ничего не осталось.")
    else:
        options_df = result_df.copy()
        options_df["card_label"] = (
            options_df["format_name"].fillna("Без названия").astype(str)
            + " | "
            + options_df["format_id"].fillna("—").astype(str)
        )

        selected_label = st.selectbox(
            "Выбери формат",
            options_df["card_label"].tolist(),
        )

        selected_row = options_df.loc[options_df["card_label"] == selected_label].iloc[0]

        left, right = st.columns([1.3, 1])

        with left:
            st.markdown(f"## {selected_row.get('format_name', 'Без названия')}")
            st.markdown(f"**ID:** {selected_row.get('format_id', '—')}")
            st.markdown(f"**Платформа:** {selected_row.get('platform', '—')}")
            st.markdown(f"**Тип сервиса:** {selected_row.get('type_service', '—')}")
            st.markdown(f"**Модель закупки:** {selected_row.get('buy_model', '—')}")

            description = selected_row.get("description", "")
            if pd.notna(description) and str(description).strip():
                st.markdown("### Описание")
                st.write(description)

            st.markdown("### Ссылки")
            display_link("Пример", selected_row.get("example_url"))
            display_link("Технические требования", selected_row.get("technical_requirements_url"))
            display_link("Медиакит", selected_row.get("mediakit_url"))
            display_link("Кейсы", selected_row.get("cases_url"))

            if pd.notna(selected_row.get("verification_terms")) and str(selected_row.get("verification_terms")).strip():
                st.markdown("### Условия верификации")
                st.write(selected_row.get("verification_terms"))

            if pd.notna(selected_row.get("seasonality_terms")) and str(selected_row.get("seasonality_terms")).strip():
                st.markdown("### Сезонность")
                st.write(selected_row.get("seasonality_terms"))

        with right:
            st.markdown("### Ключевые метрики")

            metric_col_1, metric_col_2 = st.columns(2)
            metric_col_1.metric("Min budget", format_number(selected_row.get("min_budget"), 0))
            metric_col_2.metric("Max reach", format_number(selected_row.get("max_reach"), 0))

            metric_col_3, metric_col_4 = st.columns(2)
            metric_col_3.metric("Discount", format_percent(selected_row.get("discount")))
            metric_col_4.metric("Commission", format_percent(selected_row.get("commission")))

            metric_col_5, metric_col_6 = st.columns(2)
            metric_col_5.metric("eCPM base", format_number(selected_row.get("ecpm_base")))
            metric_col_6.metric("eCPM after discount", format_number(selected_row.get("ecpm_discounted")))

            metric_col_7, metric_col_8 = st.columns(2)
            metric_col_7.metric("CTR", format_percent(selected_row.get("ctr_avg")))
            metric_col_8.metric("VTR", format_percent(selected_row.get("vtr_avg")))

            metric_col_9, metric_col_10 = st.columns(2)
            metric_col_9.metric("Viewability", format_percent(selected_row.get("viewability_avg")))
            metric_col_10.metric("Score", format_number(selected_row.get("score"), 3) if "score" in selected_row else "—")

            st.markdown("### Дополнительно")
            st.write(f"**Verification pixel:** {selected_row.get('verification_pixel', '—')}")
            st.write(f"**Verification JS:** {selected_row.get('verification_js', '—')}")
            st.write(f"**BLS:** {format_percent(selected_row.get('bls'))}")
            st.write(f"**Sales lift:** {format_percent(selected_row.get('sales_lift'))}")

            if pd.notna(selected_row.get("bls_terms")) and str(selected_row.get("bls_terms")).strip():
                st.write("**BLS terms:**")
                st.write(selected_row.get("bls_terms"))

            if pd.notna(selected_row.get("sales_lift_terms")) and str(selected_row.get("sales_lift_terms")).strip():
                st.write("**Sales lift terms:**")
                st.write(selected_row.get("sales_lift_terms"))

        with st.expander("Показать все поля этой строки"):
            all_fields = {}
            for col in DETAIL_COLUMNS:
                if col in selected_row.index:
                    all_fields[col] = selected_row.get(col)

            st.json(all_fields)
