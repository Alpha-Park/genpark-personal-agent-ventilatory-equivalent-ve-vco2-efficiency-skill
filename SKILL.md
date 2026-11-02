---
name: genpark-personal-agent-ventilatory-equivalent-ve-vco2-efficiency-skill
description: Deterministic evaluation of ventilatory efficiency, VE/VCO2 regression slope, pulmonary gas exchange matching, and Beaver V-slope threshold detection.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Ventilatory Efficiency & VE/VCO2 Slope Cardiorespiratory Skill

## Overview
The `genpark-personal-agent-ventilatory-equivalent-ve-vco2-efficiency-skill` provides sovereign personal agents with cardiopulmonary exercise testing (CPET) analytics. Ventilatory efficiency evaluates how effectively the pulmonary and cardiovascular systems match ventilation to metabolic demands. The slope of minute ventilation ($\dot{V}_E$) plotted against carbon dioxide production ($\dot{V}CO_2$) serves as an independent predictor of cardiorespiratory performance, reflecting pulmonary dead space ($V_D / V_T$), arterial $PCO_2$ regulation, and ventilation-perfusion matching.

## Physiological Model & Mathematics
1. **Ventilatory Equivalent Relationship**:
   $$\frac{\dot{V}_E}{\dot{V}CO_2} = \frac{k}{PaCO_2 \cdot (1 - V_D / V_T)}$$
2. **Ordinary Least-Squares Linear Regression Slope**:
   $$\text{Slope} = \frac{\sum (\dot{V}CO_{2,i} - \overline{\dot{V}CO}_2)(\dot{V}_{E,i} - \overline{\dot{V}}_E)}{\sum (\dot{V}CO_{2,i} - \overline{\dot{V}CO}_2)^2}$$
   - **Optimal / Athletic**: $\le 28.0$.
   - **Normal Range**: $28.0 - 34.0$.
   - **Elevated Inefficiency**: $34.0 - 39.0$.
   - **Severe Ventilation Mismatch**: $> 39.0$.
3. **Beaver V-Slope Anaerobic Threshold**:
   Identifies the inflection point where $\Delta \dot{V}CO_2 / \Delta \dot{V}O_2 > 1.0$, demarcating the transition from pure aerobic metabolism to bicarbonate buffering of excess hydrogen ions.
4. **Cardiorespiratory Efficiency Index ($CREI$)**:
   Maps the observed slope into a 0 - 100 efficiency rating.

## Tools & Endpoints
- `calculate_ve_vco2_slope`: Computes the $\dot{V}_E/\dot{V}CO_2$ linear slope, $R^2$, and $CREI$ score.
- `detect_ventilatory_anaerobic_threshold`: Identifies the first ventilatory threshold (VT1 / VAT) using V-slope inflection criteria.
