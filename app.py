import streamlit as st
import pandas as pd

st.set_page_config(page_title="Подбор форматов", layout="wide")

st.title("Подбор форматов")
st.write("Это первая тестовая версия приложения. Дальше мы добавим таблицу, фильтры и скоринг.")

data = pd.DataFrame([
    {
        "Формат": "Формат 1",
        "Цена": 100000,
        "Охват": 500000,
        "Описание": "Тестовое описание формата"
    },
    {
        "Формат": "Формат 2",
        "Цена": 150000,
        "Охват": 650000,
        "Описание": "Еще один тестовый формат"
    }
])

st.subheader("Тестовая таблица")
st.dataframe(data, use_container_width=True)
