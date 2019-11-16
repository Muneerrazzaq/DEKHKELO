from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pandas as pd
import sqlalchemy
import psycopg2
import json
from .forms import ContactForm
from .models import Contact
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, get_connection
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.

# here item am trying my scrap data to be shown

def daraz_data(keyword):  # 0 for search and 1 for category

    df = pd.read_csv('2019-11-14 Compare Data.csv')

    li = df.MainCategory.unique()

    # this is to complete the keyword if babies then babies & toys
    for i in range(len(li)):
        if li[i].find(keyword) != -1:
            keyword = li[i]

    if keyword not in li:
        df = df[df['brandName'].str.contains(keyword)]
    else:
        df = df[df['MainCategory'].str.contains(keyword)]
    length = len(df)

    items = df.to_dict()

    data = 0

    main_category = []
    main_sub_category = []
    brand_name = []
    name = []
    image = []
    link = []
    price_after_discount = []
    price_before_discount = []
    discount = []
    rating_score = []
    reviews = []
    location = []
    compareision = []
    price_old = []
    discount_old = []
    stock = []
    oldOrigianlPrice = []

    for item in items["image"]:
        main_category.append(items["MainCategory"][item])
        main_sub_category.append(items["SubCategory"][item])
        brand_name.append(items["brandName"][item])
        name.append(items["name"][item])
        image.append(items["image"][item])
        link.append(items["link"][item])
        price_after_discount.append(items["price"][item])
        price_before_discount.append(items["originalPrice"][item])
        discount.append(items["discount"][item])
        rating_score.append(items["ratingScore"][item])
        reviews.append(items["review"][item])
        location.append(items["location"][item])
        compareision.append(items["Compareision"][item])
        price_old.append(items["old price"][item])
        discount_old.append(items["old discount"][item])
        stock.append(items["inStock"][item])
        oldOrigianlPrice.append(items["old OrigianlPrice"][item])
        data = zip(

            main_category,
            main_sub_category,
            brand_name,
            name,
            image,
            link,
            price_after_discount,
            price_before_discount,
            discount,
            rating_score,
            reviews,
            location,
            compareision,
            price_old,
            discount_old,
            stock,
            oldOrigianlPrice,
        )
    return data, length, keyword


def index(request):
    return render(request, "DarazTemplates/index.html")


def new_index(request):
    if request.method == "GET":
        if request.GET.get('search'):
            keyword = request.GET.get('search')
            data, length, keyword = daraz_data(keyword)
            paginator = Paginator(list(data), 20)

            page = request.GET.get('page')

            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            return render(request, "DarazTemplates/new_index.html", {'data': data, 'keyword': keyword, 'length': length})
        else:
            return render(request, "DarazTemplates/new_index.html")
    elif request.method == "POST":
        keyword = str(request.POST.get("SearchItem"))
        data, length, keyword = daraz_data(keyword)
        if data != 0:
            paginator = Paginator(list(data), 20)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            return render(request, "DarazTemplates/new_index.html", {'data': data, 'keyword': keyword, 'length': length})
        else:
            return render(request, "DarazTemplates/new_index.html", {'keyword': keyword, 'length': length})


def brands(request):
    if request.method == "GET":
        if request.GET.get('search'):
            keyword = request.GET.get('search')
            data, length, keyword = daraz_data(keyword)
            print(request.GET)
            paginator = Paginator(list(data), 12)

            page = request.GET.get('page')

            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            return render(request, "DarazTemplates/brands.html", {'data': data, 'keyword': keyword, 'length': length})
        else:
            return render(request, "DarazTemplates/brands.html")


def categories(request):
    if request.method == "GET":
        if request.GET.get('search'):
            keyword = request.GET.get('search')
            data, length, keyword = daraz_data(keyword)
            print(request.GET)
            paginator = Paginator(list(data), 12)

            page = request.GET.get('page')

            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            return render(request, "DarazTemplates/categories.html", {'data': data, 'keyword': keyword, 'length': length})
        else:
            return render(request, "DarazTemplates/categories.html")


def about(request):
    return render(request, "DarazTemplates/about.html")


def email(request):
    subject = 'Thank you for Visiting to our site'
    message = 'you are most welcome to DEKH KE LO website your feedback  means a world to us.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request,]
    send_mail( subject, message, email_from, recipient_list )

def add_contact(request):
     submitted = False
     if request.method == 'POST':
         form = ContactForm(request.POST)
         if form.is_valid():
             form.save()
             cd = form.cleaned_data
             email(cd['email'])
             return  render(request, 'DarazTemplates/feedback.html', {'form': form.cleaned_data, 'submitted': submitted})
     else:
         form = ContactForm()
         if 'submitted' in request.GET:
             submitted = True
     return render(request, 'DarazTemplates/contact.html', {'form': form, 'submitted': submitted})


