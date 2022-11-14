from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.status import *
from django.core.serializers import serialize
import json
from json import JSONDecodeError
from .models import *
from datetime import datetime
from django.db.utils import IntegrityError
from django.core.exceptions import FieldDoesNotExist, FieldError

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
        try:
            body = json.loads(request.body)
            author, created = Author.objects.get_or_create(**body)
            if created:
                author.save()
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author created', 'data': body}), status=HTTP_201_CREATED)
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author already exists'}), status=HTTP_409_CONFLICT)
        except FieldError:
            return HttpResponse(content_type='application/json', content=json.dumps({'detail':'Error, field or fields entered does not exist'}), status=HTTP_400_BAD_REQUEST)
            

    def put(self, request, author_id):
        try:
            author = Author.objects.filter(pk=author_id)
            if not author.exists():
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author not found'}), status=HTTP_404_NOT_FOUND)
            body = json.loads(request.body)
            body['last_update'] = datetime.now()
            author.update(**body)
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Author updated'}), status=HTTP_200_OK)
        except FieldDoesNotExist:            
            return HttpResponse(content_type='application/json',content=json.dumps({'detail': 'field or does not exist'}), status=HTTP_500_INTERNAL_SERVER_ERROR)
        except JSONDecodeError:
            return HttpResponse(content_type='application/json',content=json.dumps({'detail':'Error in JSON'}),status=HTTP_500_INTERNAL_SERVER_ERROR)

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
        try:    
            body = json.loads(request.body)
            category, created = Category.objects.get_or_create(**body)
            if created:
                category.save()
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category created', 'data': body}), status=HTTP_201_CREATED)

            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category already exists'}), status=HTTP_409_CONFLICT)
        except FieldError:
            return HttpResponse(content_type='application/json', content=json.dumps({'detail':'Error, field or fields entered does not exist'}), status=HTTP_400_BAD_REQUEST)

    def put(self, request, category_id):
        try:
            category = Category.objects.filter(pk=category_id)
            if not category.exists():
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category not found'}), status=HTTP_404_NOT_FOUND)
            body = json.loads(request.body)
            body['last_update'] = datetime.now()
            category.update(**body)
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category updated'}), status=HTTP_200_OK)
        except FieldDoesNotExist:
            return HttpResponse(content_type='application/json',content=json.dumps({'detail': 'field does not exist'}), status=HTTP_500_INTERNAL_SERVER_ERROR)
        except JSONDecodeError:
            return HttpResponse(content_type='application/json',content=json.dumps({'detail':'Error in JSON'}),status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, category_id):
        category = Category.objects.filter(pk=category_id)
        if not category.exists():
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category not found'}), status=HTTP_404_NOT_FOUND)
        category.delete()
        return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Category deleted'}), status=HTTP_200_OK)


class BookView(APIView):
    def get(self, request, author_id=None):
        if author_id:
            if Book.objects.filter(author=author_id).exists():
                book_response = Book.objects.filter(author=author_id)
            else:
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Book not found'}), status=HTTP_404_NOT_FOUND)
        else:
            book_response = Book.objects.all()

        book_response = serialize('json', book_response)
        return HttpResponse(content_type='application/json', content=book_response, status=HTTP_200_OK)

    def post(self, request):
        try:
            
            body = json.loads(request.body)
            try:
                body['author'] = Author.objects.get(pk=body['author'])

            except Author.DoesNotExist:
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'no such author'}), status=HTTP_404_NOT_FOUND)
            except KeyError:
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'KeyError Author'}), status=HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                body['category'] = Category.objects.get(pk=body['category'])
            except Category.DoesNotExist:
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'no such category'}), status=HTTP_404_NOT_FOUND)
            except KeyError:
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'KeyError Category'}), status=HTTP_500_INTERNAL_SERVER_ERROR)

            book, created = Book.objects.get_or_create(**body)
            if created:
                book.save()
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Book created'}), status=HTTP_201_CREATED)

            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Book already exists'}), status=HTTP_409_CONFLICT)
        except FieldError:
            return HttpResponse(content_type='application/json', content=json.dumps({'detail':'Error, field or fields entered does not exist'}), status=HTTP_400_BAD_REQUEST)

    def put(self, request, book_id=None):
        try:

            book = Book.objects.filter(pk=book_id)
            if not book.exists():
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Book not found'}), status=HTTP_404_NOT_FOUND)
            body = json.loads(request.body)
            body['last_update'] = datetime.now()
            book.update(**body)
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Book updated'}), status=HTTP_200_OK)
        except IntegrityError:
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'FOREIGN_KEY constraint failed'}), status=HTTP_409_CONFLICT)
        except FieldDoesNotExist:            
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Book has no field '}), status=HTTP_404_NOT_FOUND)
        except JSONDecodeError:
            return HttpResponse(content_type='application/json',content=json.dumps({'detail':'Error in JSON'}),status=HTTP_500_INTERNAL_SERVER_ERROR)    

    def delete(self, request, book_id=None):
        book = Book.objects.filter(pk=book_id)
        if not book.exists():
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Book not found'}), status=HTTP_404_NOT_FOUND)
        book.delete()
        return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Book deleted'}), status=HTTP_200_OK)


class PartnerView(APIView):
    def post(self, request):
        try:
            body = json.loads(request.body)
            partner, created = Partner.objects.get_or_create(**body)
            if created:
                partner.save()
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Partner created'}), status=HTTP_201_CREATED)
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Partner is already exists'}), status=HTTP_409_CONFLICT)
        except FieldError:
            return HttpResponse(content_type='application/json', content=json.dumps({'detail':'Error, field or fields entered does not exist'}), status=HTTP_400_BAD_REQUEST)

    def put(self, request, partner_id):
        try:
            partner = Partner.objects.filter(pk=partner_id)
            if not partner.exists():
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Partner not found'}), status=HTTP_404_NOT_FOUND)
            body = json.loads(request.body)
            body['last_update'] = datetime.now()
            partner.update(**body)
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Partner updated'}), status=HTTP_200_OK)
        except FieldDoesNotExist:            
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Partner has no field '}), status=HTTP_404_NOT_FOUND)

    def delete(self, request, partner_id):
        partner = Partner.objects.filter(pk=partner_id)
        if not partner.exists():
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Partner not found'}), status=HTTP_404_NOT_FOUND)
        partner.delete()
        return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Partner deleted'}), status=HTTP_200_OK)

    def get(self, request, dni=None):
        if dni:
            if Partner.objects.filter(dni__exact=dni).exists():
                partner_response = Partner.objects.filter(dni__exact=dni)
            else:
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Partner not found'}), status=HTTP_404_NOT_FOUND)
        else:
            partner_response = Partner.objects.all()

        partner_response = serialize('json', partner_response)
        return HttpResponse(content_type='application/json', content=partner_response, status=HTTP_200_OK)


class BookLoanView(APIView):
    def post(self, request):
        try:
            body = json.loads(request.body)
            try:
                body['partner'] = Partner.objects.get(pk=body['partner'])
            except Partner.DoesNotExist:
                return HttpResponse(content_type='application/json',content=json.dumps({'detail': 'Partner matching query does not exist'}), status=HTTP_500_INTERNAL_SERVER_ERROR)
            try:
                body['book'] = Book.objects.get(pk=body['book'])
            except Book.DoesNotExist:
                return HttpResponse(content_type='application/json',content=json.dumps({'detail': 'Book matching query does not exist'}), status=HTTP_500_INTERNAL_SERVER_ERROR)

            bookLoan, created = BookLoan.objects.get_or_create(**body)

            if created:
                bookLoan.save()
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'BookLoan created'}), status=HTTP_201_CREATED)
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'BookLoan is already exists'}), status=HTTP_409_CONFLICT)
        except FieldError:
            return HttpResponse(content_type='application/json', content=json.dumps({'detail':'Error, field or fields entered does not exist'}), status=HTTP_400_BAD_REQUEST)
        except KeyError:
            return HttpResponse(content_type='application/json', content=json.dumps({'detail':'KeyError in Book or Partner'}), status=HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return HttpResponse(content_type='application/json',content=json.dumps({'detail':'Error in JSON'}), status=HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, bookLoan_id):
        try:
            bookLoan = BookLoan.objects.filter(pk=bookLoan_id)
            if not bookLoan.exists():
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'BookLoan does not found'}), status=HTTP_404_NOT_FOUND)
            body = json.loads(request.body)
            body['last_update'] = datetime.now()
            # body['status'] = 'terminado'
            bookLoan.update(**body)
            return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'BookLoan updated'}), status=HTTP_200_OK)
        except FieldDoesNotExist:
            return HttpResponse(content_type='application/json',content=json.dumps({'detail':'field name does not exist'}),status=HTTP_500_INTERNAL_SERVER_ERROR)
        except JSONDecodeError:
            return HttpResponse(content_type='application/json',content=json.dumps({'detail':'Error in JSON'}),status=HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, dni=None, status=None):
        partner_id = 0
        if dni:
            if Partner.objects.filter(dni__exact=dni).exists():
                partner_id = Partner.objects.get(dni__exact=dni).pk
                if BookLoan.objects.filter(partner=partner_id).exists():
                    bookLoan_response = BookLoan.objects.filter(
                        partner=partner_id)
                else:
                    return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'BookLoan not found'}), status=HTTP_404_NOT_FOUND)
            else:
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'Partner not found'}), status=HTTP_404_NOT_FOUND)
        elif status:
            if BookLoan.objects.filter(status__iexact=status).exists():
                bookLoan_response = BookLoan.objects.filter(
                    status__iexact=status)
            else:
                return HttpResponse(content_type='application/json', content=json.dumps({'detail': 'BookLoan not found'}), status=HTTP_404_NOT_FOUND)
        else:
            bookLoan_response = BookLoan.objects.all()

        bookLoan_response = serialize('json', bookLoan_response)
        return HttpResponse(content_type='application/json', content=bookLoan_response, status=HTTP_200_OK)
