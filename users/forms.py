from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import BaseUser
from django.http import JsonResponse

#base method form mixins
class FromCreatorMixin():
    @classmethod
    def create(cls, form_data=None):
        form = cls(form_data)
        if not form.is_valid():
            return JsonResponse({
                "message": "INvalid details",
                "errors": form.errors    
            })
        return form.save()

class FromUpdaterMixin():
    @classmethod
    def update(cls, instance, form_data=None):
        form = cls(form_data)
        if not form.is_valid():
            return JsonResponse({
                "message": "INvalid details",
                "errors": form.errors    
            })
        return form.save()

#-------------END-------->

#base user form to check fields
class BaseUserForm(UserCreationForm):
    def _can_check(self, instance, field_name):
        if instance is None:
            return True
        return getattr(instance, field_name) is not self.cleaned_data[field_name]

    def _exists(self, model=None, **kwargs):
        model = model if model else BaseUser
        return model.objects.filter(**kwargs).exists()

    def _clean_field(self, instance, field_name, model=None):
        value = self.cleaned_data[field_name]

        if self._can_check(instance, field_name) and self._exists(model, **{field_name:value}):
            raise ValidationError("%s already exists" %field_name)
        return value


class EmployeeModelForm(BaseUserForm):

    def clean_email(self, instance=None):
        return self._clean_field(instance, "email")
    
    def clean_username(self, instance=None):
        return self._clean_field(instance, "username")

    def clean_phone_number(self, instance=None):
        return self._clean_field(instance, "phone_number")

    class Meta:
        model = BaseUser
        fields = '__all__'


class EmployeeRgisterationForm(EmployeeModelForm, FromCreatorMixin):
    
    class Meta(EmployeeModelForm.Meta):
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'phone_number',
            'email',
        )