from .slice_app import build_models_contract


def model_contracts():
    return build_models_contract()["models"]


def build_models():
    return build_models_contract()
