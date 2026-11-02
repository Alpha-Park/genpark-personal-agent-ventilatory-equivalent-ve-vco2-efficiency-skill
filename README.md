# Ventilatory Efficiency & VE/VCO2 Slope Cardiorespiratory Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](https://github.com/alphaparkinc/genpark-personal-agent-ventilatory-equivalent-ve-vco2-efficiency-skill)
[![OpenClaw Ready](https://img.shields.io/badge/OpenClaw-Compatible-purple.svg)](https://github.com/alphaparkinc/genpark-personal-agent-ventilatory-equivalent-ve-vco2-efficiency-skill)
[![MCP Protocol](https://img.shields.io/badge/MCP-Standard-orange.svg)](https://modelcontextprotocol.io/)

A sovereign personal agent capability for computational CPET analysis, calculating the $\dot{V}_E / \dot{V}CO_2$ ventilatory equivalent slope, pulmonary dead space fraction, and V-slope anaerobic threshold.

## Architecture

```mermaid
flowchart TD
    CPETData["CPET Timeseries: VE (L/min), VCO2 (L/min), VO2 (L/min)"] --> RegressionEngine["Linear Least-Squares Regression (VE vs VCO2)"]
    RegressionEngine --> SlopeMetrics["VE/VCO2 Slope, Intercept & R² Correlation"]
    CPETData --> VSlopeEngine["Beaver V-Slope Inflection Detection (Delta VCO2 / Delta VO2 > 1.0)"]
    VSlopeEngine --> Threshold["Ventilatory Anaerobic Threshold (VAT / VT1)"]
    SlopeMetrics & Threshold --> CREI["Cardiorespiratory Efficiency Index (0 - 100)"]
    CREI --> AgentPrescription["OpenClaw / Hermes Zone 2 & Threshold Pacing Directives"]
```

## Quickstart

```python
from client import VentilatoryEfficiencyClient

client = VentilatoryEfficiencyClient()

# Incremental exercise gas exchange series
vco2 = [0.65, 0.95, 1.30, 1.70, 2.15, 2.60, 3.10]
ve = [18.2, 25.5, 34.0, 44.5, 56.0, 68.5, 82.0]

slope_res = client.calculate_ve_vco2_slope(ve, vco2)

print("VE/VCO2 Slope:", slope_res["ve_vco2_slope"])
print("Efficiency Index:", slope_res["cardiorespiratory_efficiency_index"], "/ 100")
print("Status:", slope_res["status"])
```

## MCP Server Integration

Add to your `claude_desktop_config.json` or OpenClaw tool registry:

```json
{
  "mcpServers": {
    "ventilatory-efficiency": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-ventilatory-equivalent-ve-vco2-efficiency-skill/mcp_server.py"]
    }
  }
}
```

## License
MIT License.
