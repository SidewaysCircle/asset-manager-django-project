from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from ..models import *

# Create your views here.


class laptopListView(LoginRequiredMixin, ListView):
    template_name = "laptopList.html"
    queryset = Laptop.objects.all()
    context_object_name = "laptopList"