import streamlit as st
import pandas as pd
import joblib

# =============================
# LOAD MODELS
# =============================
model_storage = joblib.load("model_storage.pkl")
model_mhe = joblib.load("model_mhe.pkl")
model_unit = joblib.load("model_storage_unit.pkl")

# =============================
# STORAGE SIZE RULE
# =============================
storage_size = {
    "Bin Storage": 1.2 * 1.0,
    "Rack Storage": 2.5 * 1.2,
    "Pallet Storage": 1.2 * 1.2
}

# =============================
# STREAMLIT UI
# =============================
st.set_page_config(page_title="AI Warehouse Planner", layout="centered")

st.title("📦 AI Warehouse Planning System")
st.write("Masukkan dimensi dan jumlah barang untuk mendapatkan rekomendasi gudang.")

st.divider()

# =============================
# USER INPUT
# =============================
length = st.number_input("Panjang Barang (meter)", min_value=0.01, value=0.5)
width = st.number_input("Lebar Barang (meter)", min_value=0.01, value=0.4)
height = st.number_input("Tinggi Barang (meter)", min_value=0.01, value=0.3)
quantity = st.number_input("Jumlah Barang", min_value=1, value=100)

# =============================
# PREDICTION
# =============================
if st.button("🔍 Proses Perhitungan"):
    volume = length * width * height
    total_volume = volume * quantity

    input_df = pd.DataFrame([{
        "Length_m": length,
        "Width_m": width,
        "Height_m": height,
        "Quantity": quantity,
        "Total_Volume_m3": total_volume
    }])

    pred_storage = model_storage.predict(input_df)[0]
    pred_mhe = model_mhe.predict(input_df)[0]
    pred_unit = round(model_unit.predict(input_df)[0])

    warehouse_area = pred_unit * storage_size[pred_storage]

    # =============================
    # OUTPUT
    # =============================
    st.success("✅ Rekomendasi Berhasil Dihitung")

    st.subheader("📊 Hasil Rekomendasi")
    st.write(f"**Tipe Storage:** {pred_storage}")
    st.write(f"**Jumlah Unit Storage:** {pred_unit}")
    st.write(f"**Material Handling Equipment:** {pred_mhe}")
    st.write(f"**Estimasi Luasan Gudang:** {warehouse_area:.2f} m²")
