from django.urls import path

from .views.scanTicketView import scanTicketView

urlpatterns = [
    path("", scanTicketView.as_view(), name = "resolutionDet"),

    path('ajax/load-areas/', scanTicketView.load_areas, name='ajax_load_areas'),
    path('ajax/load-errors/', scanTicketView.load_errors, name='ajax_load_errors')
]