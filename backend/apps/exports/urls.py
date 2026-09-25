from django.urls import path
from .views import GenerateQRCodeView, ExportPDFCVView

app_name = 'exports'

urlpatterns = [
    path('qrcode/<str:username>/', GenerateQRCodeView.as_view(), name='qrcode'),
    path('cv/<str:username>/', ExportPDFCVView.as_view(), name='export_cv_pdf'),
]
