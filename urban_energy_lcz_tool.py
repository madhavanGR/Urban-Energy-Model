import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

st.set_page_config(page_title="Urban Energy & LCZ Evaluator", layout="wide")
st.title("🏙️ Urban Energy & Thermal Comfort Evaluator")
st.markdown("""
This tool is based on your PhD research. Enter **Urban Morphology Indicators (UMIs)** and select **LCZ type** to estimate 
cooling energy performance, visualize prototype impacts, and tweak designs interactively.
""")

# --- Load Pretrained Model (Mock Model for Demo) ---
def estimate_cooling_energy(umi):
    ar, svf, psf, far, gsi = umi
    score = 100 - (ar * 10 + (1 - svf) * 25 + psf * 15 + far * 5 + gsi * 10)
    return max(0, min(score, 100))

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Input Parameters")

aspect_ratio = st.sidebar.slider("Aspect Ratio (AR)", 0.5, 4.0, 1.5, 0.1)
svf = st.sidebar.slider("Sky View Factor (SVF)", 0.1, 1.0, 0.35, 0.05)
psf = st.sidebar.slider("Permeable Surface Fraction (PSF)", 0.0, 1.0, 0.45, 0.05)
far = st.sidebar.slider("Floor Area Ratio (FAR)", 0.5, 5.0, 2.5, 0.1)
gsi = st.sidebar.slider("Ground Space Index (GSI)", 0.1, 1.0, 0.6, 0.05)

lcz_type = st.sidebar.selectbox("Select LCZ Type", [
    "LCZ 1 - Compact High-Rise",
    "LCZ 2 - Compact Mid-Rise",
    "LCZ 3 - Compact Low-Rise",
    "LCZ 6 - Open Low-Rise",
    "LCZ 8 - Large Low-Rise",
    "LCZ B - Scattered Trees",
    "LCZ D - Low Plants"
])

st.sidebar.markdown("---")
visual_tweak = st.sidebar.checkbox("🔄 Enable Urban Prototype Tweaking")
if visual_tweak:
    building_density = st.sidebar.slider("Building Density (%)", 10, 100, 60, 5)
    vegetation_percent = st.sidebar.slider("Vegetation Cover (%)", 0, 100, 30, 5)
    height_variance = st.sidebar.slider("Building Height Std. Dev. (m)", 0, 20, 5)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Estimated Energy Performance")
    cooling_score = estimate_cooling_energy([aspect_ratio, svf, psf, far, gsi])
    st.metric("Estimated Cooling Efficiency Score", f"{cooling_score:.1f}/100")

    st.subheader("🌡️ Morphology-Based Impact")
    st.write("Higher aspect ratio and lower SVF generally improve shading and reduce cooling load.")
    fig, ax = plt.subplots()
    ax.bar(["AR", "SVF", "PSF", "FAR", "GSI"], [aspect_ratio, svf, psf, far, gsi], color='teal')
    ax.set_ylabel("Value")
    st.pyplot(fig)

with col2:
    st.subheader("🧱 Urban Prototype Visualizer")
    fig2, ax2 = plt.subplots(figsize=(4,4))
    if visual_tweak:
        ax2.set_title(f"{lcz_type}\nBD: {building_density}%, Veg: {vegetation_percent}%, Height SD: {height_variance}m")
        ax2.barh(["Buildings", "Vegetation"], [building_density, vegetation_percent], color=['gray', 'green'])
        ax2.set_xlim(0, 100)
    else:
        ax2.text(0.5, 0.5, 'Enable prototype tweak to visualize', ha='center', va='center')
        ax2.axis('off')
    st.pyplot(fig2)

st.markdown("---")
st.markdown("Built from the PhD research of **Dr. Madhavan G R** | LCZ & UMI powered urban design intelligence 🧠")
