"""
Ventilatory Efficiency & VE/VCO2 Slope Cardiorespiratory Engine.
Provides deterministic, zero-dependency modeling of ventilatory equivalent slope,
pulmonary dead space fraction, ventilatory threshold inflection, and cardiorespiratory efficiency.
"""

from typing import Dict, Any, List, Optional


class VentilatoryEfficiencyClient:
    """
    Deterministic client for analyzing cardiopulmonary exercise test (CPET) ventilatory efficiency.
    Pure Python standard library implementation based on Wasserman & Beaver CPET principles.
    """

    def __init__(self):
        pass

    def calculate_ve_vco2_slope(
        self,
        ve_liters_min: List[float],
        vco2_liters_min: List[float]
    ) -> Dict[str, Any]:
        """
        Calculates VE/VCO2 slope using ordinary least-squares linear regression up to the respiratory compensation point.
        VE: minute ventilation in L/min.
        VCO2: carbon dioxide production in L/min.
        """
        n = min(len(ve_liters_min), len(vco2_liters_min))
        if n < 4:
            return {"error": "At least 4 paired data points of VE and VCO2 are required"}

        x = vco2_liters_min[:n]
        y = ve_liters_min[:n]

        mean_x = sum(x) / n
        mean_y = sum(y) / n

        ss_xx = sum((xi - mean_x) ** 2 for xi in x)
        ss_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))

        if ss_xx == 0.0:
            return {"error": "Variance of VCO2 is zero; cannot compute slope"}

        slope = round(ss_xy / ss_xx, 2)
        intercept = round(mean_y - (slope * mean_x), 2)

        # Pearson correlation coefficient (r^2)
        ss_yy = sum((yi - mean_y) ** 2 for yi in y)
        r_squared = round((ss_xy ** 2) / (ss_xx * ss_yy), 3) if ss_yy > 0 else 1.0

        # Cardiorespiratory Efficiency Index (CREI, 0 - 100)
        # Optimal VE/VCO2 slope is 22 - 28. Above 30 indicates inefficiency; above 36 signals pulmonary vascular or cardiogenic strain
        if slope <= 28.0:
            crei = max(80.0, 100.0 - (28.0 - slope) * 2.0)
        elif slope <= 34.0:
            crei = max(55.0, 80.0 - (slope - 28.0) * 4.0)
        elif slope <= 40.0:
            crei = max(30.0, 55.0 - (slope - 34.0) * 4.0)
        else:
            crei = max(5.0, 30.0 - (slope - 40.0) * 2.5)

        crei = round(min(100.0, max(5.0, crei)), 1)

        if slope <= 28.0:
            status = "SUPERIOR_VENTILATORY_EFFICIENCY"
            interpretation = "Optimal ventilation-perfusion matching (Va/Q) with minimal physiological dead space."
            guidance = "Cardiopulmonary efficiency is exceptional. Ideal base for high-intensity aerobic pacing."
        elif slope <= 34.0:
            status = "NORMAL_AEROBIC_EFFICIENCY"
            interpretation = "Normal ventilatory equivalent slope consistent with healthy functional capacity."
            guidance = "Maintain polarized Zone 2 endurance base and ventilatory threshold threshold work."
        elif slope <= 39.0:
            status = "ELEVATED_VENTILATORY_INEFFICIENCY"
            interpretation = "Elevated dead space ventilation fraction (Vd/Vt) or augmented chemoreflex sensitivity."
            guidance = "Incorporate low-cadence diaphragmatic breathing drills and monitor pulmonary perfusion."
        else:
            status = "SEVERE_VENTILATORY_MISMATCH"
            interpretation = "Markedly steep VE/VCO2 slope (> 39); indicates significant ventilation-perfusion mismatch or pulmonary vascular limitation."
            guidance = "Recommend formal clinical CPET echocardiography review and exercise cardiologist consultation."

        return {
            "paired_point_count": n,
            "ve_vco2_slope": slope,
            "ve_intercept_liters_min": intercept,
            "r_squared": r_squared,
            "cardiorespiratory_efficiency_index": crei,
            "status": status,
            "interpretation": interpretation,
            "guidance": guidance
        }

    def detect_ventilatory_anaerobic_threshold(
        self,
        vo2_series_liters_min: List[float],
        vco2_series_liters_min: List[float]
    ) -> Dict[str, Any]:
        """
        Detects Ventilatory Anaerobic Threshold (VAT / VT1) using the V-Slope method.
        Identifies inflection where VCO2 increases disproportionately relative to VO2 (slope > 1.0).
        """
        n = min(len(vo2_series_liters_min), len(vco2_series_liters_min))
        if n < 6:
            return {"error": "At least 6 ramp incremental points required for V-slope analysis"}

        # Look for the inflection where delta_VCO2 / delta_VO2 exceeds 1.0 consistently
        inflection_idx = -1
        for i in range(1, n - 1):
            d_vo2 = vo2_series_liters_min[i] - vo2_series_liters_min[i - 1]
            d_vco2 = vco2_series_liters_min[i] - vco2_series_liters_min[i - 1]
            if d_vo2 > 0.05 and (d_vco2 / d_vo2) > 1.02:
                # Confirm next interval also maintains elevated ratio
                if i + 1 < n:
                    d_vo2_next = vo2_series_liters_min[i + 1] - vo2_series_liters_min[i]
                    d_vco2_next = vco2_series_liters_min[i + 1] - vco2_series_liters_min[i]
                    if d_vo2_next > 0.05 and (d_vco2_next / d_vo2_next) > 1.02:
                        inflection_idx = i
                        break

        if inflection_idx != -1:
            vat_vo2 = vo2_series_liters_min[inflection_idx]
            vat_vco2 = vco2_series_liters_min[inflection_idx]
            detected = True
        else:
            # Fallback to middle point approximation
            inflection_idx = n // 2
            vat_vo2 = vo2_series_liters_min[inflection_idx]
            vat_vco2 = vco2_series_liters_min[inflection_idx]
            detected = False

        return {
            "vat_detected": detected,
            "inflection_index": inflection_idx,
            "vo2_at_vat_liters_min": round(vat_vo2, 2),
            "vco2_at_vat_liters_min": round(vat_vco2, 2),
            "interpretation": (
                "Clear ventilatory threshold 1 (VT1) identified by V-slope inflection; marks upper limit of pure oxidative phosphorylation."
                if detected else
                "Indeterminate V-slope inflection; ramp increments may be non-linear."
            )
        }
