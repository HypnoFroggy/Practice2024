from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Vacancy
def to_database(mydict):
    items = mydict['items']
    for item in items:
        description = f"Требования: {item['snippet']['requirement']} \n Обязанности: {item['snippet']['responsibility']}"
        is_open = item['type']['id'] == 'open'
        address = item['address']['raw'] if item['address'] is not None else ''
        if address is None: address = ''
        name = item['name'] if item['name'] is not None else ''
        department = item['department']['name'] if item['department'] is not None else ''
        if department is None: department = ''
        has_test = item['has_test'] if item['has_test'] is not None else ''
        response_letter_required = item['response_letter_required'] if item['response_letter_required'] is not None else ''
        area = item['area']['name'] if item['area'] is not None else ''
        if area is None: area = ''
        salary = item['salary']['from'] if item['salary'] is not None else 0
        if salary is None: salary = ''
        experience = item['experience']['name'] if item['experience']is not None else ''
        if experience is None: experience = ''
        url = item['url'] if item['url'] is not None else ''
        employer = item['employer']['url'] if item['employer'] is not None else ''
        if employer is None: employer = ''

        Vacancy(
            id=item['id'],
            name=name,
            department=department,
            has_test=has_test,
            response_letter_required=response_letter_required,
            area=area,
            salary=salary,
            description=description,
            experience=experience,
            is_open=is_open,
            address=address,
            url=url,
            employer=employer,
        ).save()

def index(request):
    return render(request, "index.html")

def list(request):
    # получаем из данных запроса POST отправленные через форму данные
    if request.method == 'POST':
        name = request.POST.get("name", "Программист")
        hhru_response = requests.get(f'https://api.hh.ru/vacancies?text={name}&per_page=100').json()
        to_database(hhru_response)

        vacancies = Vacancy.objects.filter(name__contains=name)[:10]
        array = []
        for vacancy in vacancies:
            test = 'Есть' if vacancy.has_test else "Нет"
            array.append([vacancy.name,vacancy.salary,vacancy.experience,test,vacancy.area,vacancy.description])
        print(array)
        return render(request, "list.html",{"name":name,"list":array})
    if request.method == 'GET':
        name = request.GET.get("name", "Программист")
        experience = request.GET.get("experience", "Нет опыта")
        salary = request.GET.get("salary", 0)
        has_test = request.GET.get("has_test", False)
        print(name)
        vacancies = Vacancy.objects.filter(
            name__contains=name,
            experience__contains=experience,
            salary__gte=salary,
            has_test=has_test
        )
        array = []
        for vacancy in vacancies:
            test = 'Есть' if vacancy.has_test else "Нет"
            array.append([vacancy.name, vacancy.salary, vacancy.experience, test, vacancy.area, vacancy.description])
        print(array)
        return render(request, "list.html", {"name": name, "list": array})

def about(request):
    return render(request, "about.html")
