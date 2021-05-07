from django.shortcuts import render, redirect
import requests

# Create your views here.

endpoint = 'http://localhost:5000'


def index(request):
    if request.method == 'GET':
        # req_events = requests.get('http://localhost:5000/events')
        req_stats = requests.get('http://localhost:5000/stats')
        context = {
            # 'input': req_events.text,
            'output': req_stats.text,
        }
        return render(request, 'index.html', context)
    elif request.method == 'POST':
        document = request.FILES['document']
        data = document.read()
        requests.post('http://localhost:5000/events', data)
        return redirect('index')


def reports(request):
    if request.method == 'GET':
        date = request.GET.get('date', None)
        error = request.GET.get('error', None)

        context: dict = {}
        if date != None:
            users_by_date = requests.get('http://localhost:5000/stats/by_date',
                                         {
                                             'date': date
                                         }).json()

            context['date_results']: list = []
            for user in users_by_date['data']:
                percentage = int((user['cant'] / users_by_date['total']) * 100)
                context['date_results'].append({
                    'percentage': percentage,
                    'user': user['user'],
                    'cant': user['cant'],
                    'total': users_by_date['total']
                })
        if error != None:
            errors_by_date = requests.get(
                'http://localhost:5000/stats/by_error', {
                    'error': error
                }).json()

            context['error_results']: list = []
            for date in errors_by_date['data']:
                percentage = int(
                    (date['cant'] / errors_by_date['total']) * 100)
                context['error_results'].append({
                    'percentage':
                    percentage,
                    'date':
                    date['date'],
                    'cant':
                    date['cant'],
                    'total':
                    errors_by_date['total']
                })
        return render(request, 'reports.html', context)
