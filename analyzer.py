import re

RANGES = {
    "hemoglobin": (12.0, 17.5, "g/dL"),
    "fasting glucose": (70, 99, "mg/dL"),
    "total cholesterol": (0, 199, "mg/dL"),
    "ldl cholesterol": (0, 99, "mg/dL"),
    "hdl cholesterol": (40, 100, "mg/dL"),
    "triglycerides": (0, 149, "mg/dL"),
    "vitamin d": (30, 100, "ng/mL"),
    "tsh": (0.4, 4.0, "mIU/L"),
}

def analyze(text):
    results = []
    for line in text.splitlines():
        m = re.match(r"\s*([A-Za-z0-9 ]+?)\s*[:=]\s*([\d.]+)", line)
        if not m:
            continue
        name = m.group(1).strip().lower()
        if name not in RANGES:
            continue
        value = float(m.group(2))
        low, high, unit = RANGES[name]
        status = "LOW" if value < low else "HIGH" if value > high else "NORMAL"
        results.append({"Test": name.title(), "Value": value,
                        "Unit": unit, "Status": status})
    return results