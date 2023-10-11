from django.shortcuts import render, redirect
from .forms import ExpanseFrom
from .models import Expense
from django.views.generic.edit import CreateView
from django.db.models import Sum
import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, 'myapp/index.html')


@method_decorator(login_required, name='dispatch')
class dashbord(CreateView):
    model = Expense
    fields = ['name', 'amount', 'category']
    template_name = 'myapp/dashbord.html'

    def form_valid(self, form):
        form.instance.Username = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        print(self.request.user)
        last_three_month = datetime.date.today() - datetime.timedelta(days=90)
        expanses = Expense.objects.filter(
            date__gt=last_three_month, Username=self.request.user).order_by('-date')
        total_expenses = expanses.aggregate(Sum('amount'))
        last_year = datetime.date.today() - datetime.timedelta(days=365)
        data = Expense.objects.filter(
            date__gt=last_year, Username=self.request.user)
        yearly_sum = data.aggregate(Sum('amount'))
        last_month = datetime.date.today() - datetime.timedelta(days=30)
        data = Expense.objects.filter(
            date__gt=last_month, Username=self.request.user)
        monthly_sum = data.aggregate(Sum('amount'))
        last_week = datetime.date.today() - datetime.timedelta(days=7)
        data = Expense.objects.filter(
            date__gt=last_week, Username=self.request.user)
        weekly_sum = data.aggregate(Sum('amount'))
        daily_sum = Expense.objects.filter(date__gt=last_month, Username=self.request.user).values(
            'date').order_by('-date').annotate(sum=Sum('amount'))
        categorical_sum = Expense.objects.filter(date__gt=last_month, Username=self.request.user).values(
            'category').order_by('category').annotate(sum=Sum('amount'))
        context = super(dashbord, self).get_context_data(**kwargs)
        context.update({'expenses': expanses,
                        'total_expenses': total_expenses, 'yearly_sum': yearly_sum, 'monthly_sum': monthly_sum, 'weekly_sum': weekly_sum, 'daily_sum': daily_sum, 'categorical_sum': categorical_sum})
        return context
    # return render(request,'myapp/index.html',{'expenses':expanses,"total_expenses":total_expenses,'yearly_sum':yearly_sum,'monthly_sum':monthly_sum,'weekly_sum':weekly_sum,'daily_sum':daily_sum,'categorical_sum':categorical_sum})

# def index(request):
#     expense_form=ExpanseFrom()
#     if request.method == "POST":
#         expanse=ExpanseFrom(request.POST)
#         if expanse.is_valid():
#             expanse.save()
    # expanses=Expense.objects.all()
    # total_expenses=expanses.aggregate(Sum('amount'))
    # last_year=datetime.date.today() - datetime.timedelta(days=365)
    # data=Expense.objects.filter(date__gt=last_year)
    # yearly_sum=data.aggregate(Sum('amount'))
    # last_month=datetime.date.today() - datetime.timedelta(days=30)
    # data=Expense.objects.filter(date__gt=last_month)
    # monthly_sum=data.aggregate(Sum('amount'))
    # last_week=datetime.date.today() - datetime.timedelta(days=7)
    # data=Expense.objects.filter(date__gt=last_week)
    # weekly_sum=data.aggregate(Sum('amount'))
    # daily_sum=Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    # categorical_sum=Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    # return render(request,'myapp/index.html',{'expense':expense_form,'expenses':expanses,"total_expenses":total_expenses,'yearly_sum':yearly_sum,'monthly_sum':monthly_sum,'weekly_sum':weekly_sum,'daily_sum':daily_sum,'categorical_sum':categorical_sum})


def edit(request, id):
    expense = Expense.objects.get(pk=id)
    expense_form = ExpanseFrom(instance=expense)
    # print(request.user,expense.Username)
    if request.user == expense.Username:
        if request.method == "POST":
            expense = Expense.objects.get(pk=id)
            form = ExpanseFrom(request.POST, instance=expense)
            if form.is_valid():
                expense.save()
                return redirect("myapp:dashbord")
        return render(request, 'myapp/edit.html', {'expense': expense_form})
    return redirect('user:dashbord')


def delete(request, id):
    if request.user == expense.Username:
        if request.method == "POST" and 'delete' in request.POST:
            expense = Expense.objects.get(pk=id)
            expense.delete()
        return redirect('myapp:dashbord')
    return redirect('user:dashbord')
