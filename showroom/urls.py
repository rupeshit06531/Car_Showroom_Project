from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
     path('', views.home, name='home'),
     path('add-car/', views.add_car, name='add_car'),
     path("edit-car/<int:id>/", views.edit_car, name="edit_car"),
     path("delete-car/<int:id>/", views.delete_car, name="delete_car"),
     path("car/<int:id>/", views.car_detail, name="car_detail"),
     path("customers/", views.customer_list, name="customer_list"),
     path("add-customer/", views.add_customer, name="add_customer"),
     path("edit-customer/<int:id>/", views.edit_customer, name="edit_customer"),
     path("delete-customer/<int:id>/", views.delete_customer, name="delete_customer"),
     path("sales/", views.sale_list, name="sale_list"),
     path("add-sale/", views.add_sale, name="add_sale"),
     path("invoice/<int:id>/", views.invoice, name="invoice"),
     path("employees/", views.employee_list, name="employee_list"),
     path("add-employee/", views.add_employee, name="add_employee"),
     path("edit-employee/<int:id>/", views.edit_employee, name="edit_employee"),
     path("delete-employee/<int:id>/", views.delete_employee, name="delete_employee"),
     path("login/", auth_views.LoginView.as_view(template_name="showroom/login.html"), name="login",),
     path("logout/",auth_views.LogoutView.as_view(), name="logout",),
     path("invoice/<int:id>/pdf/", views.download_invoice, name="download_invoice",),
     path("export/cars/", views.export_cars_excel, name="export_cars_excel",
),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    