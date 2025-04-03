import gradio as gr
import torch
from transformers import pipeline
import folium
from geopy.geocoders import Nominatim
from twilio.rest import Client
import random

# Load AI Model (Example: Hugging Face Pre-trained Model)
model = pipeline("text-classification", model="distilbert-base-uncased")

# Dummy Function for AI Hurricane Prediction
def predict_hurricane(air_pressure, wind_speed, humidity):
    risk = (wind_speed * 0.5 + humidity * 0.3 + air_pressure * 0.2) / 100
    prediction = "High Risk" if risk > 0.6 else "Low Risk"
    
    return f"Hurricane Risk: {prediction} ({round(risk * 100, 2)}%)"

# Function for GIS Alert System
def send_alert(location):
    # Twilio setup (Replace with your credentials)
    account_sid = "your_account_sid"
    auth_token = "your_auth_token"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"⚠️ Hurricane Alert in {location}! Take necessary precautions.",
        from_="+1234567890", to="+9876543210"
    )
    return f"Alert sent to {location}!"

# Map Generator (Visualizing Affected Areas)
def generate_map(location):
    geolocator = Nominatim(user_agent="geoapi")
    loc = geolocator.geocode(location)
    
    map_ = folium.Map(location=[loc.latitude, loc.longitude], zoom_start=6)
    folium.Marker([loc.latitude, loc.longitude], tooltip="Hurricane Alert 🚨").add_to(map_)
    
    return map_._repr_html_()

# Gradio UI
with gr.Blocks() as app:
    gr.Markdown("# 🌪 AI Hurricane Prediction & Alert System")
    
    with gr.Row():
        air_pressure = gr.Number(label="Air Pressure (hPa)")
        wind_speed = gr.Number(label="Wind Speed (km/h)")
        humidity = gr.Number(label="Humidity (%)")
    
    predict_btn = gr.Button("Predict Hurricane Risk")
    result = gr.Textbox(label="Prediction Result")
    
    predict_btn.click(predict_hurricane, inputs=[air_pressure, wind_speed, humidity], outputs=result)

    gr.Markdown("### 📍 GIS Alert System")
    location = gr.Textbox(label="Enter Location")
    alert_btn = gr.Button("Send Alert")
    alert_result = gr.Textbox(label="Alert Status")
    
    alert_btn.click(send_alert, inputs=location, outputs=alert_result)
    
    gr.Markdown("### 🗺️ Map of Affected Area")
    map_btn = gr.Button("Generate Map")
    map_output = gr.HTML()
    
    map_btn.click(generate_map, inputs=location, outputs=map_output)

app.launch()
