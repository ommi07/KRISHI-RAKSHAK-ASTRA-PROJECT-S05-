# 🌾 Krishi Rakshak — Space-to-Soil Agri & Disaster Shield

[![Live App](https://img.shields.io/badge/Live_App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://krishi-raksha.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![ASTRA 2026](https://img.shields.io/badge/ASTRA_2026-Team_05-1B4332?style=for-the-badge)](https://krishi-raksha.streamlit.app/)

**ASTRA 2026 | Team 05 (Error 404 not found)**  
**Team Members:** Omm Satyaprakash Nayak, Hrugved Sharad Rathode  
**Domains:** Domain 02 (Earth Observation & Satellite Applications) + Domain 03 (Space-Based Disaster Management)

---

## 🔗 Quick Links
- **🌐 Live Deployed App:** [https://krishi-raksha.streamlit.app/](https://krishi-raksha.streamlit.app/)
- **📊 Idea Pitch Deck (PPT):** [View Idea Pitch Presentation](./Idea_Pitch_Deck.pptx)

---

## 🌍 Overview
**Krishi Rakshak** is a space-to-soil agricultural and disaster decision-support platform built for Indian farmers. It translates satellite vegetation and water indices (**NDVI** & **NDWI**) alongside live pan-India weather data into clear crop calendars, pest warnings, 72-hour disaster playbooks, and PMFBY insurance damage reports.

---

## ✨ Key Features

| Module | What It Does |
| :--- | :--- |
| **📍 Pan-India Town & District Search** | Live geocoding via Open-Meteo allows farmers to type any Indian town or district—or pick from preset regions—and instantly load local maps and weather. |
| **💧 Aqua-Watch & Disaster Shield** | Tracks live temperature, wind, and rainfall with an 8-week **NDWI** time-lapse map and real-time alerts for Cyclones, Hailstorms, Floods, and Droughts. |
| **🌿 Crop Stress & Pest Radar** | Visualizes 8-week **NDVI** vegetation health progression alongside bioclimatic pest outbreak probabilities (Locusts, Brown Planthopper, Stem Borer & Aphids). |
| **📅 Auto Crop Calendar & Month Checker** | Automatically recommends suitable crops for the selected region and soil type with exact seasons, sowing/harvest months, and duration in days—plus an any-crop, any-month suitability checker. |
| **📈 Smart Profit & Radar Comparison** | Calculates input cost, gross revenue, net profit, and success probability, with a **5-axis Radar Chart** comparing the chosen crop against safer alternatives. |
| **🛡️ Disaster-to-Farm Impact Engine** | Interactive 72-hour emergency checklist that updates **Estimated Loss Prevented (₹)** in real time and generates a downloadable **PMFBY Satellite Damage Summary (.txt)**. |

---

## 🛰️ Satellite Index Framework

Krishi Rakshak models two core Earth Observation spectral indices aligned with Indian space data portals:

- **NDVI (Normalized Difference Vegetation Index)** — Measures crop vigor and early stress:
  $$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$$

- **NDWI (Normalized Difference Water Index)** — Detects surface water expansion, flood risk, and reservoir shrinkage:
  $$\text{NDWI} = \frac{\text{Green} - \text{NIR}}{\text{Green} + \text{NIR}}$$

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    A[User Input: Town / Soil / Crop / Month] --> B[weather_api.py<br/>Open-Meteo Weather & Geocoding]
    A --> C[agri_data.py<br/>Regional & Crop Knowledge Base]
    B --> D[risk_engine.py<br/>Disaster, Pest, Profit & PMFBY Engine]
    C --> D
    D --> E[map_view.py<br/>Plotly NDVI/NDWI Maps & 5-Axis Radar]
    D --> F[app.py<br/>Streamlit Interactive Dashboard]
    E --> F
