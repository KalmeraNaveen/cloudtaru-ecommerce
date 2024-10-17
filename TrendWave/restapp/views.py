from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
import json
from .forms import RegistrationForm
from rest_framework.views import APIView
from .models import ProductsModel,usersmodel
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .serializers import productserializer,usersserializer 
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from rest_framework.decorators import api_view
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def clear_cache_view(request):
    cache.clear()
    return HttpResponse('Cache cleared successfully')


class Mypagination(PageNumberPagination):
    page_size = 12

class productsview(ListAPIView):
    queryset = ProductsModel.objects.all() 
    serializer_class = productserializer
    pagination_class = Mypagination

@method_decorator(csrf_exempt,name='dispatch')
class usersview(APIView):
    def get(self,request,*args,**kwargs):
        email=request.GET.get('email')
        if email:
            record=usersmodel.objects.get(email=email)
            py_data={'username':record.username,
                     'email':record.email,
                     'address':record.address}
            json_data=json.dumps(py_data)
            return HttpResponse(json_data,content_type='application/json')
        records=usersmodel.objects.all().values()
        json_data=json.dumps(list(records))
        return HttpResponse(json_data,content_type='application/json')
    def post(self,request,*args,**kwargs):
        data=request.body
        if data:
            try:
                py_data=json.loads(data)
            except:
                message=json.dumps({'msg':'please send json response'})
                return HttpResponse(message,content_type='application/json',status=400)
            else:
                serializer=usersserializer(data=py_data)
                if serializer.is_valid():
                    serializer.save()
                    message=json.dumps({'msg':'Account Created successfully'})
                    return HttpResponse(message,content_type='application/json')
                else:
                    message=json.dumps(serializer.errors)
                    return HttpResponse(message,content_type='application/json',status=400)
    def put(self,request,*args,**kwargs):
        data=request.body
        py_data=json.loads(data)
        email=py_data.get('email')
        record=usersmodel.objects.get(email=email)
        if 'address' in py_data:
            address=py_data.get('address')
            updated_data={'username':record.username,
                          'email':email,
                          'password':record.password,
                          'confirmpassword':record.password,
                          'address':address,
                          'orders':record.orders,
                          'cart':record.cart}
            serializer=RegistrationForm(updated_data,instance=record)
            if serializer.is_valid():
                serializer.save()
                response=json.dumps({'msg':'Address Successfully updated'})
                return HttpResponse(response,content_type='application/json')
            else:
                json_data=json.dumps(serializer.errors)
                print(serializer.errors)
                return HttpResponse(json_data,content_type='application/json',status=400)    
        elif 'orders' in py_data:
            orders=py_data.get('orders')
            if record.orders == 'null' or record.orders == '':
                updated_data={'username':record.username,
                          'email':email,
                          'password':record.password,
                          'confirmpassword':record.password,
                          'address':record.address,
                          'orders':orders,
                          'cart':record.cart}
                serializer=RegistrationForm(updated_data,instance=record)
                if serializer.is_valid():
                    serializer.save()
                    response=json.dumps({'msg':'orders Successfully updated'})
                    return HttpResponse(response,content_type='application/json')
            else:
                updated_data={'username':record.username,
                          'email':email,
                          'password':record.password,
                          'confirmpassword':record.password,
                          'address':record.address,
                          'orders':record.orders+','+orders,
                          'cart':record.cart}
                serializer=RegistrationForm(updated_data,instance=record)
                if serializer.is_valid():
                    serializer.save()
                    response=json.dumps({'msg':'orders Successfully updated'})
                    return HttpResponse(response,content_type='application/json')
        elif 'cart' in py_data:
            cart=py_data.get('cart')
            if record.cart =='null' or record.cart =='':
                print(len(record.cart))
                print(record.cart)
                updated_data={'username':record.username,
                          'email':email,
                          'password':record.password,
                          'address':record.address,
                          'orders':record.orders,
                          'cart':cart}
                serializer=RegistrationForm(updated_data,instance=record)
                if serializer.is_valid():
                    serializer.save()
                    response=json.dumps({'msg':'cart Successfully updated'})
                    return HttpResponse(response,content_type='application/json')
                else:
                    json_data=json.dumps(serializer.errors)
                    print(serializer.errors)
                    return HttpResponse(json_data,content_type='application/json',status=400)    
            else:
                if cart not in record.cart:
                    print(len(cart))
                    print(cart)
                    updated_data={'username':record.username,
                          'email':email,
                          'password':record.password,
                          'address':record.address,
                          'orders':record.orders,
                          'cart':record.cart+','+cart}
                    serializer=RegistrationForm(updated_data,instance=record)
                    if serializer.is_valid():
                        serializer.save()
                        response=json.dumps({'msg':'cart Successfully updated'})
                        return HttpResponse(response,content_type='application/json')
                    else:
                        json_data=json.dumps(serializer.errors)
                        print(serializer.errors)
                        return HttpResponse(json_data,content_type='application/json',status=400)    
                else:
                    json_data=json.dumps({'msg':'you have already added this item to cart'})
                    return HttpResponse(json_data,content_type='application/json')
    def patch(self,request,*args,**kwargs):
        data=request.body
        py_data=json.loads(data)
        cart=py_data.get('cart')
        email=py_data.get('email')
        record=usersmodel.objects.get(email=email)
        cart_details=record.cart.split(',')
        cart_details.remove(cart)
        updated_cart=','.join(cart_details)
        updated_data={'id':record.id,
                      'username':record.username,
                      'email':email,
                      'password':record.password,
                      'orders':record.orders,
                      'cart':updated_cart,
                      'address':record.address}
        form=RegistrationForm(updated_data,instance=record)
        if form.is_valid():
            form.save()
            json_data=json.dumps({'msg':'successfully removed product from cart'})
            return HttpResponse(json_data,content_type='application/json')
        else:
            json_data=json.dumps(form.errors)
            return HttpResponse(json_data,content_type='application/json',status=400)

def products(request):
    if 'email' in request.session:
        return render(request,'products.html')
    else:
        return redirect('login')


def product_detail(request, id):
    if 'email' in request.session:
        product = ProductsModel.objects.get(id=id)
        record={'id':product.id,'title':product.title,'price':product.price,'image':product.price,'images':product.images.split(','),'description':product.description}
        return render(request, 'product_detail.html', {'product': record})
    return redirect('login')

class clothes(ListAPIView):
    queryset = ProductsModel.objects.filter(category='clothes')
    serializer_class = productserializer
    pagination_class = Mypagination

def cloth(request):
    if 'email' in request.session:
        return render(request,'clothes.html')
    else:
        return redirect('login')

class electronics(ListAPIView):
    queryset = ProductsModel.objects.filter(category='electronics')
    serializer_class = productserializer
    pagination_class = Mypagination

def electron(request):
    if 'email' in request.session:
        return render(request,'electronics.html')
    else:
        return redirect('login')

class furniture(ListAPIView):
    queryset = ProductsModel.objects.filter(category='furniture')
    serializer_class = productserializer
    pagination_class = Mypagination

def wood_furniture(request):
    if 'email' in request.session:
        return render(request,'furniture.html')
    else:
        return redirect('login')

class shoes(ListAPIView):
    queryset = ProductsModel.objects.filter(category='shoes')
    serializer_class = productserializer
    pagination_class = Mypagination

def func_shoes(request):
    if 'email' in request.session:
        return render(request,'shoes.html')
    else:
        return redirect('login')

class other(ListAPIView):
    queryset = ProductsModel.objects.filter(category='miscellanious')
    serializer_class = productserializer
    pagination_class = Mypagination

def other_items(request):
    if 'email' in request.session:
        return render(request,'other.html')
    else:
        return redirect('login')

def register(request):
    if 'email' in request.session:
        return redirect('products')
    return render(request,'registration.html')

def login(request):
    if 'email' in request.session:
        return redirect('products')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            record = usersmodel.objects.get(email=email)
            if check_password(password, record.password):
                # messages.success(request, 'Login successful')
                request.session['email']=email
                return redirect('products')  
            else:
                messages.error(request, 'Invalid password')
        except usersmodel.DoesNotExist:
            messages.error(request, 'User does not exist')

    return render(request, 'login.html')

def logout(request):
    request.session.clear()
    return redirect('login')

def profile(request):
    if 'email' in request.session:
        return render(request,'profile.html')
    else:
        return redirect('login')
@api_view(['GET'])
def cart(request):
    if 'email' in request.session:
        try:
            record = usersmodel.objects.get(email=request.session['email'])
            cart = record.cart.split(',')
            list_data = []
            if cart:
                for i in cart:
                    try:
                        product = ProductsModel.objects.get(title=i)
                        data = {
                            'id': product.id,
                            'title': product.title,
                            'price': product.price,
                            'image': product.image,
                            'images': product.images,
                            'category': product.category,
                            'description': product.description
                        }
                        list_data.append(data)
                    except ProductsModel.DoesNotExist:
                        # Log or handle the error where the product is not found
                        continue
            json_data = json.dumps(list_data)
            return HttpResponse(json_data, content_type='application/json')
        except usersmodel.DoesNotExist:
            return HttpResponse("User not found", status=404)


def cart_view(request):
    if 'email' in request.session:
        return render(request,'cart.html')
    else:
        return redirect('login')


def buy(request, id):
    product = get_object_or_404(ProductsModel, id=id)
    gst_rate = 0.05  # 5%
    price = product.price
    gst_amount = price * gst_rate
    total_amount = price + gst_amount

    context = {
        'product': product,
        'gst_amount': gst_amount,
        'total_amount': total_amount
    }
    return render(request,'buynow.html', context)



@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('productId')
            amount = data.get('amount')
            currency = data.get('currency')

            # Create a Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product': product_id,
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8000/success/',  # Replace with your success URL
                cancel_url='http://localhost:8000/cancel/',    # Replace with your cancel URL
            )

            return JsonResponse({'url': session.url})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

