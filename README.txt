# smart-agri-advisory-system

##Project Overview
Smart Agri Advisory System is an AI-powered platform that integrates drone-based crop image analysis, real-time weather data, and smart farming recommendations to help farmers monitor crop health efficiently.
It aligns with UN SDG 2 – Zero Hunger and UN SDG 13 – Climate Action, promoting sustainable agriculture and climate-resilient farming practices.

##Steps to Execute the Project
#Prerequisites
-Python 3.x installed
-VS Code or PyCharm IDE
-Internet connection for weather API access

##Setup Instructions
-Clone or download this repository to your local system.
-Open the project folder in VS Code.
-Install the required dependencies

##In the browser interface:
-Enter your city name (e.g., Chennai).
-Upload your crop image (.jpg, .png, .jpeg).
-Click "Generate Smart Report".

##The system will:
-Analyze the image using OpenCV (HSV masking) to calculate healthy crop percentage.
-Retrieve weather data using the OpenWeatherMap API.
-Combine both datasets to generate an AI-enhanced recommendation.
-Allow you to download the TXT and PDF reports automatically.

##Technologies Used
-Programming Language: Python
-Framework: Streamlit
-Libraries: OpenCV, NumPy, Requests, ReportLab, Tempfile, OS
-API: OpenWeatherMap
-Report Format: TXT and PDF

##Dashboard / Output
-After running the app, the dashboard displays:
-Healthy vs. Stressed Crop Percentage with progress bars.
-Weather-adjusted data (temperature, humidity, rainfall forecast).
-AI advisory including irrigation, nutrient, and crop maintenance suggestions.
-Downloadable PDF and TXT reports generated instantly.
