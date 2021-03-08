from django.urls import path
from users.views import Employee
from django.contrib.auth.decorators import login_required

#url start here

urlpatterns = [
    path('', Employee.as_view())
]