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
    path('authors/',AuthorView.as_view(), name='authors'),
    path('authors/<str:last_name>', AuthorView.as_view(), name='authors'),
    path('authors/update/<int:author_id>', AuthorView.as_view(), name='update'),
    path('authors/delete/<int:author_id>', AuthorView.as_view(), name='delete'),
    
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/<str:name>',CategoryView.as_view(), name='categories'),
    path('categories/update/<int:category_id>', CategoryView.as_view(), name='update_category'),
    path('categories/delete/<int:category_id>', CategoryView.as_view(),name='delete_category'),
    
    path('books/', BookView.as_view(), name='books'),
    path('books/<int:author_id>', BookView.as_view(), name='books'),
    path('books/update/<int:book_id>', BookView.as_view(), name='update_book'),
    path('books/delete/<int:book_id>', BookView.as_view(), name='delete_book'),
    
    path('partner/', PartnerView.as_view(), name='partner'),
    path('partner/<str:dni>', PartnerView.as_view(), name='partner'),
    path('partner/update/<int:partner_id>', PartnerView.as_view(), name='update_partner'),
    path('partner/delete/<int:partner_id>', PartnerView.as_view(), name='delete_partner'),
    
    path('bookloan/', BookLoanView.as_view(), name='bookloan'),
    path('bookloan/dni/<str:dni>', BookLoanView.as_view(), name='bookloan'),
    path('bookloan/status/<str:status>', BookLoanView.as_view(), name='bookloan'),
    path('bookloan/update/<int:bookLoan_id>', BookLoanView.as_view(), name='update_bookLoan'),
    
]
