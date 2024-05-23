from django.urls import path
from store import views
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.conf.urls.static import static
urlpatterns = [
    path('',  views.index.as_view(), name=''),
    path('product-detail/<int:pk>/',  views.ProductDetail.as_view(), name='product-detail'),
    path('mobile-brand/<str:data>/',  views.MobileCategory.as_view(), name='mobile-brand'),
    path('tab-brand/<str:data>/',  views.TabCategory.as_view(), name='tab-brand'),
    path('category/<str:data>/',  views.Category.as_view(), name='category'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('showall/<str:da>/', views.ShowAllView.as_view(), name='show-all'),
    path('addtocart/<int:product_id>/', login_required(views.AddToCart.as_view()), name='addtocart'),
    path('showcart/', login_required(views.ShowCartView.as_view()), name='showcart'),

    path('checkout-cart/', views.CheckoutCart.as_view(), name='checkout-cart'),
    path('checkout-info/', views.CheckOutInfoView.as_view(), name='checkout-info'),
    path('checkout-payment/', views.CheckOutPaymentView.as_view(), name='checkout-payment'),
    path('createcheckoutsession/', login_required(views.createcheckoutsession.as_view()), name='createcheckoutsession'),
    path('paymentcomplete/', login_required(views.PaymentCompleteView.as_view()), name='paymentcomplete'),

    path('decrease-quantity/<int:product_id>/', login_required(views.DecreaseQuantity.as_view()), name='decrease-quantity'),



]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)