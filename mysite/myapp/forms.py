from django.forms import ModelForm
from .models import Expense
class ExpanseFrom(ModelForm):
    class Meta:
        model=Expense
        fields=('name','amount','category')
