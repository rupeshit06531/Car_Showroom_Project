from django.shortcuts import render, redirect
from .models import Car
from .forms import CarForm

def home(request):
    cars = Car.objects.all()
    return render(request, 'showroom/home.html', {'cars': cars})

def add_car(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CarForm()

    return render(request, 'showroom/add_car.html', {'form': form})

from django.shortcuts import get_object_or_404

def edit_car(request, id):
    car = get_object_or_404(Car, id=id)

    if request.method == "POST":
        form = CarForm(request.POST, instance=car)

        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = CarForm(instance=car)

    return render(request, "showroom/add_car.html", {
        "form": form
    })