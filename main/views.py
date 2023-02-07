# Create your views here.

from django.views.generic import TemplateView
from django.http import HttpResponse
import csv
import pandas as pd
from main.models import Stores

class MainView(TemplateView) :
    template_name = 'main.html'

class SearchView(TemplateView) :
    template_name = 'search.html'

class ResultView(TemplateView) :
    template_name = 'result.html'

def csv_to_db(request) :
    # 기존 내용 삭제
    delatable_objects = Stores.objects.all()[:]
    for m in delatable_objects:
        m.delete()
    print("***** 테이블 삭제 완 *****")

    df = pd.read_csv('Stores_update.csv', index_col=[0])
    dl = df.to_dict('records')
    for di in dl :
        Stores.objects.create(**di)
        print(f"{di['name']} *** added")
    return HttpResponse('db_in_success')
