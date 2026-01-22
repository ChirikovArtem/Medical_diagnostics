from django import forms

from organisation.models import Employee, Organisation, Record
from users.forms import StyleFormMixin


class OrganisationForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания и редактирования данных об ресторане"""

    class Meta:
        model = Organisation
        fields = "__all__"


class EmployeeForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания и редактирования данных о сотрудниках"""

    class Meta:
        model = Employee
        fields = "__all__"


class RecordForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания и редактирования данных о столиках"""

    class Meta:
        model = Record
        fields = "__all__"
