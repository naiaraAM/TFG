# pages/views.py
import os
from django.shortcuts import render, get_object_or_404, redirect
from .models import Samples, Comparison
from django.http import HttpResponseBadRequest
import magic
import subprocess

def home(request):
    return render(request, 'pages/home.html', {})

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        uploaded_file = request.FILES['file']
        file_type = magic.from_buffer(uploaded_file.read(1024), mime=True)
        if file_type == 'application/x-dosexec':
            # Save to webapp_uploads directory
            upload_dir = os.path.join(current_dir, '..', '..', 'samples', 'webapp_uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            file_path = os.path.join(upload_dir, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            # Analyze the file
            file_name = uploaded_file.name
            malware_name = 'Not defined'
            source = upload_dir.split('/')[-2]
            category = 'User uploaded'
            script_path = os.path.join(current_dir, '..', '..', 'scripts', 'python', 'x86_disassembler.py')
            first_bytes = subprocess.run([script_path, file_path], capture_output=True, text=True).stdout
            tsv_path = os.path.join(current_dir, '..', '..', 'results_analysis', 'first_bytes_extracted.tsv')
            with open(tsv_path, 'a') as f:
                line = file_name + '\t' + malware_name + '\t' + source + '\t' + category + '\t' + first_bytes
                f.write('\n' + line)
            # Save to database
            db_path = os.path.join(current_dir, '..', '..', 'db', 'TFG.db')
            if not os.path.exists(db_path):
                creation_path = os.path.join(current_dir, '..', '..', 'db', 'creation.py')
                subprocess.run(['python3', creation_path])
            insertion_path = os.path.join(current_dir, '..', '..', 'db', 'insertion.py')
            subprocess.run(['python3', insertion_path])
            comparison_path = os.path.join(current_dir, '..', '..', 'db', 'comparison.py')
            subprocess.run(['python3', comparison_path])
            return redirect('comparison', pk=file_name) # Redirect to comparison page
        else:
            return HttpResponseBadRequest("Invalid file type. Only .exe files are allowed.")
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

def show_original_samples(request):
    sample_data = Samples.objects.filter(category='Original dataset')
    context = {
        "samples": sample_data
    }
    return render(request, 'pages/APT_sample_index.html', context)

def show_user_uploaded_samples(request):
    sample_data = Samples.objects.filter(category='User uploaded')
    context = {
        "samples": sample_data
    }
    return render(request, 'pages/APT_sample_index.html', context)

def comparison(request, pk):
    comparison_data = Comparison.objects.filter(filename1=pk) | Comparison.objects.filter(filename2=pk)
    if comparison_data.exists():
        comparison_values = []
        for entry in comparison_data:
            if entry.filename1 == pk:
                values = {
                    'filename': entry.filename2,
                    'levenshtein': entry.levenshtein,
                    'jaccard': entry.jaccard,
                    'jarowinkler': entry.jarowinkler
                }
            else:
                values = {
                    'filename': entry.filename1,
                    'levenshtein': entry.levenshtein,
                    'jaccard': entry.jaccard,
                    'jarowinkler': entry.jarowinkler
                }
            comparison_values.append(values)
            

        sort = request.GET.get('sort')
        order = request.GET.get('order', 'asc') # Default
        if sort:
            if sort == 'filename':
                if order == 'asc':
                    comparison_values = sorted(comparison_values, key=lambda x: x['filename'])
                else:
                    comparison_values = sorted(comparison_values, key=lambda x: x['filename'], reverse=True)
            elif sort == 'levenshtein':
                if order == 'asc':
                    comparison_values = sorted(comparison_values, key=lambda x: x['levenshtein'])
                else:
                    comparison_values = sorted(comparison_values, key=lambda x: x['levenshtein'], reverse=True)
            elif sort == 'jaccard':
                if order == 'asc':
                    comparison_values = sorted(comparison_values, key=lambda x: x['jaccard'])
                else:
                    comparison_values = sorted(comparison_values, key=lambda x: x['jaccard'], reverse=True)
            elif sort == 'jarowinkler':
                if order == 'asc':
                    comparison_values = sorted(comparison_values, key=lambda x: x['jarowinkler'])
                else:
                    comparison_values = sorted(comparison_values, key=lambda x: x['jarowinkler'], reverse=True)

        context = {
            'pk': pk,
            'comparison': comparison_values,
            'sort': sort,  # Default sort
            'order': order  # Default order
        }
        return render(request, 'pages/comparison.html', context)
    else:
        return HttpResponseBadRequest("File not found in the database.") # 400 Bad Request

    