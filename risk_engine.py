"""
Krishi Rakshak - Rule-based risk engine.

Contains all rule-based calculations: disaster alerts, pest radar,
crop success probability, budget/loss math, 72-hour playbook, and PMFBY report.

Requires an `agri_data.py` file in the same folder that defines the CROPS dict.
"""

from datetime import datetime
from agri_data import CROPS


def detect_disasters(weather, ndwi):
    alerts = []
    risk_score = 10

    if weather["wind"] >= 65:
        alerts.append("Cyclone / High Wind Warning")
        risk_score += 45
    elif weather["wind"] >= 45 and weather["rain"] >= 35:
        alerts.append("Hailstorm & Heavy Rain Alert")
        risk_score += 38

    if weather["rain"] >= 50 or ndwi >= 0.45:
        alerts.append("Flood / Waterlogging Risk (High NDWI)")
        risk_score += 25

    if (weather["temp"] >= 40 and weather["rain"] == 0) or ndwi <= -0.25:
        alerts.append("Drought / Reservoir Shrinkage Alert (Low NDWI)")
        risk_score += 35

    if not alerts:
        alerts.append("Normal Conditions (No Active Disaster)")

    return alerts, min(95, risk_score)


def calculate_pest_risk(region_name, pest_name, weather, ndvi):
    prob = 20
    reason = "Baseline seasonal activity."

    if "Locust" in pest_name and weather["wind"] >= 15 and ndvi >= 0.25:
        prob = 72
        reason = "Wind movement + vegetation greening favor locust swarms."
    elif weather["humidity"] >= 75 and 22 <= weather["temp"] <= 34:
        prob = 78
        reason = "High humidity and warm temperature trigger rapid pest/fungal growth."
    elif ndvi < 0.40:
        prob = 62
        reason = "Low NDVI indicates stressed crops, making plants vulnerable to pests."

    level = "High" if prob >= 65 else ("Moderate" if prob >= 40 else "Low")
    return {"pest": pest_name, "prob": prob, "level": level, "reason": reason}


def evaluate_crop(crop_name, soil, season, acres, total_risk):
    crop = CROPS[crop_name]
    base_success = 85

    if soil not in crop["soils"]:
        base_success -= 22
    if season not in crop["seasons"]:
        base_success -= 25

    # Adjust success rate using live satellite & disaster risk
    penalty = int(total_risk * 0.55)
    if crop["drought_tolerance"] == "High" and total_risk > 40:
        penalty = int(penalty * 0.7)

    success_prob = max(10, min(95, base_success - penalty))
    failure_prob = 100 - success_prob

    total_cost = crop["cost_per_acre"] * acres
    expected_rev = crop["revenue_per_acre"] * acres
    normal_profit = expected_rev - total_cost

    # Impact Engine math: Loss without action vs. Loss saved with early action
    loss_without_action = int(expected_rev * (failure_prob / 100.0))
    loss_with_action = int(loss_without_action * 0.35)
    loss_saved = loss_without_action - loss_with_action

    return {
        "success_prob": success_prob,
        "failure_prob": failure_prob,
        "total_cost": total_cost,
        "expected_rev": expected_rev,
        "normal_profit": normal_profit,
        "loss_without_action": loss_without_action,
        "loss_with_action": loss_with_action,
        "loss_saved": loss_saved,
        "care": crop["care"]
    }


def get_safer_alternatives(soil, season, current_crop):
    recs = []
    for name, info in CROPS.items():
        if name == current_crop:
            continue
        score = 0
        if soil in info["soils"]:
            score += 1
        if season in info["seasons"]:
            score += 1
        if info["drought_tolerance"] == "High":
            score += 1
        if score >= 2:
            recs.append((name, info["drought_tolerance"]))
    return recs


def get_72hr_playbook(sim_mode, crop_name):
    if sim_mode == "Cyclone Alert":
        return [
            f"0-24 hrs: Harvest any mature {crop_name} immediately and move produce to dry storage.",
            "24-48 hrs: Stop all pesticide/fertilizer spraying to prevent chemical wash-off.",
            "48-72 hrs: Clear field drainage channels and secure loose farm equipment."
        ]
    if sim_mode == "Hailstorm & Heavy Rain":
        return [
            f"0-24 hrs: Pause irrigation and fertilizer application for {crop_name}.",
            "24-48 hrs: Open bunds/trenches so excess rainwater drains out of root zones.",
            "48-72 hrs: Spray preventive fungicide after rain stops to block fungal blight."
        ]
    if sim_mode == "Severe Drought":
        return [
            f"0-24 hrs: Switch {crop_name} to evening/drip irrigation to cut evaporation loss.",
            "24-48 hrs: Apply organic mulch between rows to lock in remaining soil moisture.",
            "48-72 hrs: Consider switching next sowing cycle to drought-tolerant Bajra or Chana."
        ]
    return [
        f"0-24 hrs: Conditions are stable. Follow standard irrigation for {crop_name}.",
        "24-48 hrs: Scout field edges for early signs of pests.",
        "48-72 hrs: Monitor weekly NDVI/NDWI updates before applying top-dress fertilizer."
    ]


def generate_pmfby_report(region, crop, acres, weather, ndvi, ndwi, alerts, result):
    today = datetime.now().strftime("%d %b %Y, %H:%M IST")
    return (
        f"KRISHI RAKSHAK - PMFBY SATELLITE DAMAGE SUMMARY\n"
        f"==================================================\n"
        f"Generated On : {today}\n"
        f"Region       : {region}\n"
        f"Crop & Area  : {crop} ({acres} acres)\n"
        f"Active Alert : {', '.join(alerts)}\n"
        f"Weather Peak : Wind {weather['wind']} km/h | Rain {weather['rain']} mm | Temp {weather['temp']} C\n"
        f"Space Index  : NDVI = {ndvi} (Crop Health) | NDWI = {ndwi} (Water Level)\n"
        f"Est. Loss    : Rs. {result['loss_without_action']:,} (Without Action)\n"
        f"Data Ref     : ISRO Bhuvan / Bhoonidhi / MOSDAC / VEDAS & Open-Meteo\n"
    )
