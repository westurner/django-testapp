from .models import Provider
from .models import Plan
from django.views.generic import ListView
from django.views.generic import DetailView

class ProviderListView(ListView):
    model = Provider

class ProviderDetailView(DetailView):
    model = Provider

class PlanListView(ListView):
    model = Plan

class PlanDetailView(DetailView):
    model = Plan
