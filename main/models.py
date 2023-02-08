from django.db import models
from django.utils.timezone import datetime

class Stores(models.Model) :
    # category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank = True, null = True) # 연결된 카테고리가 사라지면 null 로 변경
    # tags = models.ManyToManyField('Tag', blank = True) # blank 랑 null 은 False 가 디폴트

    name = models.CharField('NAME', max_length=50, unique=True) # 식당이름, 비어있을수없음
    category = models.CharField('CATEGORY', max_length=50, blank=True, null=True) # 카테고리
    address = models.CharField('ADDRESS', max_length=100) # 주소지, 비어있을수없음
    star = models.FloatField('STAR', blank=True, null=True) # 평균 별점
    comment = models.CharField('COMMENT', max_length=150, blank=True, null=True) # 한줄요약
    naver_services = models.CharField('SERVICES', max_length=150, blank=True, null=True) # 네이버서비스 str
    station = models.CharField('STATION', max_length=20, blank=True, null=True) # 지하철역
    out = models.CharField('OUT', max_length=20, blank=True, null=True) # 몇출
    meter = models.FloatField('METER', blank=True, null=True) # 출구부터 거리
    lines = models.CharField('LINES', max_length=100, blank=True, null=True) # 호선
    walking_time = models.FloatField('WALKING_TIME', blank=True, null=True) # 걷는시간

    # tags = models.CharField('TAGS', max_length=300, blank=True, null=True) # 태그

    def __str__(self) :
        return self.name

class Search(models.Model) :
    content = models.CharField('CONTENT', max_length=200) # 검색어, 비어있을수없음
    create_date = models.DateTimeField('CREATE_DATE', default=datetime.now) # 생성날짜

    @property
    def short_content(self) :
        return self.content[:10]

    def __str__(self) :
        return self.short_content

class SearchWithFeedBack(models.Model) :
    content = models.CharField('CONTENT', max_length=200) # 검색어, 비어있을수없음
    create_date = models.DateTimeField('CREATE_DATE', default=datetime.now) # 생성날짜
    thumbs = models.BooleanField('THUMBS') # 비어있을수없음

    @property
    def short_content(self) :
        return self.content[:10]

    def __str__(self) :
        return self.short_content