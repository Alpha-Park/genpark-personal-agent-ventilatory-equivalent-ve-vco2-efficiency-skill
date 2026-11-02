"""
Example usage for Ventilatory Efficiency & VE/VCO2 Slope Skill.
Demonstrates linear regression of CPET ramp data and V-slope threshold detection.
"""

from client import VentilatoryEfficiencyClient


def main():
    client = VentilatoryEfficiencyClient()

    print("=== 1. Calculating VE/VCO2 Ventilatory Slope ===")
    # Ramp incremental CPET data points
    vco2_series = [0.65, 0.95, 1.30, 1.70, 2.15, 2.60, 3.10]
    ve_series = [18.2, 25.5, 34.0, 44.5, 56.0, 68.5, 82.0]

    slope_res = client.calculate_ve_vco2_slope(ve_series, vco2_series)
    print(f"VE/VCO2 Slope: {slope_res['ve_vco2_slope']} (R^2: {slope_res['r_squared']})")
    print(f"Intercept: {slope_res['ve_intercept_liters_min']} L/min")
    print(f"Cardiorespiratory Efficiency Index: {slope_res['cardiorespiratory_efficiency_index']} / 100")
    print(f"Status: {slope_res['status']}")
    print(f"Interpretation: {slope_res['interpretation']}")
    print(f"Guidance: {slope_res['guidance']}")

    print("\n=== 2. Detecting Ventilatory Anaerobic Threshold (V-Slope) ===")
    vo2_series = [0.80, 1.15, 1.55, 1.90, 2.25, 2.55, 2.85]
    vat_res = client.detect_ventilatory_anaerobic_threshold(vo2_series, vco2_series)
    print(f"VAT Detected: {vat_res['vat_detected']}")
    print(f"Inflection Index: {vat_res['inflection_index']}")
    print(f"VO2 at VAT: {vat_res['vo2_at_vat_liters_min']} L/min")
    print(f"VCO2 at VAT: {vat_res['vco2_at_vat_liters_min']} L/min")
    print(f"Interpretation: {vat_res['interpretation']}")


if __name__ == "__main__":
    main()
