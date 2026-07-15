from django import forms
from .models import Car, Customer, Sale, Employee, Supplier, Purchase

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"

        widgets = {
            "car_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "company": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control"
            }),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control"
            }),
            "aadhaar": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }


class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        exclude = ["invoice_number", "sale_price"]

        widgets = {
            "customer": forms.Select(attrs={
                "class": "form-control"
            }),
            "car": forms.Select(attrs={
                "class": "form-control"
            }),
            "sale_date": forms.DateInput(attrs={
                "class": "form-control"
            }),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
            "designation": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "salary": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "joining_date": forms.DateInput(attrs={
                "class": "form-control"
            }),
            "photo": forms.FileInput(attrs={
                "class": "form-control"
            }),
        }

class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "company": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control"
            }),
        }

class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase
        fields = "__all__"

    widgets = {
        "supplier": forms.Select(attrs={
            "class": "form-control"
        }),
        "car": forms.Select(attrs={
            "class": "form-control"
        }),
        "quantity": forms.NumberInput(attrs={
            "class": "form-control"
        }),
        "purchase_price": forms.NumberInput(attrs={
            "class": "form-control"
        }),
        "purchase_date": forms.DateInput(attrs={
            "class": "form-control"
        }),
    }


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

    