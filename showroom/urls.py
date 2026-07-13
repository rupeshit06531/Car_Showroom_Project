from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet



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
     path("sales-report/", views.sales_report, name="sales_report"),
     path("sales-report/pdf/", views.sales_report_pdf, name="sales_report_pdf"),

     path("invoice/<int:id>/", views.invoice, name="invoice"),
     path("employees/", views.employee_list, name="employee_list"),
     path("add-employee/", views.add_employee, name="add_employee"),

     path("suppliers/", views.supplier_list, name="supplier_list"),
     path("add-supplier/", views.add_supplier, name="add_supplier"),

     path("purchases/", views.purchase_list, name="purchase_list"),
     path("add-purchase/", views.add_purchase, name="add_purchase"),

     path("edit-purchase/<int:id>/", views.edit_purchase, name="edit_purchase"),
     path("delete-purchase/<int:id>/", views.delete_purchase, name="delete_purchase"),

     path("edit-employee/<int:id>/", views.edit_employee, name="edit_employee"),
     path("delete-employee/<int:id>/", views.delete_employee, name="delete_employee"),
     path("login/", auth_views.LoginView.as_view(template_name="showroom/login.html"), name="login",),
     path("logout/",auth_views.LogoutView.as_view(), name="logout",),
     path("invoice/<int:id>/pdf/", views.download_invoice, name="download_invoice",),
     path("export/cars/", views.export_cars_excel, name="export_cars_excel"),
          
     path('invoice-pdf/<int:sale_id>/', views.invoice_pdf, name='invoice_pdf'),

     path("edit-supplier/<int:id>/", views.edit_supplier, name="edit_supplier"),
     path("delete-supplier/<int:id>/", views.delete_supplier, name="delete_supplier"),

     path("customer-history/<int:id>/", views.customer_history, name="customer_history"),
     path("import-cars/", views.import_cars, name="import_cars"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


   
