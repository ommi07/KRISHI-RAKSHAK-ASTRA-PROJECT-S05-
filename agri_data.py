"""
Regional and crop configuration for the agriculture project.

Stores:
- Regional coordinates and baseline satellite indices (NDVI/NDWI)
- Main regional pests and default soil types
- Crop soil compatibility, growing seasons, economics, drought tolerance, and care guidance
"""

REGIONS = {
    "Sehore / Bhopal (MP)": {
        "lat": 23.20,
        "lon": 77.08,
        "base_ndvi": 0.62,
        "base_ndwi": 0.18,
        "main_pest": "Stem Borer & Aphids",
        "soil_default": "Black Soil",
    },
    "Cuttack (Odisha)": {
        "lat": 20.46,
        "lon": 85.88,
        "base_ndvi": 0.68,
        "base_ndwi": 0.32,
        "main_pest": "Brown Planthopper",
        "soil_default": "Alluvial Soil",
    },
    "Jodhpur (Rajasthan)": {
        "lat": 26.24,
        "lon": 73.02,
        "base_ndvi": 0.34,
        "base_ndwi": -0.15,
        "main_pest": "Desert Locust",
        "soil_default": "Sandy Soil",
    },
    "Nashik (Maharashtra)": {
        "lat": 19.99,
        "lon": 73.78,
        "base_ndvi": 0.58,
        "base_ndwi": 0.12,
        "main_pest": "Thrips & Fungal Blight",
        "soil_default": "Black Soil",
    },
}

CROPS = {
    "Wheat": {
        "soils": ["Black Soil", "Alluvial Soil"],
        "seasons": ["Rabi (Oct-Mar)", "Jan-Mar (Late Rabi)"],
        "cost_per_acre": 18000,
        "revenue_per_acre": 42000,
        "drought_tolerance": "Medium",
        "care": (
            "Irrigate at crown-root and flowering stages. "
            "Avoid excess nitrogen during high humidity."
        ),
    },
    "Rice (Paddy)": {
        "soils": ["Alluvial Soil", "Black Soil"],
        "seasons": ["Kharif (Jun-Oct)"],
        "cost_per_acre": 24000,
        "revenue_per_acre": 52000,
        "drought_tolerance": "Low",
        "care": (
            "Maintain 2-5 cm standing water. Monitor lower stems "
            "for planthoppers after heavy rain."
        ),
    },
    "Soybean": {
        "soils": ["Black Soil", "Red Soil"],
        "seasons": ["Kharif (Jun-Oct)"],
        "cost_per_acre": 15000,
        "revenue_per_acre": 36000,
        "drought_tolerance": "Medium",
        "care": (
            "Ensure proper field drainage to prevent root rot. "
            "Scout leaves weekly for caterpillars."
        ),
    },
    "Bajra (Pearl Millet)": {
        "soils": ["Sandy Soil", "Red Soil", "Black Soil"],
        "seasons": ["Kharif (Jun-Oct)", "Zaid (Mar-Jun)"],
        "cost_per_acre": 10000,
        "revenue_per_acre": 26000,
        "drought_tolerance": "High",
        "care": (
            "Requires minimal irrigation. Ideal backup crop for "
            "low-rainfall and drought-prone zones."
        ),
    },
    "Chickpea (Chana)": {
        "soils": ["Black Soil", "Sandy Soil", "Alluvial Soil"],
        "seasons": ["Rabi (Oct-Mar)", "Jan-Mar (Late Rabi)"],
        "cost_per_acre": 14000,
        "revenue_per_acre": 38000,
        "drought_tolerance": "High",
        "care": (
            "Needs only 1-2 light irrigations. Keep weeds clear "
            "during the first 40 days."
        ),
    },
    "Onion": {
        "soils": ["Black Soil", "Alluvial Soil", "Red Soil"],
        "seasons": [
            "Rabi (Oct-Mar)",
            "Jan-Mar (Late Rabi)",
            "Kharif (Jun-Oct)",
        ],
        "cost_per_acre": 32000,
        "revenue_per_acre": 75000,
        "drought_tolerance": "Low",
        "care": (
            "Highly sensitive to waterlogging and hailstorms. "
            "Use raised beds and fungicide before rain."
        ),
    },
}
