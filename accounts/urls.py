from django.urls import path
from . import views
from django.conf.urls.static import static  
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home ,name = "home"),
    path('products/', views.product, name="products"),

    path('customer/<str:pk>/', views.customer, name= "customer"),

    path('create_order/',views.createOrder,name = "create_order"),

    path('create_order_customer/<str:pk>',views.createOrderCustomer,name = "create_order_customer"),

    path('update_order/<str:pk>/',views.updateOrder,name = "update_order"),

    path('delete_order/<str:pk>/',views.deleteOrder,name = "delete_order"),

    path('create_customer/',views.createCustomer,name = "create_customer"),

    path('update_customer/<str:pk>/',views.updateCustomer,name = "update_customer"),

    path('delete_customer/<str:pk>/',views.deleteCustomer,name = "delete_customer"),

    path('create_product/',views.createProduct,name = "create_product"),

    path('update_product/<str:pk>/',views.updateProduct,name = "update_product"),

    path('delete_product/<str:pk>/',views.deleteProduct,name = "delete_product"),

    path('register/',views.registerPage, name = "register"),

    path('login/', views.loginPage, name = "login"),

    path('logout/', views.logoutPage, name = "logout"),

    path('user/',views.userPage, name = "user-page"),

    path('account/', views.accountSettings, name="account"),
    #password reset functionality
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = "accounts/password_reset.html"),name = "reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = "accounts/password_reset_sent.html"),name = "password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/password_reset_form.html"), name = "password_reset_confirm"),

    path('',auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password_reset_done.html"),name = "password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

