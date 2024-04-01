# pages/views.py
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Samples

def home(request):
    return render(request, 'pages/home.html', {})

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        upload_dir = '/home/chispitas/Documents/TFG/samples/webapp_uploads/'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        # Redirect to show the file analysis result
        return render(request, 'pages/upload_success.html', {'file_name': uploaded_file.name})
    else:
        return render(request, 'pages/upload_file.html')
    
def samples_index(request):
    samples_data = Samples.objects.all()
    context = {
        "samples": samples_data
    }
    return render(request, 'pages/APT_sample_index.html', context)

def sample_detail(request, pk):
    sample_data = get_object_or_404(Samples, pk=pk)
    context = {
        "sample": sample_data
    }
    return render(request, 'pages/APT_sample_detail.html', context)