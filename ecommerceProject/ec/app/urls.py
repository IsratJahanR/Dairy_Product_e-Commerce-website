
from django.urls import path
from app import views
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_view
from .forms import LoginForm



urlpatterns = [
    path('', views.home,name='home'),
    path('about/', views.about,name="about"),
    path('contact/', views.contact,name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(),name='category'),
    path("category-title/<val>", views.CategoryTitle.as_view(),name='category-title'),
    path("product-detail/<int:pk>", views.ProductDetails.as_view(),name='product-detail'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path("updateaddress/<int:pk>", views.UpdateAddress.as_view(),name='updateaddress'),
    path("Changepassword/>", views.ChangePassword,name='changepassword'),
    path('add-to-cart/<int:product_id>', views.add_to_cart,name="add-to-cart"),
    path('cart/', views.show_cart,name="showcart"),
    path('wishlist/', views.show_wishlist,name="showwishlist"),
    path('checkout/', views.checkout,name="checkout"),
    path('paymentdone/', views.paymentdone,name="paymentdone"),
    path('search/', views.search_view,name="search"),
    path('bkash/', views.bkash,name="search"),

    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/',views.minus_wishlist),
    
   #login Authentication: 
   path("registration/", views.CustomerRegistrationView.as_view(),name='customerregistration'),
   path('login/',views.LoginPage,name='login'),
   #path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
   path('login/',views.LoginPage,name='logout'),
   #login Admin Authentication: 

   path("adminhome/", views.adminhome,name='adminhome'),
   path('allproduct/', views.allproduct,name="allproduct"),
   path('allcustomer/', views.allcustomer,name="allcustomer"),
   path('addproduct/', views.addproduct_view,name="addproduct"),
   path('update-product/<int:pk>', views.update_product_view.as_view(),name='update-product'),
   path('delete-product/<int:pk>', views.delete_product_view,name='delete-product'),

   
  

  # path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),













  # path("passwordchange/",auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',#form_class=MyPaswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
   

   #path("accounts/login/",auth_view.LoginView.as_view
    #     (template_name='app/login.html',authentication_form='LoginForm'),name='login'),

    #  path('login/', views.login,name="login"),

   # path('password-reset/',auth_view.PasswordResetView.as_view
   #      (template_name='app/password_reset.html',form_class=MyPasswordResetForm),
   #      name='password_reset')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
