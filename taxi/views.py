from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CarForm, DriverCreationForm, UpdateLicenseForm, \
    DriverSearchForm, CarSearchForm, ManufacturerSearchForm
from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ManufacturerSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = ManufacturerSearchForm(self.request.GET)

        if form.is_valid():
            return super().get_queryset().filter(
                name__icontains=form.cleaned_data["name"]
            )

        return super().get_queryset()


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_confirm_delete.html"


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.request.GET.get("model", "")
        context["search_form"] = CarSearchForm(initial={
            "model": model
        })

        return context

    def get_queryset(self):
        form = CarSearchForm(self.request.GET)

        if form.is_valid():
            return super().get_queryset().filter(
                model__icontains=form.cleaned_data["model"]
            )

        return super().get_queryset()


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    template_name = "taxi/car_confirm_delete.html"
    success_url = reverse_lazy("taxi:car-list")


def assign_user_to_car(request, pk):
    user = Driver.objects.get(id=request.user.id)
    user.cars.add(pk)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))


def delete_user_from_car(request, pk):
    user = Driver.objects.get(id=request.user.id)
    user.cars.remove(pk)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = DriverSearchForm(initial={
            "username": username
        })

        return context

    def get_queryset(self):
        form = DriverSearchForm(self.request.GET)

        if form.is_valid():
            return super().get_queryset().filter(
                username__icontains=form.cleaned_data["username"]
            )

        return super().get_queryset()


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverUpdateLicenseView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = UpdateLicenseForm
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_update_license_form.html"


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_confirm_delete.html"
