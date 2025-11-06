import pandas as pd
import streamlit as st
from io import StringIO

# -----------------------------
# 1️⃣ NIFTY 50 Constituents + Weights
# -----------------------------
data = [
    ("RELIANCE INDUSTRIES LTD", 9.91, "Energy/Refineries"),
    ("HDFC BANK LTD", 7.41, "Banking"),
    ("BHARTI AIRTEL LTD", 6.25, "Telecom"),
    ("TATA CONSULTANCY SERVICES LTD", 5.33, "IT"),
    ("ICICI BANK LTD", 4.62, "Banking"),
    ("STATE BANK OF INDIA", 4.34, "Banking"),
    ("BAJAJ FINANCE LTD", 3.17, "Finance - NBFC"),
    ("INFOSYS LTD", 2.98, "IT"),
    ("HINDUSTAN UNILEVER LTD", 2.80, "FMCG"),
    ("LARSEN & TOUBRO LTD", 2.61, "Construction/Engineering"),
    ("ITC LTD", 2.50, "FMCG"),
    ("MARUTI SUZUKI INDIA LTD", 2.38, "Automobile"),
    ("MAHINDRA & MAHINDRA LTD", 2.20, "Automobile"),
    ("KOTAK MAHINDRA BANK LTD", 2.03, "Banking"),
    ("HCL TECHNOLOGIES LTD", 2.03, "IT"),
    ("SUN PHARMACEUTICAL INDUSTRIES LTD", 1.98, "Pharma"),
    ("AXIS BANK LTD", 1.87, "Banking"),
    ("ULTRATECH CEMENT LTD", 1.72, "Cement"),
    ("TITAN COMPANY LTD", 1.64, "Consumer Durables"),
    ("BAJAJ FINSERV LTD", 1.61, "Finance"),
    ("NTPC LTD", 1.55, "Power"),
    ("OIL & NATURAL GAS CORPORATION LTD", 1.55, "Energy"),
    ("ADANI PORTS AND SEZ LTD", 1.52, "Infrastructure"),
    ("BHARAT ELECTRONICS LTD", 1.46, "Defence"),
    ("ZOMATO LTD", 1.44, "Services"),
    ("JSW STEEL LTD", 1.40, "Metals/Steel"),
    ("ADANI ENTERPRISES LTD", 1.31, "Conglomerate"),
    ("WIPRO LTD", 1.23, "IT"),
    ("POWER GRID CORPORATION OF INDIA LTD", 1.23, "Power"),
    ("ASIAN PAINTS LTD", 1.22, "Consumer Durables"),
    ("NESTLE INDIA LTD", 1.20, "FMCG"),
    ("BAJAJ AUTO LTD", 1.19, "Automobile"),
    ("COAL INDIA LTD", 1.13, "Mining"),
    ("TATA STEEL LTD", 1.08, "Metals/Steel"),
    ("INTERGLOBE AVIATION LTD", 1.08, "Aviation"),
    ("SBI LIFE INSURANCE COMPANY LTD", 0.97, "Insurance"),
    ("JIO FINANCIAL SERVICES LTD", 0.93, "Finance"),
    ("EICHER MOTORS LTD", 0.91, "Automobile"),
    ("GRASIM INDUSTRIES LTD", 0.90, "Diversified"),
    ("HINDALCO INDUSTRIES LTD", 0.87, "Metals/Aluminium"),
    ("TRENT LTD", 0.81, "Retail"),
    ("HDFC LIFE INSURANCE CO LTD", 0.78, "Insurance"),
    ("TATA MOTORS LTD", 0.73, "Automobile"),
    ("SHRIRAM FINANCE LTD", 0.73, "Finance - NBFC"),
    ("TECH MAHINDRA LTD", 0.68, "IT"),
    ("CIPLA LTD", 0.59, "Pharma"),
    ("TATA CONSUMER PRODUCTS LTD", 0.58, "FMCG"),
    ("APOLLO HOSPITALS ENTERPRISES LTD", 0.55, "Healthcare"),
    ("MAX HEALTHCARE INSTITUTE LTD", 0.54, "Healthcare"),
    ("DR REDDYS LABORATORIES LTD", 0.49, "Pharma"),
]

df = pd.DataFrame(data, columns=["Company", "Weight_pct", "Sector"])
df["Weight_frac"] = df["Weight_pct"] / 100

# -----------------------------
# 2️⃣ Nifty assumptions and formula
# -----------------------------
nifty_level = 25509.7
scenarios = [100, 200, 250, 500, -100, -200, -250, -500]

def required_stock_pct_change(points_change, nifty_level, weight_frac):
    """Return required % change in stock to move Nifty by given points."""
    index_pct_move = points_change / nifty_level
    return (index_pct_move / weight_frac) * 100 if weight_frac > 0 else 0

for pts in scenarios:
    df[f"Req_%_for_{pts}pts"] = df["Weight_frac"].apply(
        lambda w: required_stock_pct_change(pts, nifty_level, w)
    ).round(2)

# -----------------------------
# 3️⃣ Infosys case study
# -----------------------------
infosys = df[df["Company"].str.contains("INFOSYS")].iloc[0]
infosys_case = {
    "Company": infosys["Company"],
    "Weight_pct": infosys["Weight_pct"],
    "100pts": required_stock_pct_change(100, nifty_level, infosys["Weight_frac"]),
    "200pts": required_stock_pct_change(200, nifty_level, infosys["Weight_frac"]),
    "250pts": required_stock_pct_change(250, nifty_level, infosys["Weight_frac"]),
    "500pts": required_stock_pct_change(500, nifty_level, infosys["Weight_frac"]),
}

# -----------------------------
# 4️⃣ Create downloadable CSV instead of Excel
# -----------------------------
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

# -----------------------------
# 5️⃣ Streamlit Frontend
# -----------------------------
st.title("📊 NIFTY 50 Index Weightage & Impact Analysis")
st.write("Analyze how each stock affects overall Nifty 50 movement.")

st.subheader("NIFTY 50 Constituents by Sector")
st.dataframe(df[["Company", "Sector", "Weight_pct"]])

st.subheader("Required % Stock Change for Nifty Move (+100, +200, +250, +500)")
st.dataframe(
    df[["Company", "Weight_pct", "Req_%_for_100pts", "Req_%_for_200pts", "Req_%_for_250pts", "Req_%_for_500pts"]]
)

st.subheader("Infosys Case Study (Example)")
st.json(infosys_case)

st.download_button(
    label="⬇️ Download Nifty 50 Impact Data (CSV)",
    data=csv_data,
    file_name="nifty50_analysis.csv",
    mime="text/csv",
)

st.success("✅ Analysis complete! CSV file ready for download.")
