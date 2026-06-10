import streamlit as st
import requests
import pandas as pd
import os
import plotly.express as px
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu


# =====================================
# BACKEND API URL
# =====================================
BASE_URL = "https://backend-skripsi-gempa-154904818236.asia-southeast1.run.app"

# ==============================
# SESSION LOGIN
# ==============================

if "login" not in st.session_state:
    st.session_state.login = False

# ==============================
# CONFIG
# ==============================

st.set_page_config(
    page_title="Prediksi Gempa Tektonik",
    layout="wide"
)

# ==============================
# STYLE - BLUE THEME
# ==============================

st.markdown("""
<style>

/* Background utama */
.stApp {
    background: linear-gradient(135deg, #EFF6FF 0%, #F8FAFC 100%);
}

/* Container utama */
.block-container {
    padding-top: 4rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E3A8A 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Card */
.custom-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(30, 58, 138, 0.08);
    border: 1px solid #DBEAFE;
    margin-bottom: 20px;
}

/* Judul utama */
.title {
    font-size: 42px;
    font-weight: 800;
    color: #1D4ED8;
    margin-bottom: 10px;
}

/* Subjudul */
.subtitle {
    font-size: 18px;
    color: #475569;
    margin-bottom: 20px;
}

/* Tombol */
.stButton > button {
    background: linear-gradient(90deg, #2563EB, #1D4ED8);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1.4rem;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1D4ED8, #1E40AF);
}

/* Input */
.stTextInput input,
.stNumberInput input {
    border-radius: 10px;
}

/* Metric card */
[data-testid="metric-container"] {
    background: white;
    border: 1px solid #DBEAFE;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.06);
}

/* Success box */
.stSuccess {
    border-radius: 12px;
}

/* Error box */
.stError {
    border-radius: 12px;
}

/* Info box */
.stInfo {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HALAMAN LOGIN MODERN
# Letakkan kode ini di frontend/app.py
# GANTI seluruh blok:
# if not st.session_state.login:
#     ...
#     st.stop()
# ==========================================

if not st.session_state.login:

    import base64
    from pathlib import Path

    # ======================================
    # CSS KHUSUS LOGIN PAGE
    # ======================================
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    .stApp {
        background:
            radial-gradient(circle at top right, rgba(59,130,246,0.15), transparent 40%),
            radial-gradient(circle at bottom left, rgba(16,185,129,0.12), transparent 35%),
            linear-gradient(135deg, #EAF4FF 0%, #F7FBFF 100%);
    }

    .login-card {
        max-width: 850px;
        margin: 30px auto 40px auto;
        background: rgba(255,255,255,0.94);
        border-radius: 32px;
        padding: 60px;
        box-shadow: 0 25px 70px rgba(37,99,235,0.12);
        border: 1px solid rgba(255,255,255,0.8);
        backdrop-filter: blur(12px);
    }

    .hero-title {
        text-align: center;
        font-size: 54px;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 20px;
        color: #1D4ED8;
    }

    .hero-subtitle {
        text-align: center;
        font-size: 18px;
        line-height: 1.9;
        color: #64748B;
        max-width: 650px;
        margin: 0 auto 25px auto;
    }

    .hero-badge {
        background: linear-gradient(90deg, #ECFDF5, #D1FAE5);
        border: 1px solid #A7F3D0;
        color: #047857;
        padding: 14px 18px;
        border-radius: 14px;
        font-size: 15px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 30px;
    }

    .stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 30px;
    }

    .stat-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
    }

    .stat-value {
        font-size: 28px;
        font-weight: 800;
        color: #1D4ED8;
        margin-bottom: 5px;
    }

    .stat-label {
        font-size: 13px;
        color: #64748B;
        font-weight: 600;
    }

    .login-title {
        text-align: center;
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ======================================
    # OPTIONAL LOGO
    # ======================================
    logo_html = "🌍"

    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        logo_html = f"""
        <img src="data:image/png;base64,{encoded}"
             style="width:110px;height:110px;object-fit:contain;">
        """

    # GANTI SELURUH BLOK HERO LOGIN LAMA DENGAN KODE INI

    # GANTI SELURUH BLOK HERO LOGIN DENGAN KODE INI
    # (jangan letakkan HTML mentah di file Python)

    # ==========================================================
    # SOLUSI FINAL AGAR HTML TIDAK MUNCUL SEBAGAI TEKS
    # GANTI BLOK hero_html DAN st.markdown(hero_html, ...)
    # DENGAN KODE DI BAWAH INI
    # ==========================================================

    # Login Card dibuka
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    # Logo
    st.markdown(
        f'''
        <div style="text-align:center; margin-bottom:20px;">
            {logo_html}
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Judul
    st.markdown(
        '''
        <div class="hero-title">
            Sistem Prediksi Gempa Tektonik
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Subtitle
    st.markdown(
        '''
        <div class="hero-subtitle">
            Dashboard cerdas berbasis
            <b>Machine Learning</b> dan
            <b>Recurrent Neural Network (RNN)</b>
            untuk Memprediksi Magnitudo dan Risiko Gempa Bumi.
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Badge
    st.markdown(
        '''
        <div class="hero-badge">
            Sistem aktif dan siap digunakan
        </div>
        ''',
        unsafe_allow_html=True
    )
    

    # Judul login
    st.markdown(
        '''
        <div class="login-title">
            Login ke Sistem
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Form login di dalam card
    left, center, right = st.columns([1, 2, 1])
    
    with center:
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")

        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "123":
                st.session_state.login = True
                st.session_state.username = "admin"
                st.session_state.role = "admin"
                st.rerun()

            elif username == "user" and password == "123":
                st.session_state.login = True
                st.session_state.username = "user"
                st.session_state.role = "user"
                st.rerun()

            else:
                st.error("❌ Username atau password salah.")

    # Tutup login card
    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ==============================
# SIDEBAR MODERN (TANPA HTML AGAR TIDAK MUNCUL KOTAK PUTIH)
# ==============================

role = st.session_state.get("role", "user")
username = st.session_state.get("username", "Guest")

with st.sidebar:
    # Spasi atas
    st.markdown("<br>", unsafe_allow_html=True)

    # Judul Sidebar
    st.markdown("""
    <h1 style="
        color: white;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 25px;
        line-height: 1.2;
    ">
    </h1>
    """, unsafe_allow_html=True)

    # Card informasi user menggunakan komponen native Streamlit
    with st.container():
        st.markdown("""
        <div style="
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 25px;
        ">
        """, unsafe_allow_html=True)

        st.caption("👤 Login sebagai")
        st.markdown(
            f"<h3 style='color:white; margin:0;'>{username}</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <span style="
                display:inline-block;
                margin-top:8px;
                background: rgba(255,255,255,0.12);
                color:#D1FAE5;
                padding:4px 12px;
                border-radius:999px;
                font-size:12px;
                font-weight:600;
            ">
                {role.upper()}
            </span>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tombol Logout
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
        
    # Menu Admin
if role == "admin":
    menu_options = [
        "Dashboard",
        "Prediksi Gempa",
        "Prediksi Magnitudo RNN",
        "Riwayat Prediksi",
        "Visualisasi Data",
        "Evaluasi Model",
        "Grafik Training RNN",
        "BMKG Real-time",
    ]
else:
    menu_options = [
        "Prediksi Gempa",
        "Prediksi Magnitudo RNN",
        "BMKG Real-time",
    ]

menu = option_menu(
    menu_title=None,
    options=menu_options,
    icons=[
        "house",
        "search",
        "cpu",
        "clock-history",
        "bar-chart",
        "clipboard-data",
        "graph-up",
        "globe"
    ][:len(menu_options)],
    orientation="horizontal",
    default_index=0
)

# ==============================
# DASHBOARD MODERN
# ==============================

if menu == "Dashboard":
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 50%, #38BDF8 100%);
            padding: 40px;
            border-radius: 24px;
            color: white;
            box-shadow: 0 20px 50px rgba(37, 99, 235, 0.25);
            margin-bottom: 30px;
        ">
            <div style="display:flex; align-items:center; gap:20px;">
                <div style="
                    font-size: 58px;
                    background: rgba(255,255,255,0.15);
                    width: 90px;
                    height: 90px;
                    border-radius: 24px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                ">
                    🌍
                </div>
                <div>
                    <h1 style="
                        margin:0;
                        font-size:38px;
                        font-weight:800;
                        line-height:1.2;
                        color:white;
                    ">
                        Dashboard Prediksi Gempa Tektonik
                    </h1>
                    <p style="
                        margin:10px 0 0 0;
                        font-size:17px;
                        color: rgba(255,255,255,0.88);
                    ">
                        Sistem prediksi dan monitoring gempa bumi berbasis
                        <b>Machine Learning</b> dan
                        <b>Recurrent Neural Network (RNN)</b>.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ==============================
    # LOAD DATASET BMKG
    # ==============================
    from pathlib import Path

    # Path absolut ke file CSV
    BASE_DIR = Path(__file__).resolve().parent
    csv_path = BASE_DIR.parent / "data" / "gempa_2019_2024_bersih.csv"

    # Optional: cek path
    # st.write("CSV Path:", csv_path)

    df_dataset = pd.read_csv(csv_path)
    total_data = len(df_dataset)

    # Ambil akurasi model dari hasil evaluasi
    accuracy = 0.9324   # sesuaikan dengan hasil evaluasi model Anda

    # Jumlah prediksi hari ini (sementara contoh)
    prediksi_hari_ini = 23

    # ==============================
    # METRICS DASHBOARD
    # ==============================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Data Gempa",
            f"{total_data:,}".replace(",", ".")
        )

    with col2:
        st.metric(
            "Akurasi Model",
            f"{accuracy*100:.2f}%"
        )

    with col3:
        st.metric(
            "Prediksi Hari Ini",
            str(prediksi_hari_ini)
        )

    with col4:
        st.metric(
            "Status Sistem",
            "Aktif"
        )

    # STATUS
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #ECFDF5, #D1FAE5);
        border-left: 6px solid #10B981;
        padding: 20px 24px;
        border-radius: 16px;
        font-size: 16px;
        color: #065F46;
        font-weight: 600;
        margin-bottom: 30px;
    ">
        ✅ Sistem berhasil berjalan dengan baik dan siap digunakan.
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================
    # FITUR UTAMA SISTEM (100% AMAN - TANPA HTML COMPLEX)
    # ==========================================================
    col_left, col_right = st.columns([2.5, 1])

    # =========================
    # CARD KIRI
    # =========================
    with col_left:
        st.markdown("""
        <div style="
            background: white;
            padding: 30px;
            border-radius: 24px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        ">
            <h2 style="
                color: #1D4ED8;
                margin: 0 0 20px 0;
                font-size: 34px;
                font-weight: 800;
            ">
                Fitur Utama Sistem
            </h2>
        </div>
        """, unsafe_allow_html=True)

        # Gunakan Streamlit native agar tidak muncul kode HTML
        st.markdown("""
        - Prediksi risiko gempa bumi
        - Prediksi magnitudo gempa berikutnya
        - Visualisasi data dan evaluasi model
        - Monitoring gempa terbaru BMKG
        - Ekspor riwayat prediksi ke CSV
        """)

    # GANTI bagian card kanan menjadi seperti ini
    with col_right:
        # Card biru
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1D4ED8, #2563EB);
            padding: 35px 25px;
            border-radius: 24px;
            box-shadow: 0 15px 35px rgba(37,99,235,0.30);
            text-align: center;
            min-height: 280px;
            color: white;
        ">
            <div style="font-size: 64px; margin-bottom: 20px;">🌍</div>
            <h3 style="
                margin: 0;
                font-size: 28px;
                font-weight: 800;
                color: white;
            ">
                Earthquake AI
            </h3>
            <p style="
                margin-top: 12px;
                font-size: 15px;
                line-height: 1.9;
                color: rgba(255,255,255,0.92);
            ">
                Sistem cerdas berbasis Machine Learning dan RNN
                untuk memprediksi magnitudo dan risiko gempa bumi.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==============================
# MENU PREDIKSI GEMPA
# ==============================

if menu == "Prediksi Gempa":

    st.markdown(
        '<p class="title">Prediksi Gempa</p>',
        unsafe_allow_html=True
    )

    st.subheader("Input Data Gempa")

    col1, col2 = st.columns(2)

    with col1:
        magnitudo = st.slider(
            "Magnitudo",
            0.0,
            10.0,
            5.0,
            0.1
        )

        depth = st.slider(
            "Kedalaman (km)",
            0.0,
            700.0,
            10.0,
            1.0
        )

    with col2:
        lat = st.number_input(
            "Latitude",
            value=-6.2
        )

        lon = st.number_input(
            "Longitude",
            value=106.8
        )

    # ==============================
    # BUTTON PREDIKSI
    # ==============================

    if st.button("Prediksi Sekarang"):

        payload = {
            "magnitudo": magnitudo,
            "depth": depth,
            "lat": lat,
            "lon": lon
        }

        try:

            # ==============================
            # REQUEST PREDIKSI RISIKO
            # ==============================
            risk_response = requests.post(
                "https://skripsi-gempa-production.up.railway.app/api/predict",
                json=payload,
                timeout=30
            )

            # ==============================
            # REQUEST PREDIKSI MAGNITUDE
            # ==============================
            magnitude_response = requests.post(
                "https://skripsi-gempa-production.up.railway.app/api/predict-magnitude",
                json={
                    "depth": depth,
                    "lat": lat,
                    "lon": lon
                },
                timeout=30
            )

            # ==============================
            # VALIDASI RESPONSE
            # ==============================
            if (
                risk_response.status_code == 200
                and magnitude_response.status_code == 200
            ):

                result = risk_response.json()
                magnitude_result = magnitude_response.json()

                prediction = result["prediction"]
                probability = result["probability"]
                predicted_magnitude = magnitude_result[
                    "predicted_magnitude"
                ]
                # Rule-based adjustment
                if magnitudo >= 7.0:
                    prediction = 1
                    probability = max(probability, 0.95)

                st.success("✅ Prediksi berhasil dilakukan!")

                st.divider()
                st.subheader("Hasil Prediksi")

                # ==============================
                # STATUS RISIKO
                # ==============================
                if prediction == 1:
                    st.error("🔴 Risiko Gempa Tinggi")

                    if probability > 0.8:
                        st.warning(
                            "⚠️ Potensi Gempa Sangat Tinggi!"
                        )
                else:
                    st.success("🟢 Risiko Gempa Rendah")

                # ==============================
                # METRICS
                # ==============================
                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric(
                        label="Status Prediksi",
                        value=prediction
                    )

                with c2:
                    st.metric(
                        label="Probabilitas",
                        value=f"{probability:.2f}"
                    )

                with c3:
                    st.metric(
                        label="Predicted Magnitude",
                        value=f"{predicted_magnitude:.2f} Mw"
                    )


            else:
                st.error("❌ Backend gagal memproses prediksi")

                if risk_response.status_code != 200:
                    st.write("Risk API Error:")
                    st.code(risk_response.text)

                if magnitude_response.status_code != 200:
                    st.write("Magnitude API Error:")
                    st.code(magnitude_response.text)

        except Exception as e:
            st.error(f"❌ Gagal connect ke backend: {e}")

# ==============================
# MENU HISTORY
# ==============================

if menu == "Riwayat Prediksi":

    st.markdown(
        '<p class="title">📋 Riwayat Prediksi</p>',
        unsafe_allow_html=True
    )

    try:

        history_response = requests.get(
            "https://skripsi-gempa-production.up.railway.app/api/history"
        )

        if history_response.status_code == 200:

            history_data = history_response.json()

            if len(history_data) > 0:

                df = pd.DataFrame(history_data)

                st.dataframe(
                    df,
                    use_container_width=True
                )

                # ==============================
                # DOWNLOAD EXCEL
                # ==============================

                csv = df.to_csv(index=False)

                st.download_button(
                    label="📥 Download History CSV",
                    data=csv,
                    file_name="history_prediksi.csv",
                    mime="text/csv"
                )

            else:
                st.info("Belum ada data prediksi")

        else:
            st.error("❌ Gagal mengambil data history")

    except Exception as e:
        st.error(f"❌ Gagal load history: {e}")

# ==============================
# MENU VISUALISASI
# ==============================

if menu == "Visualisasi Data":

    st.markdown(
        '<p class="title">Visualisasi Data Gempa</p>',
        unsafe_allow_html=True
    )

    try:
        history_response = requests.get(
            "https://skripsi-gempa-production.up.railway.app/api/history",
            timeout=30
        )

        if history_response.status_code == 200:

            history_data = history_response.json()

            if len(history_data) > 0:

                df = pd.DataFrame(history_data)

                # ==============================
                # PIE CHART
                # ==============================
                risk_count = df["prediction"].value_counts().reset_index()
                risk_count.columns = ["prediction", "total"]

                risk_count["prediction"] = risk_count["prediction"].replace({
                    0: "Risiko Rendah",
                    1: "Risiko Tinggi"
                })

                fig_pie = px.pie(
                    risk_count,
                    names="prediction",
                    values="total",
                    title="Distribusi Risiko Gempa"
                )

                st.plotly_chart(
                    fig_pie,
                    use_container_width=True
                )

                # ==============================
                # BAR CHART
                # ==============================
                fig_bar = px.bar(
                    df,
                    x="created_at",
                    y="probability",
                    title="Probabilitas Prediksi Gempa"
                )

                st.plotly_chart(
                    fig_bar,
                    use_container_width=True
                )

                # ==============================
                # PETA LOKASI GEMPA
                # ==============================
                st.subheader("🗺️ Peta Lokasi Gempa")

                if "lat" in df.columns and "lon" in df.columns:

                    map_df = df[["lat", "lon"]].copy()
                    map_df = map_df.dropna()

                    if not map_df.empty:
                        map_df["lat"] = map_df["lat"].astype(float)
                        map_df["lon"] = map_df["lon"].astype(float)

                        map_df = map_df.rename(columns={
                            "lat": "latitude",
                            "lon": "longitude"
                        })

                        st.map(map_df, zoom=5)

                    else:
                        st.warning("⚠️ Data koordinat kosong.")

                else:
                    st.warning("⚠️ Kolom lat dan lon tidak ditemukan.")

            else:
                st.info("Belum ada data prediksi.")

        else:
            st.error("❌ Gagal mengambil data history.")

    except Exception as e:
        st.error(f"❌ Gagal load visualisasi: {e}")



# =====================================
# EVALUASI MODEL
# =====================================

if menu == "Evaluasi Model":

    st.markdown(
        '<p class="title">📈 Evaluasi Model </p>',
        unsafe_allow_html=True
    )

    try:
        response = requests.get(
            f"{BASE_URL}/evaluation",
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()

            # Metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Accuracy", f"{result['accuracy']:.4f}")

            with col2:
                st.metric("Precision", f"{result['precision']:.4f}")

            with col3:
                st.metric("Recall", f"{result['recall']:.4f}")

            with col4:
                st.metric("F1 Score", f"{result['f1_score']:.4f}")

            st.divider()

            # Confusion Matrix
            st.subheader("Confusion Matrix")

            cm = pd.DataFrame(
                result["confusion_matrix"],
                index=["Aktual 0", "Aktual 1"],
                columns=["Prediksi 0", "Prediksi 1"]
            )

            st.dataframe(cm, use_container_width=True)

            # Interpretasi
            st.info("""
### Interpretasi Hasil
- Accuracy menunjukkan akurasi keseluruhan model.
- Precision menunjukkan ketepatan prediksi gempa berisiko tinggi.
- Recall menunjukkan kemampuan model mendeteksi gempa berisiko tinggi.
- F1 Score merupakan kombinasi precision dan recall.
""")

        else:
            st.error("Gagal mengambil data evaluasi model.")
            st.code(response.text)

    except Exception as e:
        st.error(f"Error: {e}")

# =====================================
# MENU PREDIKSI MAGNITUDO RNN
# =====================================

if menu == "Prediksi Magnitudo RNN":

    st.markdown(
        '<p class="title">Prediksi Magnitudo RNN</p>',
        unsafe_allow_html=True
    )

    st.write(
        "Masukkan 10 magnitudo terakhir untuk memprediksi magnitudo berikutnya."
    )

    # Input 10 nilai magnitudo
    cols = st.columns(5)
    values = []

    default_values = [
        4.5, 4.6, 4.7, 4.8, 4.9,
        5.0, 4.8, 4.7, 4.9, 5.1
    ]

    for i in range(10):
        with cols[i % 5]:
            val = st.number_input(
                f"M{i+1}",
                min_value=0.0,
                max_value=10.0,
                value=default_values[i],
                step=0.1,
                key=f"mag_{i}"
            )
            values.append(val)

    if st.button(
        "Prediksi Magnitudo Berikutnya",
        use_container_width=True
    ):
        try:
            payload = {
                "sequence": values
            }

            response = requests.post(
                f"{BASE_URL}/predict-rnn",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()
                pred = result["predicted_magnitude"]

                st.success(
                    f"Prediksi Magnitudo Berikutnya: {pred:.2f} Mw"
                )

                # Data grafik
                chart_data = pd.DataFrame({
                    "Step": [f"M{i+1}" for i in range(10)] + ["Prediksi"],
                    "Magnitude": values + [pred]
                })

                import plotly.express as px

                fig = px.line(
                    chart_data,
                    x="Step",
                    y="Magnitude",
                    markers=True,
                    title="Grafik Prediksi Magnitudo RNN"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.dataframe(
                    chart_data,
                    use_container_width=True
                )

            else:
                st.error(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

# =====================================
# GRAFIK TRAINING RNN
# =====================================

if menu == "Grafik Training RNN":

    st.markdown(
        '<p class="title">📉 Grafik Training RNN</p>',
        unsafe_allow_html=True
    )

    history_path = "backend/models/rnn_history.csv"

    if os.path.exists(history_path):

        history_df = pd.read_csv(history_path)

        st.subheader("Data History Training")
        st.dataframe(
            history_df,
            use_container_width=True
        )

        # Grafik loss
        fig = px.line(
            history_df,
            y=["loss", "val_loss"],
            title="Training Loss vs Validation Loss"
        )

        fig.update_layout(
            xaxis_title="Epoch",
            yaxis_title="Loss"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Metrics
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Final Training Loss",
                f"{history_df['loss'].iloc[-1]:.6f}"
            )

        with col2:
            st.metric(
                "Final Validation Loss",
                f"{history_df['val_loss'].iloc[-1]:.6f}"
            )

    else:
        st.error(
            "File backend/models/rnn_history.csv tidak ditemukan."
        )

# =====================================
# BMKG REAL-TIME
# =====================================

if menu == "BMKG Real-time":

    st.markdown(
        '<p class="title">Gempa Terbaru BMKG</p>',
        unsafe_allow_html=True
    )

    # ==========================================
    # UPLOAD DATASET CSV BMKG
    # ==========================================
    uploaded_file = st.file_uploader(
        "📂 Upload Dataset BMKG (CSV)",
        type=["csv"]
    )

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)

            st.success("✅ Dataset berhasil diupload.")
            st.dataframe(df_upload.head(), use_container_width=True)

            # Cek kolom koordinat
            if "Latitude" in df_upload.columns and "Longitude" in df_upload.columns:
                map_df = df_upload[["Latitude", "Longitude"]].dropna().copy()
                map_df.columns = ["lat", "lon"]

                if not map_df.empty:
                    st.subheader("Peta Dataset BMKG")
                    st.map(map_df)
                else:
                    st.warning("Data koordinat kosong.")
            else:
                st.warning("Kolom Latitude dan Longitude tidak ditemukan.")

        except Exception as e:
            st.error(f"Gagal membaca dataset: {e}")

    st.divider()

    # ==========================================
    # API BMKG REALTIME
    # ==========================================
    BMKG_URL = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"

    try:
        response = requests.get(BMKG_URL, timeout=20)

        if response.status_code == 200:

            data = response.json()
            gempa = data["Infogempa"]["gempa"]

            st.subheader("Detail Gempa")

            st.write(f"**Tanggal:** {gempa['Tanggal']}")
            st.write(f"**Jam:** {gempa['Jam']}")
            st.write(f"**Wilayah:** {gempa['Wilayah']}")
            st.write(f"**Koordinat:** {gempa['Coordinates']}")
            st.write(f"**Magnitude:** {gempa['Magnitude']}")
            st.write(f"**Kedalaman:** {gempa['Kedalaman']}")
            st.write(f"**Dirasakan:** {gempa.get('Dirasakan', '-')}")

            # Parse koordinat
            coords = gempa["Coordinates"].split(",")

            lat = float(coords[0].strip())
            lon = float(coords[1].strip())

            # Peta
            st.subheader("Lokasi Gempa Real-time")

            map_df = pd.DataFrame({
                "lat": [lat],
                "lon": [lon]
            })

            st.map(map_df, zoom=5)

        else:
            st.error(
                f"Gagal mengambil data BMKG. Status: {response.status_code}"
            )

    except Exception as e:
        st.error(f"Error BMKG: {e}")
