from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Laptop
from ..forms import createLaptopForm


class laptopCreateView(LoginRequiredMixin, CreateView):
    template_name = "laptopCreate.html"
    form_class = createLaptopForm
    queryset = Laptop.objects.all()

    def form_valid(self, form):
        return super(laptopCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Return Bad Request response if form is invalid
        """
        response = super().form_invalid(form)
        response.status_code = 400
        return response