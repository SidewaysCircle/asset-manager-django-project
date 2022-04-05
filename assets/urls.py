import imp
from django.urls import path

from .views.laptopCreateView import laptopCreateView
from .views.laptopListView import laptopListView
from .views.laptopUpdate import laptopUpdateView
from .views.laptopDelete import laptopDeleteView
from .views.laptopCheckout import laptopCheckoutView
from .views.laptopCheckin import laptopCheckinView


urlpatterns = [
    path('', laptopListView.as_view(), name = "laptopList"),
    path('new/', laptopCreateView.as_view(), name = "laptopCreate"),
    path('<int:pk>/update/', laptopUpdateView.as_view(), name = "laptopUpdate"),
    path('<int:pk>/checkin/', laptopCheckinView.as_view(), name = "laptopCheckin"),
    path('<int:pk>/checkout/', laptopCheckoutView.as_view(), name = "laptopCheckout" ),
    path('<int:pk>/delete/', laptopDeleteView.as_view(), name = "laptopDelete"),
]