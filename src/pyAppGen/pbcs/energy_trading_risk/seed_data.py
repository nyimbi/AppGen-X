PBC_KEY = "energy_trading_risk"



def seed_plan():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "records": (
            {
                "table": "energy_trading_risk_market_price_curve",
                "code": "PJM-2026-06",
                "payload": {
                    "tenant": "seed",
                    "commodity": "power",
                    "market_hub": "PJM",
                    "delivery_period": "2026-06",
                    "curve_price": 41.5,
                },
            },
            {
                "table": "energy_trading_risk_exposure_limit",
                "code": "PJM-BOOK-1",
                "payload": {
                    "tenant": "seed",
                    "commodity": "power",
                    "market_hub": "PJM",
                    "book": "BOOK-1",
                    "max_net_exposure_mwh": 250.0,
                },
            },
        ),
        "side_effects": (),
    }



def validate_seed_data():
    plan = seed_plan()
    return {
        "ok": plan["ok"] and all(record["table"].startswith(f"{PBC_KEY}_") for record in plan["records"]),
        "pbc": PBC_KEY,
        "side_effects": (),
    }



def smoke_test():
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
