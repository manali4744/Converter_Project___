from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('index',Index.as_view(),name='index'),
    path('convert_pdf_to_docx',ConvertToDocx.as_view(),name='pdftoword'),
    path('convert_pdf_to_excel',ConvertToExcel.as_view(),name='pdftoexcel')
]