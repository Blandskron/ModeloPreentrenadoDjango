from django.db import models

class CreditRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    client_name = models.CharField(max_length=120)
    client_email = models.EmailField(max_length=254)

    ingreso_mensual = models.FloatField()
    gastos_mensuales = models.FloatField()
    antiguedad_laboral_meses = models.FloatField()

    label = models.IntegerField()
    status = models.CharField(max_length=80)
    monto_maximo = models.BigIntegerField()

    # Guardamos probas como texto JSON (opcional, pero útil)
    proba_json = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client_name} - {self.status} - {self.created_at:%Y-%m-%d %H:%M}"