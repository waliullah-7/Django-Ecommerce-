from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from . models import ProductModel,BrandModel,CategoryModel, AdditionalInformationModel, ProductDescriptionModel, ProductShortDescriptionModel, ProductImageModel, CustomerModel, CartModel
from django.views import View
from django.views.generic import CreateView, ListView
# Create your views here.
from django.views.generic import TemplateView, DetailView, FormView
from django.db.models import Q
from .forms import ProfileForm
from django.db.models.aggregates import Sum

from django.contrib.auth.mixins import LoginRequiredMixin
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY



class index(TemplateView):
    template_name="store/index.html"
  
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # data = self.kwargs['data']
        context= super().get_context_data(**kwargs)
        context['product']=ProductModel.objects.all()
        context['mobile']=ProductModel.objects.filter(p_category__category = 'Mobile')
        context['tab']=ProductModel.objects.filter(p_category__category='Tab')
        context['brand']=BrandModel.objects.all()
        context['trend']=ProductModel.objects.filter(featured=True)
        context['category']=CategoryModel.objects.all()
        context['cart'] = CartModel.objects.filter(username=self.request.user)

        return context
    
class MobileCategory(TemplateView):
    template_name="store/mobile.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        brand_name=self.kwargs['data']
        context['mobile']=ProductModel.objects.filter(p_brand__brand=brand_name , p_category__category='Mobile'  )
        context['product']=ProductModel.objects.all()
        context['tab']=ProductModel.objects.filter(p_category__category='Tab')
        context['brand']=BrandModel.objects.all()
        context['category']=CategoryModel.objects.all()
        context['cart'] = CartModel.objects.filter(username=self.request.user)

        return context

class TabCategory(TemplateView):
    template_name="store/mobile.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        brand_name=self.kwargs['data']
        context['mobile']=ProductModel.objects.filter(p_category__category='Mobile'  )
        context['product']=ProductModel.objects.all()
        context['tab']=ProductModel.objects.filter(p_brand__brand=brand_name , p_category__category='Tab')
        context['brand']=BrandModel.objects.all()
        context['category']=CategoryModel.objects.all()
        context['cart'] = CartModel.objects.filter(username=self.request.user)

        return context
    
    
class Category(TemplateView):
    template_name="store/product.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        brand_name=self.kwargs['data']
        context['product']=ProductModel.objects.all()
        context['category']=ProductModel.objects.filter(p_brand__brand=brand_name , p_category__category='Tab')
        context['brand']=BrandModel.objects.all()

        context['cart'] = CartModel.objects.filter(username=self.request.user)

        return context
    

    
class ProductDetail(DetailView):
    template_name='store/product_detail.html'
    model=ProductModel
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
       context= super().get_context_data(**kwargs)
       id = self.kwargs['pk']
       
       context['proddes']=ProductDescriptionModel.objects.get(productid=id)
       
       context['short']= ProductShortDescriptionModel.objects.filter(productname=id)
       context['images']= ProductImageModel.objects.filter(productid=id)
       context['info']= AdditionalInformationModel.objects.filter(productname=id)
       context['category']=CategoryModel.objects.all()
       context['brand']=BrandModel.objects.all()
       context['cart'] = CartModel.objects.filter(username=self.request.user)

       
       return context
   
    
   
class AccountView(CreateView):
 model= CustomerModel
 template_name='store/my_account.html'
 fields=('fname', 'lname', 'areacode', 'phone', 'address', 'zipcode')
 success_url= ''
 def form_valid(self, form):
     form.instance.user=self.request.user
     return super().form_valid(form)
 

class SearchView(ListView):
   model=ProductModel
   context_object_name="items"
   ordering = ['id']
   paginate_by = 3
   template_name = 'store/search_results.html'
   def get_queryset(self):
      kwrd = self.request.GET.get("keyword")
      queryset= ProductModel.objects.all()
      if kwrd:
        queryset= ProductModel.objects.filter(Q(title__icontains = kwrd) | Q(p_category__category__icontains=kwrd)| Q(p_brand__brand__icontains = kwrd))
        # context={'count=items.count()
                                      
      return queryset
        # return context      
   
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      kwrd = self.request.GET.get("keyword")

      print("my>>",kwrd)
    #   print('count: ',context['count'])
      context['kwrd']= kwrd
    #   context['count']=context['items']
      context['count'] = context['items'].count()
      context['brand'] = BrandModel.objects.all( )
      context['category'] = CategoryModel.objects.all()
      context['cart'] = CartModel.objects.filter(username=self.request.user)
      return context
   
class ShowAllView(TemplateView):
   template_name = 'store/product.html'
   def get_context_data(self, **kwargs):
      context = super().get_context_data()
      kwrd = self.kwargs['da']
      print(kwrd)
      context['brand']=BrandModel.objects.all()
      context['category']=CategoryModel.objects.all()
      context['items']= ProductModel.objects.filter(Q(p_category__category = kwrd) | Q(p_brand__brand= kwrd))
      
      # context['count']=items.count()
      context['kwrd']= kwrd
      return context
   
class CheckoutCart(TemplateView):
   template_name = 'store/checkout_cart.html'
   def get_context_data(self, **kwargs) -> dict[str, Any]:
       context = super().get_context_data(**kwargs)
       context['cart'] = CartModel.objects.filter(username=self.request.user)
       context['brand']=BrandModel.objects.all()
       context['category']=CategoryModel.objects.all()
       return context

   



class AddToCart(LoginRequiredMixin, TemplateView):
   template_name='store/checkout_cart.html'
   def get(self, request, product_id):
       user = self.request.user
       product_id = self.kwargs['product_id']
       product = CartModel.objects.filter(productid=product_id, username= user).first()
       if product:
         product.quantity += 1
         product.save()
       else:
        cart= CartModel(username=user, productid_id=product_id)
        cart.save()
       
       return redirect('/showcart/', kwargs={'pk': product_id})
       

       
   def get_context_data(self, **kwargs) -> dict[str, Any]:
    
      context = super().get_context_data(**kwargs)
      context['cart'] = CartModel.objects.filter(username=self.request.user)
      return context
   
class DecreaseQuantity(TemplateView):
   template_name='store/checkout_cart.html'
   def get(self, request, product_id):
       user = self.request.user
       product = CartModel.objects.get(productid=product_id, username= self.request.user)
       product_id = self.kwargs['product_id']
       if CartModel.objects.filter(productid=product_id).exists() and product.quantity>1 :
         product.quantity -= 1
         product.save()
       else:
         product.delete()

       return redirect('checkout-cart')
       

   def get_context_data(self, **kwargs) -> dict[str, Any]:
      context = super().get_context_data(**kwargs)
      context['cart'] = CartModel.objects.filter(username=self.request.user)
      return context
   
class ShowCartView(TemplateView):
   template_name = 'store/checkout_cart.html'
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      brand = BrandModel.objects.all( )
      cart= CartModel.objects.filter(username=self.request.user)
      category= CategoryModel.objects.all()
      items = CartModel.objects.filter(username=self.request.user)
      if items:
         total_prices= CartModel.objects.filter(username=self.request.user)
         li = []
         abc=None
         for i in total_prices:
            li.append(i.quantity* i.productid.discounted_price)
            abc = sum(li)
         shipping_charges = 100
         total_with_shipping = abc + shipping_charges
      
      context = {'total_price':abc, 'total_with_shipping':total_with_shipping,
                  'brand':brand, 'cart':cart, 'category':category}
      return context
   


class CheckOutInfoView(FormView):
   template_name = 'store/checkout_info.html'
   form_class = ProfileForm
   success_url = '/checkout-payment/'
   def form_valid(self, form):
      
         event = form.save(commit=False)
         event.username = self.request.user
         event.save()
         form.save()
         return super().form_valid(form)





class createcheckoutsession(View):
    
   def post(self, *args, **kwargs):
        items= CartModel.objects.filter(username=self.request.user).values()
        for item in items:
            item=item['productid_id']
        total_prices= CartModel.objects.filter(username=self.request.user)
        li = []
        for i in total_prices:
            # print(i.quantity* i.productid.discounted_price)
            li.append(i.quantity* i.productid.discounted_price)
            abc = sum(li)
        shipping_charges = 100
        total_with_shipping= abc + shipping_charges
        checkout_session = stripe.checkout.Session.create(
           payment_method_types = ['card'],
            line_items=[
                {
                  'price_data':{
                     'currency':'usd',
                     'unit_amount':int(total_with_shipping*100),
                     'product_data':{
                                      
                           'name':item
                     },
                  },
                  'quantity':1
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/paymentcomplete/',
        )

        return redirect(checkout_session.url, code=303)
   

class CheckOutPaymentView(TemplateView):
   template_name = 'store/checkout_payment.html'

class PaymentCompleteView(TemplateView):
   template_name = 'store/checkout_complete.html'
   def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
      total_price= CartModel.objects.filter(username=self.request.user).aggregate(Sum('productid__discounted_price'))
      total_price_s=(total_price['productid__discounted_price__sum'])
      cart = CartModel.objects.filter(username=self.request.user)
      shipping_charges = 100
      total_with_shipping= total_price_s + shipping_charges
      context= super().get_context_data(**kwargs)
      context={'total_with_shipping': total_with_shipping, 'cart':cart}
      return context



