import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from agri_data import REGIONS, CROPS
from weather_api import get_live_weather, apply_alert_simulation, search_indian_location
from risk_engine import (
    detect_disasters, calculate_pest_risk, evaluate_crop,
    get_safer_alternatives, get_72hr_playbook, generate_pmfby_report
)
from map_view import create_satellite_map, create_crop_radar

st.set_page_config(page_title="Krishi Rakshak | Space-to-Soil Shield", layout="wide")

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Detailed crop calendar (months & duration in days)
CROP_CALENDAR = {
    "Wheat": {
        "season": "Rabi (Oct–Mar)",
        "sowing_months": ["October", "November", "December"],
        "active_months": ["January", "February", "March"],
        "window": "Oct 15 – Mar 30",
        "days": "120–140 days"
    },
    "Rice (Paddy)": {
        "season": "Kharif (Jun–Oct)",
        "sowing_months": ["June", "July"],
        "active_months": ["August", "September", "October", "November"],
        "window": "Jun 15 – Nov 15",
        "days": "120–150 days"
    },
    "Soybean": {
        "season": "Kharif (Jun–Oct)",
        "sowing_months": ["June", "July"],
        "active_months": ["August", "September", "October"],
        "window": "Jun 20 – Oct 15",
        "days": "95–110 days"
    },
    "Chickpea (Chana)": {
        "season": "Rabi (Oct–Mar)",
        "sowing_months": ["October", "November"],
        "active_months": ["December", "January", "February", "March"],
        "window": "Oct 15 – Mar 15",
        "days": "100–120 days"
    },
    "Onion": {
        "season": "Rabi / Late Kharif",
        "sowing_months": ["October", "November", "January"],
        "active_months": ["December", "February", "March", "April"],
        "window": "Oct 20 – Apr 15",
        "days": "110–130 days"
    },
    "Bajra (Pearl Millet)": {
        "season": "Kharif / Zaid",
        "sowing_months": ["June", "July", "March"],
        "active_months": ["August", "September", "April", "May"],
        "window": "Jun 15 – Sep 30",
        "days": "75–90 days"
    },
    "Mustard": {
        "season": "Rabi (Oct–Mar)",
        "sowing_months": ["October", "November"],
        "active_months": ["December", "January", "February", "March"],
        "window": "Oct 10 – Mar 10",
        "days": "110–130 days"
    },
    "Cotton": {
        "season": "Kharif (May–Nov)",
        "sowing_months": ["May", "June"],
        "active_months": ["July", "August", "September", "October", "November"],
        "window": "May 15 – Nov 30",
        "days": "150–180 days"
    }
}

def get_calendar_info(crop):
    return CROP_CALENDAR.get(crop, {
        "season": "Seasonal",
        "sowing_months": ["June", "July", "October", "November"],
        "active_months": ["August", "September", "December", "January", "February"],
        "window": "Jun–Oct / Oct–Mar",
        "days": "100–120 days"
    })

def check_month_suitability(crop, month):
    cal = get_calendar_info(crop)
    if month in cal["sowing_months"]:
        return "Ideal Sowing Window", "success", f"{month} is an optimal sowing month for {crop} ({cal['window']}, {cal['days']})."
    elif month in cal["active_months"]:
        return "Active Growing / Harvest Window", "info", f"{crop} is normally already growing or nearing harvest in {month}. Late sowing may reduce yield."
    else:
        return "Off-Season / High Risk", "warning", f"{month} is outside the recommended window ({cal['window']}) for {crop}. Consider a seasonal crop instead."

# --- HEADER ---
st.title("Krishi Rakshak")
st.caption("Space-to-Soil Agricultural & Disaster Decision Platform  |  ASTRA 2026 (Domains 02 & 03)  |  Team 05")

# --- SIDEBAR: DIRECT SEARCH + FARMER INPUTS ---
st.sidebar.header("Farm & Region Profile")
custom_place = st.sidebar.text_input(
    "Search Any Indian Town / District",
    placeholder="Type e.g. Pune, Indore, Cuttack & press Enter"
)

if custom_place.strip():
    found = search_indian_location(custom_place.strip())
    if found:
        region_name = found["name"]
        region = found
        st.sidebar.success(f"Located: {region_name}")
    else:
        st.sidebar.error("Town/District not found. Using preset below.")
        region_name = st.sidebar.selectbox("Preset Region", list(REGIONS.keys()))
        region = REGIONS[region_name]
else:
    region_name = st.sidebar.selectbox("Or Choose Preset Region", list(REGIONS.keys()))
    region = REGIONS[region_name]

soil = st.sidebar.selectbox("Soil Type", ["Black Soil", "Alluvial Soil", "Red Soil", "Sandy Soil"])
season = st.sidebar.selectbox("Cultivation Season", ["Rabi (Oct-Mar)", "Jan-Mar (Late Rabi)", "Kharif (Jun-Oct)", "Zaid (Mar-Jun)"])
selected_month = st.sidebar.selectbox("Target Month to Check", MONTHS, index=10)  # Default: November
crop_name = st.sidebar.selectbox("Check Any Crop", list(CROPS.keys()))
acres = st.sidebar.number_input("Farm Area (Acres)", min_value=1, max_value=50, value=5)

st.sidebar.divider()
st.sidebar.header("Disaster Scenario Control")
sim_mode = st.sidebar.selectbox(
    "Active Weather / Alert Mode",
    ["Normal (Live Weather)", "Cyclone Alert", "Hailstorm & Heavy Rain", "Severe Drought"]
)

# --- BACKEND PROCESSING ---
raw_weather = get_live_weather(region["lat"], region["lon"])
weather, ndvi, ndwi = apply_alert_simulation(
    raw_weather, region["base_ndvi"], region["base_ndwi"], sim_mode
)
alerts, disaster_risk = detect_disasters(weather, ndwi)
pest_info = calculate_pest_risk(region_name, region["main_pest"], weather, ndvi)
total_risk = min(100, int(disaster_risk * 0.7 + pest_info["prob"] * 0.3))
crop_eval = evaluate_crop(crop_name, soil, season, acres, total_risk)

# --- TOP KPI BAR ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Regional Risk Index", f"{total_risk} / 100")
k2.metric("NDVI (Crop Vigor)", f"{ndvi}")
k3.metric("NDWI (Water Level)", f"{ndwi}")
k4.metric(f"{crop_name} Success Rate", f"{crop_eval['success_prob']}%")

st.divider()

# --- AUTO-RECOMMENDED CROPS FOR SELECTED REGION ---
rec_rows = []
for cname, cdata in CROPS.items():
    if soil in cdata["soils"]:
        cal = get_calendar_info(cname)
        rec_rows.append({
            "Recommended Crop": cname,
            "Season": cal["season"],
            "Best Months / Window": cal["window"],
            "Duration": cal["days"],
            "Drought Tolerance": cdata["drought_tolerance"]
        })

with st.expander(f"Recommended Crops & Calendar for {region_name} ({soil})", expanded=True):
    if rec_rows:
        st.dataframe(pd.DataFrame(rec_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No exact soil match found; check Tab 3 for full crop comparisons.")

# --- MAIN NAVIGATION TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Aqua-Watch & Disasters",
    "Crop Stress & Pest Radar",
    "Smart Crop & Month Advisor",
    "Impact Engine & PMFBY"
])

# TAB 1: AQUA-WATCH & DISASTER SHIELD
with tab1:
    st.subheader(f"Aqua-Watch (NDWI) & Alerts — {region_name}")
    st.info(
        f"Source: {weather['source']}  |  Temperature: {weather['temp']} °C  |  "
        f"Wind Speed: {weather['wind']} km/h  |  Rainfall: {weather['rain']} mm"
    )
    for alert in alerts:
        if "Normal" in alert:
            st.success(alert)
        else:
            st.error(alert)

    week_ndwi = st.slider("Satellite Time-Lapse (Water Change Detection)", 1, 8, 8, format="Week %d", key="ndwi_wk")
    st.plotly_chart(
        create_satellite_map(region["lat"], region["lon"], ndwi, mode="NDWI", week=week_ndwi, sim_mode=sim_mode),
        use_container_width=True
    )
    st.caption("NDWI Scale: Blue indicates surface water / flood expansion; Red-Brown indicates dry soil or shrinking reservoirs.")

# TAB 2: CROP STRESS & PEST RADAR
with tab2:
    st.subheader(f"Vegetation Stress (NDVI) & Pest Radar — {region_name}")
    col_map, col_pest = st.columns([2, 1])

    with col_map:
        week_ndvi = st.slider("Satellite Time-Lapse (Crop Health Progression)", 1, 8, 8, format="Week %d", key="ndvi_wk")
        st.plotly_chart(
            create_satellite_map(region["lat"], region["lon"], ndvi, mode="NDVI", week=week_ndvi, sim_mode=sim_mode),
            use_container_width=True
        )
        st.caption("NDVI Scale: Dark Green indicates healthy crops; Yellow-Red indicates early crop stress.")

    with col_pest:
        st.markdown("#### Regional Pest Radar")
        st.write(f"**Primary Threat:** {pest_info['pest']}")
        st.metric("Outbreak Probability", f"{pest_info['prob']}%", pest_info["level"])
        st.write(f"**Bioclimatic Trigger:** {pest_info['reason']}")

# TAB 3: SMART LAND, MONTH & PROFIT ADVISOR
with tab3:
    st.subheader(f"Crop & Month Check: {crop_name} in {selected_month} ({region_name})")

    status_label, status_type, status_msg = check_month_suitability(crop_name, selected_month)
    if status_type == "success":
        st.success(f"**{status_label}:** {status_msg}")
    elif status_type == "info":
        st.info(f"**{status_label}:** {status_msg}")
    else:
        st.warning(f"**{status_label}:** {status_msg}")

    m1, m2, m3 = st.columns(3)
    m1.metric("Estimated Input Cost", f"₹{crop_eval['total_cost']:,}")
    m2.metric("Expected Gross Revenue", f"₹{crop_eval['expected_rev']:,}")
    m3.metric("Projected Net Profit", f"₹{crop_eval['normal_profit']:,}")

    st.write(f"**Success Probability:** {crop_eval['success_prob']}%  |  **Failure Risk:** {crop_eval['failure_prob']}%")
    st.progress(crop_eval["success_prob"] / 100.0)
    st.info(f"**Recommended Care Guide:** {crop_eval['care']}")

    alts = get_safer_alternatives(soil, season, crop_name)
    if alts:
        st.markdown("#### Compare With Safer Alternative")
        alt_names = [a[0] for a in alts]
        chosen_alt = st.selectbox("Select Alternative Crop to Compare", alt_names)
        st.plotly_chart(
            create_crop_radar(crop_name, chosen_alt, soil, season, total_risk),
            use_container_width=True
        )

# TAB 4: DISASTER-TO-FARM IMPACT ENGINE
with tab4:
    st.subheader("Disaster-to-Farm Impact Engine & 72-Hour Playbook")
    col_check, col_chart = st.columns([1, 1.3])

    with col_check:
        st.markdown("#### Interactive 72-Hour Emergency Playbook")
        st.caption("Check off actions completed to see live financial protection:")
        steps = get_72hr_playbook(sim_mode, crop_name)
        completed = 0
        for idx, step in enumerate(steps):
            if st.checkbox(step, value=(idx == 0), key=f"step_{idx}"):
                completed += 1

        action_ratio = completed / len(steps)
        live_saved = int(crop_eval["loss_saved"] * action_ratio)
        live_remaining_loss = crop_eval["loss_without_action"] - live_saved

        st.success(f"Estimated Loss Prevented: ₹{live_saved:,}")

    with col_chart:
        fig_bar = go.Figure(data=[
            go.Bar(name="Loss Without Action", x=["Projected Loss"], y=[crop_eval["loss_without_action"]], marker_color="#B91C1C"),
            go.Bar(name="Loss After Selected Actions", x=["Projected Loss"], y=[live_remaining_loss], marker_color="#1B4332")
        ])
        fig_bar.update_layout(
            barmode="group", yaxis_title="Amount (₹)", height=300,
            margin=dict(t=20, b=20), paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()
    st.markdown("#### PMFBY Crop Insurance Satellite Evidence")
    report_txt = generate_pmfby_report(region_name, crop_name, acres, weather, ndvi, ndwi, alerts, crop_eval)
    st.download_button(
        label="Download PMFBY Satellite Damage Summary (.txt)",
        data=report_txt,
        file_name="pmfby_damage_summary.txt"
    )

st.divider()
st.caption("Data Alignment & Acknowledgments: ISRO Bhuvan, Bhoonidhi, MOSDAC, VEDAS | Live Weather: Open-Meteo API")