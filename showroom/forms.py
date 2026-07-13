from django import forms
from .models import Car, Customer, Sale, Employee, Supplier, Purchase

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        exclude = ["invoice_number", "sale_price"]

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = "__all__"

class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase
        fields = "__all__"

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()