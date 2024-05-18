# pages/views.py
import os
from django.shortcuts import render, get_object_or_404, redirect
from .models import Samples, Comparison
from django.http import HttpResponseBadRequest
import magic
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import hashlib
from django.db.models import Q


def home(request):
    run_scripts() # Run scripts to initialize/update the database
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
            run_scripts() # Run scripts to update the database
            return redirect('sample_detail', pk=file_name) # Redirect to comparison page
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
    # print nomber of fields in sample_data
    

    comparison_data = Comparison.objects.filter(filename1=pk) | Comparison.objects.filter(filename2=pk)
    if not comparison_data.exists():
        return HttpResponseBadRequest("Data not found in the database.")
    comparison_values = process_comparison_data(comparison_data, pk)
    sort = request.GET.get('sort', 'filename')
    order = request.GET.get('order', 'asc')
    comparison_values = get_sorted_comparison_values(comparison_values, sort, order)

    # Add comparison data to context
    context = {
        "sample": sample_data,
        "comparison": comparison_values,
        "sort": sort,
        "order": order
    }
    create_histogram(pk)
    return render(request, 'pages/APT_sample_detail.html', context)

def heatmaps(request):
    create_heatmap()
    return render(request, 'pages/heatmaps.html')

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

def get_sorted_comparison_values(comparison_values, sort, order):
    if sort == 'filename':
        key_func = lambda x: x['filename']
    elif sort == 'levenshtein':
        key_func = lambda x: x['levenshtein']
    elif sort == 'jaccard':
        key_func = lambda x: x['jaccard']
    elif sort == 'jarowinkler':
        key_func = lambda x: x['jarowinkler']
    elif sort == 'arithmetic_mean':
        key_func = lambda x: x['arithmetic_mean']
    elif sort == 'geometric_mean':
        key_func = lambda x: x['geometric_mean']
    else:
        key_func = None  # Default if no sort is specified

    if key_func:
        reverse = True if order == 'desc' else False
        return sorted(comparison_values, key=key_func, reverse=reverse)
    else:
        return comparison_values  # Return unchanged if no sort is specified

def get_comparison_data_by_pk(pk):
    comparison_data = Comparison.objects.filter(filename1=pk) | Comparison.objects.filter(filename2=pk)
    return comparison_data

def get_arithmetic_mean(comparison_values):
    values = {
        'levenshtein': comparison_values['levenshtein'],
        'jaccard': comparison_values['jaccard'],
        'jarowinkler': comparison_values['jarowinkler']
    }
    return (values['levenshtein'] + values['jaccard'] + values['jarowinkler']) / 3

def get_geometric_mean(comparison_values):
    values = {
        'levenshtein': comparison_values['levenshtein'],
        'jaccard': comparison_values['jaccard'],
        'jarowinkler': comparison_values['jarowinkler']
    }
    return (float(values['levenshtein']) * float(values['jaccard']) * float(values['jarowinkler'])) ** (1/3)

def process_comparison_data(comparison_data, pk):
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

        # Calculate means
        arithmetic_mean = get_arithmetic_mean(values)

        # Redondear a dos decimales, si no tiene 2, rellevar con 0
        values['arithmetic_mean'] = round(arithmetic_mean, 2)
        values['arithmetic_mean'] = "{:.2f}".format(round(arithmetic_mean, 2))

        geometric_mean = get_geometric_mean(values)
        values['geometric_mean'] = "{:.2f}".format(round(geometric_mean, 2))

        comparison_values.append(values)

    return comparison_values

def histogram_data(pk):
    comparison_data = get_comparison_data_by_pk(pk)
    comparison_values = process_comparison_data(comparison_data, pk)
    arthmetic_mean = [entry['arithmetic_mean'] for entry in comparison_values]
    geometric_mean = [entry['geometric_mean'] for entry in comparison_values]

    return arthmetic_mean, geometric_mean

def create_histogram(pk):
    # Retreive data for histogram
    arthmetic_mean, geometric_mean = histogram_data(pk)

    # Shorten the primary key for the plot title
    short_pk = pk[:7] + '...' + pk[-7:]
    bins = [i/10 for i in range(11)]  # From 0 to 1 in 0.1 increments
    # Images path
    current_dir = os.path.dirname(os.path.realpath(__file__))
    images_dir = os.path.join(current_dir, '..', 'static', 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    # To float point
    arthmetic_mean = np.array([float(i) for i in arthmetic_mean])
    geometric_mean = np.array([float(i) for i in geometric_mean])
    
    # Histogram for arithmetic mean
    plt.figure(figsize=(10, 6))
    plt.hist(arthmetic_mean, color='skyblue', edgecolor='black', bins=bins)
    plt.title(f'Arithmetic Mean of Comparison Values for {short_pk}')
    plt.xlabel('Arithmetic Mean')
    plt.ylabel('Number of Samples')
    
    # Set axis limits and ticks
    plt.xlim(0, 1)
    plt.ylim(0, max(10, plt.gca().get_ylim()[1]))
    plt.xticks(np.arange(0, 1.1, 0.1))
    
    arithmetic_histogram_path = os.path.join(images_dir, f'{pk}_arithmetic_histogram.png')
    plt.savefig(arithmetic_histogram_path)
    plt.close()
    
    # Histogram for geometric mean
    plt.figure(figsize=(10, 6))
    plt.hist(geometric_mean, color='violet', edgecolor='black', bins=bins)
    plt.title(f'Geometric Mean of Comparison Values for {short_pk}')
    plt.xlabel('Geometric Mean')
    plt.ylabel('Number of Samples')
    
    # Set axis limits and ticks
    plt.xlim(0, 1)
    plt.ylim(0, max(10, plt.gca().get_ylim()[1]))
    plt.xticks(np.arange(0, 1.1, 0.1))
    
    geometric_histogram_path = os.path.join(images_dir, f'{pk}_geometric_histogram.png')
    plt.savefig(geometric_histogram_path)
    plt.close()


def run_scripts():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    process_malware_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'scripts', 'bash', 'process_basic_info.sh'))
    subprocess.run([process_malware_path], shell=True)
    compare_malware_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'scripts', 'python', 'compare.py'))
    subprocess.run(['python3', compare_malware_path])
    creation_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'db', 'creation.py'))
    subprocess.run(['python3', creation_path])
    insertion_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'db', 'insertion.py'))
    subprocess.run(['python3', insertion_path])
    comparison_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'db', 'comparison.py'))
    subprocess.run(['python3', comparison_path])

def generate_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def load_previous_hash(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read().strip()

def save_current_hash(file_path, hash_value):
    with open(file_path, 'w') as f:
        f.write(hash_value)

def check_hash(filenames):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    hash_file_path = os.path.join(current_dir, '..', 'static', 'samples_hash.txt')
    filenames = list(Samples.objects.values_list('sha_256', flat=True))
    combined_filenames = ''.join(filenames)
    current_hash = generate_hash(combined_filenames)
    previous_hash = load_previous_hash(hash_file_path)
    save_current_hash(hash_file_path, current_hash)
    return current_hash == previous_hash


def create_heatmap():
    filenames = list(Samples.objects.values_list('sha_256', flat=True))
    dataset_size = len(filenames)
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    images_dir = os.path.join(current_dir, '..', 'static', 'images')
    
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    if not check_hash(filenames):
        heatmap_values_arithmetic = np.zeros((dataset_size, dataset_size))
        heatmap_values_geometric = np.zeros((dataset_size, dataset_size))
        
        for i in range(dataset_size):
            filename_1 = filenames[i]
            for j in range(dataset_size):
                filename_2 = filenames[j]
                if i == j:
                    heatmap_values_arithmetic[i, j] = 1
                    heatmap_values_geometric[i, j] = 1
                else:
                    pair_data = Comparison.objects.filter(
                        Q(filename1=filename_1, filename2=filename_2) |
                        Q(filename1=filename_2, filename2=filename_1)
                    )
                    heatmap_values_arithmetic[i, j] = get_arithmetic_mean(pair_data.values()[0])
                    heatmap_values_geometric[i, j] = get_geometric_mean(pair_data.values()[0])

        # Save the heatmaps with colorbars
        plt.figure()
        plt.title("Heatmap of arithmetic values")
        plt.imshow(heatmap_values_arithmetic, aspect='auto', cmap='viridis')
        plt.colorbar()  # Add colorbar
        heatmap_arithmetic_path = os.path.join(images_dir, 'heatmap_arithmetic.png')
        plt.savefig(heatmap_arithmetic_path)
        plt.close()

        plt.figure()
        plt.title("Heatmap of geometric values")
        plt.imshow(heatmap_values_geometric, aspect='auto', cmap='viridis')
        plt.colorbar()  # Add colorbar
        heatmap_geometric_path = os.path.join(images_dir, 'heatmap_geometric.png')
        plt.savefig(heatmap_geometric_path)
        plt.close()