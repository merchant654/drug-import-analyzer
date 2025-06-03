import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="تحلیل واردات دارویی", layout="wide")

st.title("📊 داشبورد تحلیل هزینه واردات دارو")

# --- آپلود فایل‌ها ---
st.sidebar.header("آپلود فایل‌ها")
import_file = st.sidebar.file_uploader("➕ فایل واردات دارو", type=["xlsx"])
rate_file = st.sidebar.file_uploader("➕ فایل نرخ ارز", type=["xlsx"])

if import_file and rate_file:
    try:
        import_df = pd.read_excel(import_file)
        rate_df = pd.read_excel(rate_file)

        # تبدیل تاریخ‌ها
        import_df["تاریخ خرید"] = pd.to_datetime(import_df["تاریخ خرید"], format="%Y/%m/%d")
        rate_df["تاریخ"] = pd.to_datetime(rate_df["تاریخ"], format="%Y/%m/%d")

        # ادغام نرخ ارز با داده‌های واردات
        merged = pd.merge(import_df, rate_df, how="left",
                          left_on=["تاریخ خرید", "نوع ارز"],
                          right_on=["تاریخ", "نوع ارز"])

        # محاسبه قیمت ریالی
        merged["قیمت تمام‌شده (ریال)"] = merged["مقدار (کیلو)"] * merged["قیمت دلاری"] * merged["نرخ ارز"]

        # نمایش جدول نهایی
        st.subheader("📄 جدول قیمت تمام‌شده واردات")
        st.dataframe(merged[["ماده", "مقدار (کیلو)", "قیمت دلاری", "نوع ارز", "نرخ ارز", "قیمت تمام‌شده (ریال)"]])

        # مجموع کل
        total_cost = merged["قیمت تمام‌شده (ریال)"].sum()
        st.success(f"💰 جمع کل هزینه واردات: {total_cost:,.0f} ریال")

        # رسم نمودار نرخ ارز
        st.subheader("📈 روند تغییرات نرخ ارز")
        fig = px.line(rate_df, x="تاریخ", y="نرخ ارز", color="نوع ارز",
                      title="روند نرخ ارز به تفکیک نوع ارز", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"خطا در پردازش فایل‌ها: {e}")
else:
    st.info("لطفاً هر دو فایل را در نوار کناری بارگذاری کنید.")
