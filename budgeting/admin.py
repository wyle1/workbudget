from django.contrib import admin
from .models import WorkEntry, BudgetAllocation

admin.site.register(WorkEntry)
admin.site.register(BudgetAllocation)