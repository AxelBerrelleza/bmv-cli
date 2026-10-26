"""Test fixtures for API responses - DataBursatil v2 API."""


def prices_response():
    """Mock response from /v2/cotizaciones endpoint."""
    return {
        "GFNORTEO": {
            "bmv": {
                "u": 213.5,
                "p": 213.46,
                "a": 207.91,
                "x": 214.69,
                "n": 206.89,
                "c": 2.67,
                "m": 5.55,
                "v": 8081217.0,
                "o": 25245.0,
                "i": 1710147325.48,
                "f": "2026-10-23 14:00:00",
            },
            "biva": {
                "u": 213.5,
                "p": 213.46,
                "a": 207.91,
                "x": 214.43,
                "n": 207.49,
                "c": 2.68,
                "m": 5.59,
                "v": 1190223.0,
                "o": 6307.0,
                "i": 252457560.01,
                "f": "2026-10-23 14:05:00",
            },
        },
        "WALMEX*": {
            "bmv": {
                "u": 50.73,
                "p": 50.77,
                "a": 50.34,
                "x": 50.94,
                "n": 50.01,
                "c": 0.85,
                "m": 0.43,
                "v": 8904568.0,
                "o": 18587.0,
                "i": 451685201.71,
                "f": "2026-10-23 14:00:00",
            },
            "biva": {
                "u": 50.88,
                "p": 50.77,
                "a": 50.34,
                "x": 50.94,
                "n": 50.12,
                "c": 1.07,
                "m": 0.53,
                "v": 1714520.0,
                "o": 6643.0,
                "i": 86940490.91,
                "f": "2026-10-23 14:05:00",
            },
        },
    }


def currencies_response():
    """Mock response from /v2/divisas endpoint."""
    return {
        "AUDUSD": {"u": 0.6903, "c": -0.1, "m": -0.0007},
        "CADMXN": {"u": 12.3493, "c": 0.16, "m": 0.0196},
        "CHFMXN": {"u": 21.6778, "c": 0.3, "m": 0.0659},
        "EURMXN": {"u": 19.9913, "c": 0.42, "m": 0.0833},
        "EURUSD": {"u": 1.1408, "c": 0.34, "m": 0.0039},
        "GBPMXN": {"u": 23.1671, "c": 0.29, "m": 0.0671},
        "GBPUSD": {"u": 1.3224, "c": 0.24, "m": 0.0031},
        "USDCAD": {"u": 1.4181, "c": -0.14, "m": -0.002},
        "USDJPY": {"u": 161.55, "c": -0.15, "m": -0.24},
        "USDMXN": {"u": 17.5147, "c": 0.03, "m": 0.0047},
        "t": "2026-06-26 04:01:00",
    }


def credits_response():
    """Mock response from /v2/creditos endpoint."""
    return {"disponibles": 249421}


def emisoras_response():
    """Mock response from /v2/emisoras endpoint."""
    return {
        "WALMEX": {
            "*": {
                "razon_social": "WAL - MART DE MEXICO, S.A.B. DE C.V.",
                "isin": "MX01WA000038",
                "bolsa": "BMV",
                "tipo_valor_descripcion": "ACCIONES DE EMPRESAS COMERCIALES, INDUSTRIALES Y DE SERVICIOS",
                "tipo_valor_id": "1",
                "estatus": "ACTIVA",
                "acciones_en_circulacion": 17461402631,
                "rango_historicos": "2010-01-05 a 2026-10-23",
                "rango_financieros": "1T_2017, 1T_2018, 1T_2019, 1T_2020, 1T_2021, 1T_2022, 1T_2023, 1T_2024, 1T_2025, 1T_2026",
                "dividendos": {
                    "reciente": {
                        "2025-12-17": {
                            "pago": 0.85,
                            "tipo": "DIVIDENDO EN EFECTIVO",
                            "divisa": "MXN",
                            "fechaexcupon": "2025-12-16",
                        }
                    },
                    "historico": {
                        "2021-11-24": {"pago": 0.81, "tipo": "DIVIDENDO EN EFECTIVO"},
                        "2021-12-28": {"pago": 0.82, "tipo": "DIVIDENDO EN EFECTIVO"},
                        "2022-11-22": {"pago": 0.85, "tipo": "DIVIDENDO EN EFECTIVO"},
                        "2022-12-27": {"pago": 0.86, "tipo": "DIVIDENDO EN EFECTIVO"},
                        "2023-04-11": {"pago": 0.75, "tipo": "DIVIDENDO EN EFECTIVO"},
                        "2023-11-29": {"pago": 0.97, "tipo": "DIVIDENDO EN EFECTIVO"},
                        "2023-12-06": {"pago": 0.97, "tipo": "DIVIDENDO EN EFECTIVO"},
                        "2024-11-12": {"pago": 0.59, "tipo": "DIVIDENDO EN EFECTIVO"},
                        "2024-12-10": {"pago": 1.09, "tipo": "DIVIDENDO EN EFECTIVO"},
                        "2025-11-19": {"pago": 0.84, "tipo": "DIVIDENDO EN EFECTIVO"},
                        "2025-12-17": {"pago": 0.85, "tipo": "DIVIDENDO EN EFECTIVO"},
                    },
                },
            }
        }
    }


def emisoras_error_response():
    """Mock error response from /v2/emisoras endpoint."""
    return {
        "Error": "La busqueda no arrojo ningun resultado. ¿Dudas? Revisa la documentacion: https://databursatil.com/docs.html"
    }
