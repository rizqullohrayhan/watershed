import streamlit as st
from process_watershed import process_watershed

st.write("Aplikasi Deteksi Sel")
st.write("Silahkan unggah gambar sel untuk dideteksi.")
uploaded_file = st.file_uploader("Pilih gambar sel", type=["jpg", "jpeg", "png", "bmp", "tiff", "tif", "dib"])

st.sidebar.header("Parameter Watershed")
channel_option = st.sidebar.selectbox("Pilih Saluran Warna:", ("Grayscale", "Hijau", "Biru", "Merah"))
thresh_val = st.sidebar.slider("Sensitivitas Threshold", 0, 255, 127)
dist_val = st.sidebar.slider("Pemisahan Objek (Distance Transform)", 0.1, 1.0, 0.5)

if st.button("Proses Deteksi"):
    if uploaded_file is not None:
        # Simpan file sementara
        with open("temp_image.png", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        result, map_markers, total_sel = process_watershed("temp_image.png", dist_val)
        
        st.write(f"Jumlah sel terdeteksi: {total_sel}")
        st.image(result, caption="Hasil Deteksi Sel", use_column_width=True)
    else:
        st.warning("Silahkan unggah gambar terlebih dahulu.")
