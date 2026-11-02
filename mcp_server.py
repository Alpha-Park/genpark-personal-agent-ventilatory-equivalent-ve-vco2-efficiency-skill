"""
MCP Server for Ventilatory Efficiency & VE/VCO2 Slope Cardiorespiratory Engine.
Exposes JSON-RPC endpoints for computing ventilatory equivalent slope and V-slope anaerobic threshold.
"""

import json
import sys
from client import VentilatoryEfficiencyClient

client = VentilatoryEfficiencyClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate_ve_vco2_slope",
                        "description": "Calculates VE/VCO2 ventilatory efficiency slope via linear regression, evaluating pulmonary dead space and cardiorespiratory efficiency index.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "ve_liters_min": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Minute ventilation series in L/min during incremental exercise"
                                },
                                "vco2_liters_min": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Carbon dioxide output series in L/min during incremental exercise"
                                }
                            },
                            "required": ["ve_liters_min", "vco2_liters_min"]
                        }
                    },
                    {
                        "name": "detect_ventilatory_anaerobic_threshold",
                        "description": "Detects Ventilatory Anaerobic Threshold (VAT / VT1) from VO2 and VCO2 timeseries using the Beaver V-slope inflection algorithm.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "vo2_series_liters_min": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Oxygen uptake series in L/min"
                                },
                                "vco2_series_liters_min": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Carbon dioxide output series in L/min"
                                }
                            },
                            "required": ["vo2_series_liters_min", "vco2_series_liters_min"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "calculate_ve_vco2_slope":
            res = client.calculate_ve_vco2_slope(
                ve_liters_min=args.get("ve_liters_min", []),
                vco2_liters_min=args.get("vco2_liters_min", [])
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        elif tool_name == "detect_ventilatory_anaerobic_threshold":
            res = client.detect_ventilatory_anaerobic_threshold(
                vo2_series_liters_min=args.get("vo2_series_liters_min", []),
                vco2_series_liters_min=args.get("vco2_series_liters_min", [])
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
