import streamlit as st
import pandas as pd
import plotly.express as px
import io
import requests

# 📌 تابع نرخ جهانی دلار (تقریبی)
@st.cache_data(ttl=600)
def get_usd_to_irr():
    try:
        url = "https://api.exchangerate.host/latest?base=USD&symbols=IRR"
        r = requests.get(url, timeout=5)
        rate = r.json()['rates']['IRR']
        return round(rate)
    except:
        return None

# 🧭 تنظیمات اولیه داشبورد
st.set_page_config(page_title="تحلیل واردات دارویی", layout="wide")
st.title("📊 داشبورد تحلیل هزینه واردات دارو")

# 💵 نمایش نرخ دلار جهانی
rate = get_usd_to_irr()
if rate:
    st.metric("💵 نرخ جهانی دلار (تقریبی)", f"{rate:,} ریال")
else:
    st.warning("❌ نرخ لحظه‌ای قابل دریافت نیست.")

# --- 📁 آپلود فایل‌ها ---
st.sidebar.header("آپلود فایل‌ها")
import_file = st.sidebar.file_uploader("➕ فایل واردات دارو", type=["xlsx"])
rate_file = st.sidebar.file_uploader("➕ فایل نرخ ارز", type=["xlsx"])

# --- ✅ تحلیل و نمایش ---
if import_file and rate_file:
    try:
        # خواندن فایل‌ها
        import_df = pd.read_excel(import_file)
        rate_df = pd.read_excel(rate_file)

        # تبدیل تاریخ‌ها به فرمت datetime
        import_df["تاریخ خرید"] = pd.to_datetime(import_df["تاریخ خرید"], format="%Y/%m/%d")
        rate_df["تاریخ"] = pd.to_datetime(rate_df["تاریخ"], format="%Y/%m/%d")

        # ادغام نرخ ارز با داده‌های واردات
        merged = pd.merge(import_df, rate_df, how="left",
                          left_on=["تاریخ خرید", "نوع ارز"],
                          right_on=["تاریخ", "نوع ارز"])

        # محاسبه قیمت ریالی
