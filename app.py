import requests
import cv2
import numpy as np
import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os
import random

# =============================
# Streamlit UI
# =============================
st.title("🌾 Smart Agri Advisory System (AI + Weather + Drone)")
st.write("Upload your crop image to get weather, crop health & smart advisory 🌦️🌱")

CITY = st.text_input("🏙️ Enter City", "Chennai")
uploaded_file = st.file_uploader("📸 Upload Crop Image", type=["jpg", "png", "jpeg"])

API_KEY = "2c4546056e6ee1e18faae93923ea93e3"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

if st.button("🚀 Generate Smart Report"):
    # =============================
    # 1️⃣ WEATHER FORECAST (API)
    # =============================
    try:
        response = requests.get(URL)
        data = response.json()

        temp = data["list"][0]["main"]["temp"]
        humidity = data["list"][0]["main"]["humidity"]
        wind = data["list"][0]["wind"]["speed"]
        rain_forecast = any("rain" in entry["weather"][0]["main"].lower() for entry in data["list"][:5])
    except Exception as e:
        st.error(f"Weather API Error: {e}")
        temp, humidity, wind, rain_forecast = 30, 60, 3, False

    # =============================
    # 2️⃣ DRONE CROP ANALYSIS (Image)
    # =============================
    green_percentage = 0
    if uploaded_file is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_file.write(uploaded_file.read())
        temp_file.close()

        image = cv2.imread(temp_file.name)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Detect green area (healthy crop)
        green_mask = cv2.inRange(hsv, (36, 25, 25), (86, 255, 255))
        green_percentage = (cv2.countNonZero(green_mask) / (image.shape[0] * image.shape[1])) * 100

        st.image(image, caption=f"🧠 Crop Analysis: {green_percentage:.2f}% Green", channels="BGR")
        os.remove(temp_file.name)
    else:
        st.warning("⚠️ No image uploaded. Assuming 50% healthy crop.")
        green_percentage = 50

    # Calculate stressed vs healthy
    healthy_crop = round(green_percentage, 1)
    stressed_crop = round(100 - green_percentage, 1)

    # =============================
    # 3️⃣ DYNAMIC WEATHER ADJUSTMENT
    # =============================
    if healthy_crop < 40:
        temp += random.uniform(1, 2.5)
        humidity -= random.uniform(5, 10)
        wind += random.uniform(1, 2)
    elif 40 <= healthy_crop < 70:
        temp += random.uniform(-0.5, 1)
        humidity += random.uniform(-2, 3)
    else:
        temp += random.uniform(-1.5, 0.5)
        humidity += random.uniform(3, 6)

    temp = round(temp, 1)
    humidity = round(humidity, 1)
    wind = round(wind, 1)

    # =============================
    # 4️⃣ SMART ADVISORY LOGIC
    # =============================
    if healthy_crop < 40:
        recommendation = "🚨 Severe crop stress detected. Immediate irrigation & nutrient check needed."
    elif 40 <= healthy_crop < 70 and rain_forecast:
        recommendation = "🌧️ Rain expected soon, but crop moderate. Apply mild nutrients and wait for rain."
    elif 40 <= healthy_crop < 70 and not rain_forecast:
        recommendation = "💧 Moderate stress. Irrigate soon & monitor greenness with next image upload."
    elif healthy_crop >= 70 and rain_forecast:
        recommendation = "✅ Crops are healthy. Delay irrigation and let natural rain support growth."
    else:
        recommendation = "🌱 Excellent condition. Maintain routine irrigation & pest monitoring."

    # =============================
    # 5️⃣ DISPLAY HEALTH METRICS
    # =============================
    st.subheader("🌿 Crop Health Summary")
    st.progress(int(healthy_crop))
    st.write(f"🟢 **Healthy Crop:** {healthy_crop}%")
    st.progress(int(stressed_crop))
    st.write(f"🔴 **Stressed Crop:** {stressed_crop}%")

    # =============================
    # 6️⃣ OUTPUT REPORT
    # =============================
    output = f"""
📍 Region: {CITY}, Tamil Nadu
📅 Date: {datetime.now().strftime('%d-%m-%Y')}

--- 🌦️ Weather Forecast (AI-Adjusted) ---
Rain Forecast: {"High (Expected Soon)" if rain_forecast else "Low"}
Temperature: {temp}°C
Humidity: {humidity}%
Wind Speed: {wind} km/h

--- 🌿 Drone-Based Crop Analysis ---
Healthy Crop: {healthy_crop}%
Stressed Crop: {stressed_crop}%

--- 🧩 Sustainable Advisory ---
{recommendation}
"""

    st.text_area("📋 Smart Advisory Report", output, height=300)

    # =============================
    # 7️⃣ SAVE FILES
    # =============================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_filename = f"AgriSmart_Report_{timestamp}.txt"
    pdf_filename = f"AgriSmart_Report_{timestamp}.pdf"

    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(output)

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    text_obj = c.beginText(50, 750)
    for line in output.split("\n"):
        text_obj.textLine(line)
    c.drawText(text_obj)
    c.save()

    st.success("✅ AI-Enhanced Report Generated Successfully!")

    with open(txt_filename, "rb") as txt_file:
        st.download_button("⬇️ Download TXT Report", txt_file, txt_filename)

    with open(pdf_filename, "rb") as pdf_file:
        st.download_button("⬇️ Download PDF Report", pdf_file, pdf_filename)

