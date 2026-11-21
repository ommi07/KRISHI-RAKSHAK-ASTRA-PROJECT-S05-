import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agri_data import CROPS

def create_satellite_map(lat, lon, current_val, mode="NDVI", week=8, sim_mode="Normal (Live Weather)"):
    progress = (week - 1) / 7.0
    if sim_mode == "Severe Drought":
        week_val = current_val + (1.0 - progress) * 0.25
    elif sim_mode in ("Cyclone Alert", "Hailstorm & Heavy Rain") and mode == "NDWI":
        week_val = current_val - (1.0 - progress) * 0.30
    else:
        week_val = current_val - (1.0 - progress) * 0.08

    offsets = [-0.04, -0.02, 0.0, 0.02, 0.04]
    rows = []
    for i, dlat in enumerate(offsets):
        for j, dlon in enumerate(offsets):
            val = round(max(-1.0, min(1.0, week_val + (i - 2) * 0.04 - (j - 2) * 0.03)), 2)
            rows.append({
                "lat": lat + dlat,
                "lon": lon + dlon,
                mode: val,
                "Grid Cell": f"Sector {i+1}-{j+1}"
            })

    df = pd.DataFrame(rows)
    color_scale = "RdYlGn" if mode == "NDVI" else "RdBu"

    fig = px.scatter_map(
        df, lat="lat", lon="lon", color=mode,
        hover_name="Grid Cell", color_continuous_scale=color_scale,
        range_color=[-0.5, 0.8],
        center={"lat": lat, "lon": lon},
        zoom=10, height=360
    )
    fig.update_traces(marker=dict(size=18, opacity=0.85))
    fig.update_layout(
        map_style="carto-positron",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def _score_crop_axes(crop_name, soil, season, total_risk):
    c = CROPS[crop_name]
    profit_score = min(100, int(((c["revenue_per_acre"] - c["cost_per_acre"]) / 45000) * 100))
    soil_score = 95 if soil in c["soils"] else 45
    season_score = 95 if season in c["seasons"] else 40
    tol_map = {"High": 90, "Medium": 60, "Low": 30}
    drought_score = tol_map[c["drought_tolerance"]]
    survival_score = max(15, 100 - int(total_risk * (0.5 if c["drought_tolerance"] == "High" else 0.85)))
    return [profit_score, soil_score, season_score, drought_score, survival_score]

def create_crop_radar(target_crop, alt_crop, soil, season, total_risk):
    categories = ["Profit Potential", "Soil Match", "Season Match", "Drought Tolerance", "Disaster Survival"]
    target_scores = _score_crop_axes(target_crop, soil, season, total_risk)
    alt_scores = _score_crop_axes(alt_crop, soil, season, total_risk)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=target_scores + [target_scores[0]],
        theta=categories + [categories[0]],
        fill="toself", name=f"Selected: {target_crop}",
        line_color="#B91C1C", fillcolor="rgba(185, 28, 28, 0.18)"
    ))
    fig.add_trace(go.Scatterpolar(
        r=alt_scores + [alt_scores[0]],
        theta=categories + [categories[0]],
        fill="toself", name=f"Alternative: {alt_crop}",
        line_color="#1B4332", fillcolor="rgba(27, 67, 50, 0.22)"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        height=340, margin=dict(t=30, b=20, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig