import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Mini Dashboard", layout="wide")

st.title("📊 Mini Sales Dashboard")

# ---------- Sidebar filters ----------
with st.sidebar:
    st.header("Filters")
    year = st.selectbox("Year", [2023, 2024, 2025])
    min_revenue = st.slider("Min revenue", 0, 100000, 20000, step=5000)

# ---------- Fake data ----------
np.random.seed(42)
df = pd.DataFrame({
    "year": np.random.choice([2023, 2024, 2025], size=200),
    "region": np.random.choice(["Europe", "Asia", "Americas"], size=200),
    "revenue": np.random.randint(5_000, 100_000, size=200),
})

# Apply filters
filtered = df[(df["year"] == year) & (df["revenue"] >= min_revenue)]

st.caption(f"Showing {len(filtered)} rows for year {year} with revenue ≥ {min_revenue}")

# ---------- Layout ----------
col1, col2 = st.columns(2)

with col1:
    with st.expander("ℹ️ What this chart shows"):
        st.write("This bar chart displays **total revenue by each region** after filters are applied.")
    st.subheader("Revenue by Region")
    rev_by_region = filtered.groupby("region")["revenue"].sum()
    st.bar_chart(rev_by_region)

with col2:
    with st.expander("ℹ️ What this chart shows"):
        st.write("This area chart shows the **distribution of revenue values** for the selected filters.")
    st.subheader("Revenue Distribution")
    st.area_chart(filtered["revenue"])

# ---------- Data Table ----------
with st.expander("📄 See filtered data"):
    st.dataframe(filtered)
