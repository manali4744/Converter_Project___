from django.shortcuts import render
from django.views import View
from PyPDF2 import PdfReader
import PyPDF2
import io
from docx import Document
from django.http import FileResponse
import json
from django.http import JsonResponse
import pandas as pd

# Create your views here.
class Index(View):
    def get(self,request):
        return render(request,'index.html')

class ConvertToDocx(View):
    def get(self,request):
        req = json.loads(request.body)
        print(req["pdf_file"])
        pdf_file = open(req["pdf_file"],'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        document = Document()
        number_of_pages = len(pdf_reader.pages)
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            document.add_paragraph(text)

        docx_file = io.BytesIO()
        document.save(docx_file)

        docx_file.seek(0)
        converted_file_name = req["pdf_file"].split(".")[0]
        print("converted_file_name",converted_file_name)
        file_path = f'{converted_file_name}_converted_file.docx'  # Update with your desired file path
        with open(file_path, 'wb') as f:
            f.write(docx_file.read())
        pdf_file.close()
        response = FileResponse(docx_file, as_attachment=True, filename=file_path)
        print("response",response)
        if response:
            return JsonResponse({"status":"success","data":"Created docx file successfully!!!!"})
        else:
            return JsonResponse({"status":"fail","data":"Not created docx file!!!!"})
        
class ConvertToExcel(View):
    def get(self,request):
        req = json.loads(request.body)
        print(req["pdf_file"])
        pdf_file = open(req["pdf_file"],'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        excel_data = pd.DataFrame()
        for page in pdf_reader.pages:
            # pdf_page = pdf_reader.pages[page]
            page_text = page.extract_text()
            rows = page_text.split('\n')
            rows = [row for row in rows if row]
            page_data = pd.DataFrame(rows)
            page_data = page_data[0].str.split('\t', expand=True)
            excel_data = pd.concat([excel_data, page_data])
        converted_file_name = req["pdf_file"].split(".")[0]
        excel_data.to_excel(f'{converted_file_name}_converted.xlsx', index=False)
        file_path = f'{converted_file_name}_converted_file.xlsx'
        with open(file_path, 'wb') as f:
            f.write(excel_data.read())
        pdf_file.close()
        response = FileResponse(excel_data, as_attachment=True, filename=file_path)
        print("response",response)
        if response:
            return JsonResponse({"status":"success","data":"Created docx file successfully!!!!"})
        else:
            return JsonResponse({"status":"fail","data":"Not created docx file!!!!"})
        