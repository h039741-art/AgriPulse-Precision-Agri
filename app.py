def calculate_agripulse_score(crop, n, p, k, ph):
    # Data from Domain Logic [cite: 10, 12, 13]
    base_score = 100
    penalties = 0
    deficiencies = []
    actions = []

    # 1. pH Penalty (-20 pts) [cite: 13]
    ranges = {"TOMATO": (6.0, 7.0), "WHEAT": (6.0, 7.5), "RICE": (5.0, 6.5), "MAIZE": (5.8, 7.0)}
    low, high = ranges.get(crop.upper())
    if not (low <= ph <= high):
        penalties += 20

    # 2. Universal Nutrient Thresholds [cite: 10, 14]
    if n < 20: 
        penalties += 15
        deficiencies.append("Nitrogen")
        actions.append("Apply Urea Fertilizer")
    if p < 15: 
        penalties += 15
        deficiencies.append("Phosphorus")
        actions.append("Apply DAP")
    if k < 150: 
        penalties += 15
        deficiencies.append("Potassium")
        actions.append("Apply MOP")

    # 3. Critical Crop Penalty (-10 pts) [cite: 12, 15]
    critical_thresholds = {"TOMATO": ("k", 200), "WHEAT": ("n", 30), "RICE": ("p", 25), "MAIZE": ("n", 35)}
    nutrient_key, threshold = critical_thresholds.get(crop.upper())
    
    val_to_check = {"n": n, "p": p, "k": k}[nutrient_key]
    if val_to_check < threshold:
        penalties += 10 # This is the "Hard-Coded" mandatory penalty 

    final_score = max(0, base_score - penalties)
    return final_score, deficiencies, actions
