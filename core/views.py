from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.status import *
from django.core.serializers import serialize
import json
from .models import *
from datetime import datetime

# Create your views here.


class AuthorView(APIView):
    def get(self, request, last_name=None):
        if last_name:
            if Author.objects.filter(last_name__iexact=last_name).exists():
                author_response = Author.objects.filter(
                    last_name__iexact=last_name)
            else:
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author not found'}), status=HTTP_404_NOT_FOUND)
        else:
            author_response = Author.objects.all()

        author_response = serialize('json', author_response)
        return HttpResponse(content_type='application/json', content=author_response, status=HTTP_200_OK)

    def post(self, request):
        body = json.loads(request.body)
        author, created = Author.objects.get_or_create(**body)
        if created:
            author.save()
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author created', 'data': body}), status=HTTP_201_CREATED)
        return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author already exists'}), status=HTTP_409_CONFLICT)

    def put(self, request, author_id):
        author = Author.objects.filter(pk=author_id)
        if not author.exists():
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author not found'}), status=HTTP_404_NOT_FOUND)
        body = json.loads(request.body)
        body['last_update'] = datetime.now()
        author.update(**body)
        return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author updated'}), status=HTTP_200_OK)

    def delete(self, request, author_id):
        author = Author.objects.filter(pk=author_id)
        if not author.exists():
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author not found'}), status=HTTP_404_NOT_FOUND)
        author.delete()
        return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author deleted'}), status=HTTP_200_OK)


class CategoryView(APIView):

    def get(self, request, name=None):
        if name:
            if Category.objects.filter(name__iexact=name).exists():
                category_response = Category.objects.filter(name__iexact=name)
            else:
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category not found'}), status=HTTP_404_NOT_FOUND)
        else:
            category_response = Category.objects.all()

        category_response = serialize('json', category_response)
        return HttpResponse(content_type='application/json', content=category_response, status=HTTP_200_OK)
    
    def post(self, request):
        body=json.loads(request.body)
        category, created = Category.objects.get_or_create(**body)
        if created:
            category.save()
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category created','data':body}), status=HTTP_201_CREATED)
        
        return HttpResponse(content_type='application/json',content=json.dumps({'detail':'Category already exists'}), status=HTTP_409_CONFLICT)
    
    def put(self,request, category_id):
        category = Category.objects.filter(pk=category_id)
        if not category.exists():
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category not found'}), status=HTTP_404_NOT_FOUND)
        body = json.loads(request.body)
        body['last_update'] = datetime.now()
        category.update(**body)
        return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category updated'}), status=HTTP_200_OK)
    
    def delete(self, request, category_id):
        category = Category.objects.filter(pk=category_id)
        if not category.exists():
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category not found'}), status=HTTP_404_NOT_FOUND)
        category.delete()
        return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category deleted'}), status=HTTP_200_OK)
    
    
        
            
        
