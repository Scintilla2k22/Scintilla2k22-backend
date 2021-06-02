from django.db.models import query
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import *
class PatientListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def __init__(self):
        query_count = PatientProfile.objects.all().filter(patient_status='A').count()
        self.total = query_count//self.page_size + 1 if query_count%self.page_size else 0

    def get_paginated_response(self, data):
        # total_page = len(data)//self.page_size + 1 if len(data)%self.page_size else 0
        return Response({

            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages' : self.total,
            'results': data
        })