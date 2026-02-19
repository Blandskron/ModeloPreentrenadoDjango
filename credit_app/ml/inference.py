import os
import joblib
import numpy as np
from django.conf import settings

LABEL_MAP = {
    0: {"status": "NO_CUMPLE_SOBREENDEUDAMIENTO", "monto_maximo": 0},
    1: {"status": "CUMPLE_PARCIAL_MONTO_BAJO", "monto_maximo": 1_000_000},
    2: {"status": "CUMPLE_MONTO_ALTO", "monto_maximo": 10_000_000},
}

MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_models", "credit_model_xgb.joblib")

_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_credit(ingreso_mensual: float, gastos_mensuales: float, antiguedad_laboral_meses: float):
    model = get_model()
    X = np.array([[ingreso_mensual, gastos_mensuales, antiguedad_laboral_meses]], dtype=float)

    label = int(model.predict(X)[0])

    proba = None
    if hasattr(model, "predict_proba"):
        proba = [float(x) for x in model.predict_proba(X)[0].tolist()]

    return {
        "label": label,
        "decision": LABEL_MAP.get(label, {"status": "DESCONOCIDO", "monto_maximo": None}),
        "proba": proba
    }