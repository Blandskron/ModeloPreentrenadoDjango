import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .ml.inference import predict_credit
from .models import CreditRequest

@require_http_methods(["GET", "POST"])
def dashboard_view(request):
    if request.method == "GET":
        return render(request, "credit_app/dashboard.html")

    # Datos del formulario (NO pasan por el modelo: name/email)
    client_name = (request.POST.get("client_name") or "").strip()
    client_email = (request.POST.get("client_email") or "").strip()

    # Datos que sí van al modelo
    ingreso = float(request.POST.get("ingreso_mensual", "0"))
    gastos = float(request.POST.get("gastos_mensuales", "0"))
    antig  = float(request.POST.get("antiguedad_laboral_meses", "0"))

    result = predict_credit(ingreso, gastos, antig)

    # Guardar en DB
    CreditRequest.objects.create(
        client_name=client_name,
        client_email=client_email,
        ingreso_mensual=ingreso,
        gastos_mensuales=gastos,
        antiguedad_laboral_meses=antig,
        label=int(result["label"]),
        status=str(result["decision"]["status"]),
        monto_maximo=int(result["decision"]["monto_maximo"]),
        proba_json=json.dumps(result["proba"]) if result.get("proba") is not None else None,
    )

    context = {
        "input": {
            "client_name": client_name,
            "client_email": client_email,
            "ingreso_mensual": ingreso,
            "gastos_mensuales": gastos,
            "antiguedad_laboral_meses": antig,
        },
        "result": result,
    }
    return render(request, "credit_app/result.html", context)