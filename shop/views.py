from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json


# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = int(n//4 + ceil((n/4)-(n//4)))

    #params = {'no_of_slides':nSlides, 'range':range(1, nSlides) , 'product': products}

    # allProds = [[products,range(1,len(products)),nSlides],
    #             [products, range(1, len(products)), nSlides]]
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = int(n//4 + ceil((n/4)-(n//4)))
        allProds.append([prod, range(1, nslides), nslides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('description', '')
        contact_msg = Contact(name=name, email=email, phone=phone, desc=desc)
        contact_msg.save()
        message = True
        return render(request, 'shop/contact.html', {'message': message})
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def productView(request, myid):
    #Fetch the product by using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/productView.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '') + ", " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip', '')

        order = Order(items_json=items_json, name=name, email=email, phone=phone, address=address, city=city, state=state, zip=zip_code)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        o_id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': o_id})
    return render(request, 'shop/checkout.html')
