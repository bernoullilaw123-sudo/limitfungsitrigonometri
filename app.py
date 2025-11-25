import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, limit, sin, cos, tan, log
from sympy.parsing.mathematica import parse_mathematica

# Menggunakan SymPy untuk perhitungan limit formal
x = symbols('x')

# --- Fungsi Evaluasi Limit ---
def evaluate_limit(function_str, a):
    """Mengevaluasi limit fungsi formal menggunakan SymPy."""
    
    # Ganti notasi khusus Streamlit/user menjadi notasi SymPy
    function_str = function_str.replace('^', '**')
    function_str = function_str.replace('ln', 'log')
    
    try:
        # Gunakan parse_mathematica untuk mengubah string ke ekspresi SymPy
        expr = parse_mathematica(function_str)
        
        # Hitung limit
        L = limit(expr, x, a)
        return str(L)
    except Exception as e:
        return f"Error: {e}"

# --- Fungsi Plotting ---
def plot_function(function_str, a, delta):
    """Membuat plot interaktif fungsi di sekitar titik limit."""
    
    # Persiapkan domain x
    # Membuat rentang yang sangat dekat dengan 'a'
    x_left = np.linspace(a - delta, a - 1e-9, 500)
    x_right = np.linspace(a + 1e-9, a + delta, 500)
    x_range = np.concatenate([x_left, x_right])

    try:
        # Konversi string fungsi ke fungsi Python yang dapat dievaluasi oleh NumPy
        # Mengganti 'sin(x)' menjadi 'np.sin(x)', dst.
        f_expr = function_str.replace('^', '**')
        f_expr = f_expr.replace('sin', 'np.sin')
        f_expr = f_expr.replace('cos', 'np.cos')
        f_expr = f_expr.replace('tan', 'np.tan')
        f_expr = f_expr.replace('ln', 'np.log') # Perhatikan: np.log adalah ln
        
        # Evaluasi fungsi pada domain
        y_range = eval(f_expr.replace('x', 'x_range'))
        
        # Ambil nilai limit formal untuk anotasi
        limit_val_str = evaluate_limit(function_str, a)
        limit_val = float(limit_val_str)
        
        # Inisialisasi Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot Fungsi
        ax.plot(x_range, y_range, label=f"$f(x) = {function_str}$", color='blue', alpha=0.7)
        
        # Titik Limit (Hole/Nilai Limit)
        ax.plot(a, limit_val, 'ro', markersize=8, label=f"Limit $L = {limit_val:.4f}$")
        ax.hlines(limit_val, a - delta, a + delta, color='red', linestyle='--', linewidth=1, alpha=0.6, label='Garis y = L')
        ax.vlines(a, ax.get_ylim()[0], ax.get_ylim()[1], color='gray', linestyle=':', linewidth=1)
        
        # Area Visualisasi Delta
        ax.axvspan(a - delta, a + delta, alpha=0.1, color='green', label=f"Rentang $\\delta$ (x-axis)")
        
        # Keterangan dan Estetika
        ax.set_title(f"Visualisasi Limit Fungsi di sekitar x = {a}", fontsize=16)
        ax.set_xlabel("x", fontsize=12)
        ax.set_ylabel("f(x)", fontsize=12)
        ax.set_xlim(a - delta, a + delta)
        
        # Atur batas Y agar tidak terlalu ekstrim
        y_min = np.nanpercentile(y_range, 1)
        y_max = np.nanpercentile(y_range, 99)
        ax.set_ylim(y_min - 0.5, y_max + 0.5)
        
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        
        return fig
        
    except Exception as e:
        st.error(f"Terjadi kesalahan saat mengevaluasi atau plotting fungsi: {e}. Pastikan Anda menggunakan notasi Python yang benar (misalnya `x` sebagai variabel, `**` untuk pangkat).")
        return None

# --- Fungsi Utama Streamlit ---
def main():
    st.set_page_config(
        page_title="Virtual Lab Limit Fungsi Trigonometri",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🧪 Virtual Lab Limit Fungsi Trigonometri")
    st.markdown("Eksplorasi perilaku grafik fungsi trigonometri saat mendekati suatu titik.")

    st.sidebar.header("⚙️ Input Fungsi & Titik Limit")
    
    # 1. Input Fungsi
    st.sidebar.markdown("**Contoh Fungsi:** `sin(x)/x`, `(1-cos(x))/x`, `tan(2*x)/(x*cos(x))`")
    function_str = st.sidebar.text_input(
        "Masukkan $f(x)$ (Gunakan `**` untuk pangkat, `ln` untuk $\\log_e$)",
        value="sin(x)/x"
    )
    
    # 2. Input Titik Limit
    a = st.sidebar.number_input(
        "Titik Limit ($a$): $x \\to a$",
        value=0.0,
        step=0.1
    )
    
    # 3. Rentang Visualisasi (Delta)
    delta = st.sidebar.slider(
        "Rentang Visualisasi ($\\delta$)",
        min_value=0.01,
        max_value=2.0,
        value=0.5,
        step=0.01,
        help="Semakin kecil delta, semakin dekat Anda melihat titik limit."
    )
    
    st.header("🎯 Hasil Limit Formal (SymPy)")
    
    # Hitung dan Tampilkan Limit Formal
    limit_result = evaluate_limit(function_str, a)
    st.code(f"$$\\lim_{{x \\to {a}}} {function_str} = {limit_result}$$")
    
    if "Error" not in limit_result:
        st.success(f"Nilai limit formal adalah: **{limit_result}**")
    
    
    st.header("📈 Visualisasi Interaktif")
    
    # Tampilkan Plot
    fig = plot_function(function_str, a, delta)
    if fig:
        st.pyplot(fig)
        
        # Panduan untuk Siswa
        st.markdown("""
        ### 💡 Panduan Eksplorasi:
        1.  **Coba ubah $\\delta$**: Amati bagaimana grafik 'mengecil' di sekitar titik $x=a$ saat Anda mengurangi $\\delta$.
        2.  **Cek Kesinambungan**: Perhatikan apakah grafik 'melewati' titik merah. Jika fungsinya tidak terdefinisi di $x=a$ (misalnya pembagian nol), akan ada 'lubang' (hole) di titik tersebut, namun limitnya tetap ada.
        3.  **Ganti Fungsi**: Eksplorasi fungsi-fungsi dasar seperti $\\frac{\\sin x}{x}$ (limit $\to 1$ saat $x\\to 0$) atau $\\frac{1-\\cos x}{x}$ (limit $\to 0$ saat $x\\to 0$).
        """)

if __name__ == "__main__":
    main()
