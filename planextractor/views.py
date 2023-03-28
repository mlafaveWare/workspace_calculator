import os
import PyPDF2
import pyRevit
import ezdxf
from django.views.generic.edit import FormView
from myapp.forms import FileUploadForm
from myapp.models import Dimension
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from .models import FloorPlan
from .serializers import FloorPlanSerializer

class FileUploadView(FormView):
    template_name = 'file_upload.html'
    form_class = FileUploadForm
    success_url = '/'

    def form_valid(self, form):
        file = form.cleaned_data['file']
        file_path = os.path.join('media', file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        file_type = os.path.splitext(file.name)[1][1:].lower()
        length = width = height = multiplier = 0
        if file_type == 'pdf':
            pdf_reader = PyPDF2.PdfFileReader(open(file_path, 'rb'))
            page = pdf_reader.getPage(0)
            length, width = page.mediaBox.getWidth(), page.mediaBox.getHeight()
        elif file_type == 'rvt':
            pyRevit.open(file_path)
            length, width, height = pyRevit.get_size()
        elif file_type == 'dwg':
            doc = ezdxf.readfile(file_path)
            modelspace = doc.modelspace()
            bbox = modelspace.get_bounding_box()
            length, width = bbox.width, bbox.height
        multiplier = form.cleaned_data['multiplier']
        dimension = Dimension(file_type=file_type, file_path=file_path, length=length, width=width, height=height, multiplier=multiplier)
        dimension.save()
        return super().form_valid(form)


class UploadPlanView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        file = request.FILES['file']
        name = file.name
        dimensions = extract_dimensions(file)
        multiplier = float(request.POST.get('multiplier', 1.45))
        area = dimensions['width'] * dimensions['height'] * multiplier
        plan = FloorPlan(name=name, file=file, area=area)
        plan.save()
        serializer = FloorPlanSerializer(plan)
        return Response(serializer.data)
