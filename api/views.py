from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from main.models import Stores, Search
from rate.models import Rate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.forms.models import model_to_dict
from django.core.paginator import Paginator


# from blog.models import Post
# from api.utils import obj_to_post # 시리얼라이저

class ApiSearch(View) :
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs): 
        return super(ApiSearch, self).dispatch(request, *args, **kwargs)
    
    def post(self, request) :
        """
        잔뜩 잔뜩 수정해야하는 부분. 모델도 넣고, 식당별 점수도 매기고, 점수별로 정렬해주고 json 을 돌려줘야함.
        
        search 필드와 식당명이 일치하는 데이터를 돌려준다.
        search 필드 내용을 저장한다.
        """
        r_dict = json.loads(request.body)
        
        if not set(r_dict.keys()) == set(['search']) : 
            print(r_dict.keys())
            print("???")
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400) # status Bad Request

        search=r_dict['search']
        try :
            res_dict = model_to_dict(Stores.objects.get(name=search))
        except :
            res_dict = {'message' : f"STORE {search} NOT IN DATABASE"}

        new_search = { 'content' : search }
        Search.objects.create(**new_search)

        return JsonResponse(data = res_dict, safe = True, status = 200)

class ApiRate(View) :
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs): 
        return super(ApiRate, self).dispatch(request, *args, **kwargs)

    def get(self, request) :
        """
        코멘트 전부다 모아서 list 로 뭉쳐서 반환
        """
        rate_objs = Rate.objects.all()
        res_list = []
        for obj in rate_objs :
            temp = model_to_dict(obj)
            del temp['password']
            res_list.append(temp)
        return JsonResponse(data = { "comments" :res_list }, status = 200)


    def post(self, request) :
        """
        입력 받은 코멘트 정보 저장, 성공 여부 반환
        """
        r_dict = json.loads(request.body)

        if not set(r_dict.keys()) == set(['rating','comment','password']) :
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400)

        try :
            Rate.objects.create(**r_dict)
            success = True
        except :
            success = False
        return JsonResponse(data = {'success' : success}, status = 200)


class ApiRatePage(View) :
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs): 
        return super(ApiRatePage, self).dispatch(request, *args, **kwargs)

    def get(self, request, page) :
        """
        코멘트 전부다 모아서 list 로 뭉쳐서 반환
        """
        rate_objs = Rate.objects.all()
        end_page = (len(rate_objs)+5)//6
        paginator = Paginator(rate_objs, 6)
        objs = paginator.get_page(page)
        res_list = []
        for obj in objs :
            temp = model_to_dict(obj)
            del temp['password']
            res_list.append(temp)
        return JsonResponse(data = { "end_page":end_page, "comments":res_list }, status = 200)

class ApiRateID(View) :
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs): 
        return super(ApiRateID, self).dispatch(request, *args, **kwargs)

    def post(self, request, id_num) :
        """
        id_num 번 코멘트 삭제 요청
        """

        # url id 가 존재하는지 확인
        try :
            m = Rate.objects.get(id=id_num)
        except :
            return HttpResponse("WRONG ID", status = 400)

        r_dict = json.loads(request.body)
        # request 형식 체크
        if not set(r_dict.keys()) == set(['password']) :
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400)

        # 비밀번호 일치 체크해서 삭제
        if m.password == r_dict['password'] :
            m.delete()
            correct = True
        else : correct = False

        return JsonResponse(data = {'delete_success' : correct}, status = 200)


    def put(self, request, id_num) :
        """
        id_num 번 코멘트 수정 요청
        """
        # url id 가 존재하는지 확인
        try :
            m = Rate.objects.get(id=id_num)
        except :
            return HttpResponse("WRONG ID", status = 400)

        r_dict = json.loads(request.body)
        # request 형식 체크
        if not set(r_dict.keys()) == set(['password','comment']) :
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400)

        # 비밀번호 일치 체크해서 수정
        if m.password == r_dict['password'] :
            m.comment = r_dict['comment']
            m.save()
            correct = True
        else : correct = False

        return JsonResponse(data = {'modify_success' : correct}, status = 200)
