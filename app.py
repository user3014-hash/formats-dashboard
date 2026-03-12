st.markdown(
    """
    <style>

        :root {
            --sidebar-bg: #3E20FF;
            --page-bg: #FFFFFF;
            --text-main: #070037;
        }

        /* фон страницы */

        [data-testid="stAppViewContainer"] {
            background: var(--page-bg);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        /* левая панель */

        section[data-testid="stSidebar"] {
            background: var(--sidebar-bg);
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 24px;
            padding-left: 24px;
            padding-right: 20px;
        }

        /* заголовок "Поиск" */

        .sidebar-title {
            font-size: 20px;
            font-weight: 600;
            color: #FFFFFF;
        }

        /* поле поиска */

        [data-testid="stSidebar"] [data-baseweb="input"] > div {
            background: #FFFFFF;
            border: none;
            box-shadow: none;
            outline: none;
            border-radius: 8px;
            min-height: 40px;
        }

        /* текст, который вводит пользователь */

        [data-testid="stSidebar"] input {
            font-size: 18px;
            font-weight: 400;
            color: #070037;
            caret-color: #070037;
            padding-left: 12px;
            padding-right: 12px;
            line-height: 1.4;
        }

        /* hover */

        [data-testid="stSidebar"] [data-baseweb="input"] > div:hover {
            border: 1px solid #070037;
        }

        /* focus */

        [data-testid="stSidebar"] [data-baseweb="input"] > div:focus-within {
            border: 1px solid #070037;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

search_query = st.text_input(
    "Поиск",
    value="",
    label_visibility="collapsed",
)
