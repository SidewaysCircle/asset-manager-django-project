from urllib import request
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..models import Laptop
from django.shortcuts import get_object_or_404
from django.urls import reverse

class laptopDeleteView(UserPassesTestMixin, DeleteView):
    template_name = "laptopDelete.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_object(self, queryset = None):
        laptop_id=self.kwargs.get("pk")
        return get_object_or_404(Laptop, id=laptop_id)

    def get_success_url(self):
        return reverse("laptopList")