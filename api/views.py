from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from main.models import Stores, Search, SearchWithFeedBack
from rate.models import Rate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from api.apps import SearchConfig


# from blog.models import Post
# from api.utils import obj_to_post # 시리얼라이저

class ApiSearch(View) :
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs): 
        return super(ApiSearch, self).dispatch(request, *args, **kwargs)
    
    def post(self, request) :
        """
        로드 되어있는 모델과 식당 정보를 이용
        사용자 인풋 -> 모델 -> 식당정보와 연산해서 정렬 -> 식당정보 top 5 리턴?
        사용자 인풋 db에 저장
        """

        r_dict = json.loads(request.body)
        
        # request json 형식 확인
        if not set(r_dict.keys()) == set(['search']) : 
            print(r_dict.keys())
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400) # status Bad Request

        # 알고리즘 파트
        search=r_dict['search']
   
        # input에 대한 모델 연산, 딕셔너리화
        iscores = SearchConfig.model.predict(search)
        key_list = ['price','cute','wide','corps','satisfaction','modern','ambience','visual','cozy','clean','service','exoticfood','exotictheme','classic','alone']
        input_scores = {}
        for ind, score in enumerate(iscores) :
            input_scores[key_list[ind]] = score
        
        # 스토어 정보 dict 배열
        stores_info = SearchConfig.stores_inf
        # 점수 연산 (지금은 L1 norm)
        for s in stores_info :
            score = 0
            for k in key_list :
                score += abs(s[k] - input_scores[k])
            s['score'] = score
        # 정렬
        sorted_stores = sorted(stores_info, key=(lambda x: x['score']))
        # 상위 5개
        res_dict = {
            "result_tags" : [],
            "main_store" : {
                "name" : '',
                "station" : '',
                "line" : [],
                "tags" : [],
                "walking_time" : ''
            },
            "sub_stores" : []
        }
        main_store = sorted_stores[0]
        res_dict["main_store"]["name"] = main_store['name']
        res_dict["main_store"]["station"] = main_store["station"]
        res_dict["main_store"]["line"] = main_store["lines"].split(',')
        res_dict["main_store"]["walking_time"] = main_store["walking_time"]
        for s in sorted_stores[1:5] :
            res_dict["sub_stores"].append(s['name'])

        print(res_dict)

        # try :
        #     res_dict = model_to_dict(Stores.objects.get(name=search))
        # except :
        #     res_dict = {'message' : f"STORE {search} NOT IN DATABASE"}

        new_search = { 'content' : search }
        Search.objects.create(**new_search)

        return JsonResponse(data = res_dict, safe = True, status = 200)
    
    def put(self, request) :
        """
        평가 받은 리뷰들을 따로 한번 더 저장
        """
        r_dict = json.loads(request.body)
        
        # request json 형식 확인
        if not set(r_dict.keys()) == set(['search', 'thumbs_up']) : 
            print(r_dict.keys())
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400) # status Bad Request

        # db 저장
        try :
            new_search = { 'content' : r_dict['search'], 'thumbs': r_dict['thumbs_up']}
            SearchWithFeedBack.objects.create(**new_search)
            return JsonResponse(data = {'success':True}, safe = True, status = 200)
        except :
            return JsonResponse(data = {'success':False}, safe = True, status = 400)



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
        페이지네이션
        """
        rate_objs = Rate.objects.all()
        end_page = (len(rate_objs)+5)//8
        paginator = Paginator(rate_objs, 8)
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
