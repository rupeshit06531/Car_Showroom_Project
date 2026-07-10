from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Car, Customer, Sale, Employee
from .forms import CarForm, CustomerForm, SaleForm, EmployeeForm
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.contrib import messages
from openpyxl import Workbook
from openpyxl.styles import Font
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required


# =========================
# HOME PAGE
# =========================

@login_required
def home(request):

    query = request.GET.get("q")
    company = request.GET.get("company")
    fuel = request.GET.get("fuel")
    price = request.GET.get("price")
    stock = request.GET.get("stock")

    cars = Car.objects.all()

    # Search
    if query:
        cars = cars.filter(
            Q(car_name__icontains=query) |
            Q(company__icontains=query) |
            Q(model__icontains=query)
        )

    # Company Filter
    if company:
        cars = cars.filter(company=company)

    # Fuel Filter
    if fuel:
        cars = cars.filter(fuel_type=fuel)

    # Price Filter
    if price == "1":
        cars = cars.filter(price__lt=500000)

    elif price == "2":
        cars = cars.filter(
            price__gte=500000,
            price__lte=1000000
        )

    elif price == "3":
        cars = cars.filter(price__gt=1000000)

    # Stock Filter
    if stock == "available":
        cars = cars.filter(stock__gt=0)

    elif stock == "out":
        cars = cars.filter(stock=0)

# ==========================
# Pagination
# ==========================

    paginator = Paginator(cars, 10)   # 10 cars per page
    page_number = request.GET.get("page")
    cars = paginator.get_page(page_number)

    # Dashboard Cards
    total_cars = Car.objects.count()
    total_customers = Customer.objects.count()
    total_sales = Sale.objects.count()

    total_companies = Car.objects.values(
        "company"
    ).distinct().count()

    total_value = Car.objects.aggregate(
        Sum("price")
    )["price__sum"] or 0

    total_revenue = Sale.objects.aggregate(
        Sum("sale_price")
    )["sale_price__sum"] or 0

    total_stock = Car.objects.aggregate(
        Sum("stock")
    )["stock__sum"] or 0

    low_stock = Car.objects.filter(
        stock__lte=2
    ).count()

    companies = Car.objects.values_list(
        "company",
        flat=True
    ).distinct()

    fuel_types = Car.objects.values_list(
        "fuel_type",
        flat=True
    ).distinct()

    # Monthly Sales Chart
    months = []
    sales_count = []

    current_month = timezone.now().month
    current_year = timezone.now().year

    for i in range(11, -1, -1):

        month = current_month - i
        year = current_year

        if month <= 0:
            month += 12
            year -= 1

        count = Sale.objects.filter(
            sale_date__year=year,
            sale_date__month=month
        ).count()

        months.append(f"{month}/{year}")
        sales_count.append(count)

    revenue = []

    for i in range(11, -1, -1):

      month = current_month - i
      year = current_year

    if month <= 0:
         month += 12
         year -= 1

    total = Sale.objects.filter(
        sale_date__year=year,
        sale_date__month=month
    ).aggregate(
        Sum("sale_price")
    )["sale_price__sum"] or 0

    revenue.append(total)



    # ==========================
    # Company Wise Sales
    # ==========================

    company_names = []
    company_sales = []

    companies_data = Car.objects.values_list(
        "company",
        flat=True
    ).distinct()

    for company in companies_data:

        count = Sale.objects.filter(
            car__company=company
        ).count()

        company_names.append(company)
        company_sales.append(count)

 # ==========================
# Top Selling Cars
# ==========================

    top_cars = (
    Sale.objects
    .values("car__car_name")
    .annotate(total_sold=Count("id"))
    .order_by("-total_sold")[:5]
    )



    return render(request, "showroom/home.html", {
        "cars": cars,
        "total_cars": total_cars,
        "total_customers": total_customers,
        "total_sales": total_sales,
        "total_companies": total_companies,
        "total_value": total_value,
        "total_revenue": total_revenue,
        "total_stock": total_stock,
        "low_stock": low_stock,
        "companies": companies,
        "fuel_types": fuel_types,
        "months": months,
        "sales_count": sales_count,
        "revenue": revenue,
        "company_names": company_names,
        "company_sales": company_sales,
        "top_cars": top_cars,

    })
# ==========================
# Monthly Sales Chart Data
# ==========================

    months = []
    sales_count = []

    current_month = timezone.now().month
    current_year = timezone.now().year

    for i in range(11, -1, -1):

        month = current_month - i
        year = current_year

        if month <= 0:
            month += 12
            year -= 1

        count = Sale.objects.filter(
            sale_date__year=year,
            sale_date__month=month
        ).count()

        months.append(f"{month}/{year}")
        sales_count.append(count)

    
# =========================
# ADD CAR
# =========================

@login_required
@permission_required('showroom.add_car', raise_exception=True)
def add_car(request):

    if request.method == "POST":

        form = CarForm(request.POST, request.FILES)

        if form.is_valid():
           form.save()
           messages.success(request, "Car added successfully.")
           return redirect("/")

    else:
         form = CarForm()

         return render(request, "showroom/add_car.html", {
           "form": form
     })


# =========================
# EDIT CAR
# =========================

@login_required
@permission_required('showroom.change_car', raise_exception=True)
def edit_car(request, id):

    car = get_object_or_404(Car, id=id)

    if request.method == "POST":

        form = CarForm(
            request.POST,
            request.FILES,
            instance=car
        )

        if form.is_valid():
           form.save()
           messages.success(request, "Car updated successfully.")
           return redirect("/")

    else:

        form = CarForm(instance=car)

    return render(request, "showroom/edit_car.html", {
        "form": form
    })


# =========================
# DELETE CAR
# =========================

@login_required
@permission_required('showroom.delete_car', raise_exception=True)
def delete_car(request, id):

    car = get_object_or_404(Car, id=id)

    if request.method == "POST":
        car.delete()
        messages.success(request, "Car deleted successfully.")
        return redirect("/")

    return render(request, "showroom/delete_car.html", {
        "car": car
    })


@login_required
def export_cars_excel(request):

    wb = Workbook()
    ws = wb.active
    ws.title = "Cars"

    headers = [
        "ID",
        "Car Name",
        "Company",
        "Model",
        "Color",
        "Fuel",
        "Price",
        "Stock",
    ]

    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True)

    cars = Car.objects.all()

    for car in cars:
        ws.append([
            car.id,
            car.car_name,
            car.company,
            car.model,
            car.color,
            car.fuel_type,
            car.price,
            car.stock,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="cars.xlsx"'

    wb.save(response)

    return response



# =========================
# CAR DETAIL
# =========================

@login_required
def car_detail(request, id):

    car = get_object_or_404(Car, id=id)

    return render(request, "showroom/car_detail.html", {
        "car": car
    })

# =========================
# CUSTOMER LIST
# =========================

@login_required
def customer_list(request):

    customers = Customer.objects.all()

    return render(request, "showroom/customer_list.html", {
        "customers": customers
    })


# =========================
# ADD CUSTOMER
# =========================

@login_required
def add_customer(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/customers/")

    else:
        form = CustomerForm()

    return render(request, "showroom/add_customer.html", {
        "form": form
    })


# =========================
# EDIT CUSTOMER
# =========================

@login_required
def edit_customer(request, id):

    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":

        form = CustomerForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():
            form.save()
            return redirect("/customers/")

    else:
        form = CustomerForm(instance=customer)

    return render(request, "showroom/edit_customer.html", {
        "form": form
    })


# =========================
# DELETE CUSTOMER
# =========================

@login_required
def delete_customer(request, id):

    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":
        customer.delete()
        return redirect("/customers/")

    return render(request, "showroom/delete_customer.html", {
        "customer": customer
    })


# =========================
# SALES LIST
# =========================

@login_required
def sale_list(request):

    sales = Sale.objects.select_related(
        "customer",
        "car"
    ).all()

    return render(request, "showroom/sale_list.html", {
        "sales": sales
    })


# =========================
# ADD SALE
# =========================

@login_required
def add_sale(request):

    if request.method == "POST":

        form = SaleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/sales/")

    else:
        form = SaleForm()

    return render(request, "showroom/add_sale.html", {
        "form": form
    })


# =========================
# INVOICE
# =========================

@login_required
def invoice(request, id):

    sale = get_object_or_404(Sale, id=id)

    return render(request, "showroom/invoice.html", {
        "sale": sale
    })

@login_required
def download_invoice(request, id):

    sale = get_object_or_404(Sale, id=id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Invoice_{sale.invoice_number}.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>CAR SHOWROOM MANAGEMENT SYSTEM</b>", styles["Title"]))
    elements.append(Paragraph("Invoice", styles["Heading2"]))

    data = [
        ["Invoice No", sale.invoice_number],
        ["Customer", sale.customer.name],
        ["Car", sale.car.car_name],
        ["Company", sale.car.company],
        ["Sale Price", f"₹ {sale.sale_price}"],
        ["Sale Date", str(sale.sale_date)],
    ]

    table = Table(data, colWidths=[150, 250])

    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))

    elements.append(table)

    doc.build(elements)

    return response


# =========================
# EMPLOYEE LIST
# =========================

@login_required
def employee_list(request):

    employees = Employee.objects.all()

    return render(request, "showroom/employee_list.html", {
        "employees": employees
    })


# =========================
# ADD EMPLOYEE
# =========================

@login_required
@staff_member_required
def add_employee(request):

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect("/employees/")

    else:
        form = EmployeeForm()

    return render(request, "showroom/add_employee.html", {
        "form": form
    })


# =========================
# EDIT EMPLOYEE
# =========================

@login_required
@staff_member_required
def edit_employee(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            request.FILES,
            instance=employee
        )

        if form.is_valid():
            form.save()
            return redirect("/employees/")

    else:
        form = EmployeeForm(instance=employee)

    return render(request, "showroom/edit_employee.html", {
        "form": form
    })


# =========================
# DELETE EMPLOYEE
# =========================

@login_required
@staff_member_required
def delete_employee(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        employee.delete()
        return redirect("/employees/")

    return render(request, "showroom/delete_employee.html", {
        "employee": employee
    })