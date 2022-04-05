from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Laptop
from ..forms import checkoutLaptopForm
from django.shortcuts import get_object_or_404

class laptopCheckoutView(LoginRequiredMixin, UpdateView):
    template_name = "laptopCheckout.html"
    form_class = checkoutLaptopForm

    def get_object(self, queryset = None):
        laptop_id=self.kwargs.get("pk")
        return get_object_or_404(Laptop, id=laptop_id)

    def form_valid(self, form):
        return super(laptopCheckoutView, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response