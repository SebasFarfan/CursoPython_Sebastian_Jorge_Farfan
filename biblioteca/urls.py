"""biblioteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # --------------------------------------------------------------------------------------
    # rutas para autores
    # listar todos los autores y registrar autores
    path('authors/',AuthorView.as_view(), name='authors'),    
    # obtener autor por apellido
    path('authors/<str:last_name>', AuthorView.as_view(), name='authors'),    
    # modificar autores
    path('authors/update/<int:author_id>', AuthorView.as_view(), name='update'),    
    # eliminar autores
    path('authors/delete/<int:author_id>', AuthorView.as_view(), name='delete'),
    
    # --------------------------------------------------------------------------------------
    # rutas para categorias
    # obtener todas las categorias    
    path('categories/', CategoryView.as_view(), name='categories'),
    # obtener categorias por nombre
    path('categories/<str:name>',CategoryView.as_view(), name='categories'),
    # modificar categorias
    path('categories/update/<int:category_id>', CategoryView.as_view(), name='update_category'),
    # eliminar categorias
    path('categories/delete/<int:category_id>', CategoryView.as_view(),name='delete_category'),
    
    # --------------------------------------------------------------------------------------
    # rutas para libros
    # obtener todos los libros
    path('books/', BookView.as_view(), name='books'),
    # obtener libros por autor. por id_autor.
    path('books/<int:author_id>', BookView.as_view(), name='books'),
    # modificar libros
    path('books/update/<int:book_id>', BookView.as_view(), name='update_book'),
    # eliminar libros
    path('books/delete/<int:book_id>', BookView.as_view(), name='delete_book'),
    
    # --------------------------------------------------------------------------------------
    # rutas para socios
    # obtener todos los socios y registrar socios.
    path('partner/', PartnerView.as_view(), name='partner'),
    # obtener socios por dni
    path('partner/<str:dni>', PartnerView.as_view(), name='partner'),
    # modificar socios
    path('partner/update/<int:partner_id>', PartnerView.as_view(), name='update_partner'),
    # eliminar socios
    path('partner/delete/<int:partner_id>', PartnerView.as_view(), name='delete_partner'),
    
    # --------------------------------------------------------------------------------------
    # rutas para prestamos
    # obtener todos los prestamos y registrar prestamos
    path('bookloan/', BookLoanView.as_view(), name='bookloan'),
    # obtener prestamo por dni de socio
    path('bookloan/dni/<str:dni>', BookLoanView.as_view(), name='bookloan'),
    # obtener prestamos por estado 
    path('bookloan/status/<str:status>', BookLoanView.as_view(), name='bookloan'),
    # modificar estado del prestamo
    path('bookloan/update/<int:bookLoan_id>', BookLoanView.as_view(), name='update_bookLoan'),
    
]
