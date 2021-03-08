from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import EmployeeRgisterationForm, FromCreatorMixin
import json


@method_decorator(csrf_exempt, name='setup_user')
class Manager(View):
    def post(self, request):
        payload = json.loads(request.body)
        EmployeeRgisterationForm.create(payload)

        return JsonResponse({
            "message": "Manager registered successfully...!!"
        })
        



# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class Employee(View):
    def get(self, request):
        if request.user.role == 'manager':
            emp_list = Employee.objects.all()
            requested_data = []
            for emp in emp_list:
                data = {
                    "id": emp.id,
                    "First Name": emp.first_name,
                    "Last Name" : emp.last_name,
                    "Email": emp.email,
                    "Phone No": emp.phone_number
                }
                requested_data.append(data)

            return JsonResponse({
            "message": "This is get request made by manager",
            "Employee List": requested_data
        })
        return JsonResponse({
            "message": "You are not allow here"
        })

    def post(self, request):
        if request.user.role == 'manager':
            payload = json.loads(request.body)
            EmployeeRgisterationForm.create(payload)
            
        return JsonResponse({
            "message": "Employee profile created successfully..!!"
        })
    
    def delete(self, request, id):
        if request.user.role == "manager":
            emp = Employee.objects.get(id=id)
            emp.delete()
        return JsonResponse({
            "message": "User profile removed fom database...!!"
        })