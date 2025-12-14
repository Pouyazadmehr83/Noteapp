from django.urls import path

from .views import (
    read_data,
    detail_data,
    create_data,
    update_data,
    delete_data,
)

app_name = "notes"

urlpatterns = [
    path("", read_data, name="read"),
    path("note/<int:pk>/", detail_data, name="detail"),
    path("note/new/", create_data, name="create"),
    path("note/<int:pk>/edit/", update_data, name="update"),
    path("note/<int:pk>/delete/", delete_data, name="delete"),
]
