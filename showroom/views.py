from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Car, Customer, Sale, Employee, Supplier, Purchase
from .forms import (
    CarForm,
    CustomerForm,
    SaleForm,
    EmployeeForm,
    SupplierForm,
    PurchaseForm,
    ExcelUploadForm,
)
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

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
import openpyxl





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

    # Total Purchase Cost
    total_purchase = Purchase.objects.aggregate(
        Sum("purchase_price")
    )["purchase_price__sum"] or 0

# Net Profit
    net_profit = total_revenue - total_purchase

    total_stock = Car.objects.aggregate(
        Sum("stock")
    )["stock__sum"] or 0

    low_stock = Car.objects.filter(
        stock__lte=2
    ).count()


# Today's Dashboard
    today = timezone.now().date()
    

    today_sales = Sale.objects.filter(
        sale_date=today
    ).count()

    today_revenue = Sale.objects.filter(
        sale_date=today
    ).aggregate(
        Sum("sale_price")
    )["sale_price__sum"] or 0


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

    best_employee = (
    Sale.objects.values("employee__name")
    .annotate(total_sales=Count("id"))
    .order_by("-total_sales")
    .first()
)

    return render(request, "showroom/home.html", {
        "cars": cars,
        "total_cars": total_cars,
        "total_customers": total_customers,
        "total_sales": total_sales,
        "total_companies": total_companies,
        "total_value": total_value,
        "total_revenue": total_revenue,
        "total_purchase": total_purchase,
        "net_profit": net_profit,
        "total_stock": total_stock,
        "low_stock": low_stock,

        "today_sales": today_sales,
        "today_revenue": today_revenue,

        "companies": companies,
        "fuel_types": fuel_types,
        "months": months,
        "sales_count": sales_count,
        "revenue": revenue,
        "company_names": company_names,
        "company_sales": company_sales,
        "top_cars": top_cars,
        "best_employee": best_employee,
        "recent_sales": recent_sales,

    })

    
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
        "car",
        "employee"
    ).all().order_by("-sale_date")

    query = request.GET.get("q")
    employee = request.GET.get("employee")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if query:
        sales = sales.filter(
            Q(invoice_number__icontains=query) |
            Q(customer__name__icontains=query) |
            Q(car__car_name__icontains=query)
        )

    if employee:
        sales = sales.filter(employee__id=employee)

    if start_date and end_date:
        sales = sales.filter(
            sale_date__range=[start_date, end_date]
        )

    employees = Employee.objects.all()

    paginator = Paginator(sales, 10)
    page_number = request.GET.get("page")
    sales = paginator.get_page(page_number)

    return render(request, "showroom/sale_list.html", {
        "sales": sales,
        "employees": employees,
    })

# =========================
# ADD SALE
# =========================

@login_required
def add_sale(request):

    if request.method == "POST":

        form = SaleForm(request.POST)

        if form.is_valid():

          sale = form.save()

    # Send Email
    if sale.customer.email:

        send_mail(
            subject="Car Purchase Invoice",
            message=f"""
            Hello {sale.customer.name},

            Thank you for purchasing {sale.car.car_name}.

            Invoice Number: {sale.invoice_number}

            Amount: ₹{sale.sale_price}

            Purchase Date: {sale.sale_date}

            Thank you for choosing our showroom.
            """,

            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sale.customer.email],
            fail_silently=True,
        )

        return redirect("sale_list")

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

@login_required
def invoice_pdf(request, sale_id):

    sale = get_object_or_404(Sale, id=sale_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{sale.invoice_number}.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, 800, "CAR SHOWROOM INVOICE")

    p.setFont("Helvetica", 12)

    y = 760

    p.drawString(50, y, f"Invoice No : {sale.invoice_number}")
    y -= 25

    p.drawString(50, y, f"Date : {sale.sale_date}")
    y -= 25

    p.drawString(50, y, f"Customer : {sale.customer.name}")
    y -= 25

    p.drawString(50, y, f"Car : {sale.car.car_name}")
    y -= 25

    p.drawString(50, y, f"Company : {sale.car.company}")
    y -= 25

    p.drawString(50, y, f"Model : {sale.car.model}")
    y -= 25

    p.drawString(50, y, f"Price : Rs. {sale.selling_price}")
    y -= 40

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Thank You For Your Purchase!")

    p.showPage()
    p.save()

    return response

@login_required
def sales_report(request):

    sales = Sale.objects.all().order_by("-sale_date")

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        sales = sales.filter(
            sale_date__range=[start_date, end_date]
        )

    total_revenue = sales.aggregate(
        Sum("sale_price")
    )["sale_price__sum"] or 0

    return render(request, "showroom/sales_report.html", {
        "sales": sales,
        "total_revenue": total_revenue,
        "start_date": start_date,
        "end_date": end_date,
    })

@login_required
def sales_report_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="sales_report.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()
    elements = []

    # Heading
    elements.append(Paragraph("<b>Car Showroom Sales Report</b>", styles["Title"]))

    # Table Data
    data = [["Invoice", "Customer", "Car", "Employee", "Price"]]

    sales = Sale.objects.all().order_by("-sale_date")

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
         sales = sales.filter(
        sale_date__range=[start_date, end_date]
    )

    total_revenue = 0

    for sale in sales:

        data.append([
            sale.invoice_number,
            sale.customer.name,
            sale.car.car_name,
            sale.employee.name if sale.employee else "-",
            f"₹ {sale.sale_price}"
        ])

        total_revenue += sale.sale_price

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
    ]))

    elements.append(table)

    elements.append(
        Paragraph(
            f"<br/><b>Total Revenue : ₹ {total_revenue}</b>",
            styles["Heading2"]
        )
    )

    doc.build(elements)

    return response

@login_required
def supplier_list(request):

    suppliers = Supplier.objects.all().order_by("name")

    return render(
        request,
        "showroom/supplier_list.html",
        {
            "suppliers": suppliers
        }
    )

@login_required
def add_supplier(request):

    if request.method == "POST":

        form = SupplierForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("supplier_list")

    else:
        form = SupplierForm()

    return render(
        request,
        "showroom/add_supplier.html",
        {
            "form": form
        }
    )


@login_required
def edit_supplier(request, id):

    supplier = get_object_or_404(Supplier, id=id)

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)

        if form.is_valid():
            form.save()
            return redirect("supplier_list")

    else:
        form = SupplierForm(instance=supplier)

    return render(
        request,
        "showroom/add_supplier.html",
        {
            "form": form
        }
    )

@login_required
def delete_supplier(request, id):

    supplier = get_object_or_404(Supplier, id=id)

    supplier.delete()

    return redirect("supplier_list")

@login_required
def purchase_list(request):

    purchases = Purchase.objects.select_related(
        "supplier",
        "car"
    ).order_by("-purchase_date")

    return render(
        request,
        "showroom/purchase_list.html",
        {
            "purchases": purchases
        }
    )


@login_required
def add_purchase(request):

    if request.method == "POST":

        form = PurchaseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("purchase_list")

    else:
        form = PurchaseForm()

    return render(
        request,
        "showroom/add_purchase.html",
        {
            "form": form
        }
    )

@login_required
def edit_purchase(request, id):

    purchase = get_object_or_404(Purchase, id=id)

    old_quantity = purchase.quantity

    if request.method == "POST":

        form = PurchaseForm(request.POST, instance=purchase)

        if form.is_valid():

            purchase = form.save(commit=False)

            difference = purchase.quantity - old_quantity

            purchase.car.stock += difference
            purchase.car.save()

            purchase.save()

            return redirect("purchase_list")

    else:
        form = PurchaseForm(instance=purchase)

    return render(request, "showroom/add_purchase.html", {
        "form": form
    })

@login_required
def delete_purchase(request, id):

    purchase = get_object_or_404(Purchase, id=id)

    purchase.car.stock -= purchase.quantity
    purchase.car.save()

    purchase.delete()

    return redirect("purchase_list")

@login_required
def customer_history(request, id):

    customer = get_object_or_404(Customer, id=id)

    sales = Sale.objects.select_related(
        "car",
        "employee"
    ).filter(customer=customer)

    total_amount = sales.aggregate(
        Sum("sale_price")
    )["sale_price__sum"] or 0

    return render(
        request,
        "showroom/customer_history.html",
        {
            "customer": customer,
            "sales": sales,
            "total_amount": total_amount,
        }
    )


@login_required
def import_cars(request):

    if request.method == "POST":

        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():

            excel_file = request.FILES["excel_file"]

            workbook = openpyxl.load_workbook(excel_file)

            sheet = workbook.active

            for row in sheet.iter_rows(min_row=2, values_only=True):

                Car.objects.create(
                    car_name=row[0],
                    company=row[1],
                    model=row[2],
                    color=row[3],
                    fuel_type=row[4],
                    price=row[5],
                    stock=row[6],
                )

            messages.success(
                request,
                "Cars imported successfully!"
            )

            return redirect("home")

    else:

        form = ExcelUploadForm()

    return render(
        request,
        "showroom/import_cars.html",
        {
            "form": form
        }
    )