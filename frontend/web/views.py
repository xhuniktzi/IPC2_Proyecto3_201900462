from django.shortcuts import render, redirect
import requests

# Create your views here.

endpoint = 'http://localhost:5000'


def index(request):
    if request.method == 'GET':
        req_events = requests.get('http://localhost:5000/events')
        req_stats = requests.get('http://localhost:5000/stats')
        context = {
            'input': req_events.text,
            'output': req_stats.text,
        }
        return render(request, 'index.html', context)
    elif request.method == 'POST':
        document = request.FILES['document']
        data = document.read()
        requests.post('http://localhost:5000/events', data)
        return redirect('index')


def reports(request):
    return render(request, 'reports.html')
