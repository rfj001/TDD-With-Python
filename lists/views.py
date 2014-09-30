from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.forms import ItemForm
from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})
    
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form =ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})

def new_list(request):
    # Pass the request.POST data into the form's constructor
    form = ItemForm(data=request.POST)
    # We use form.is_valid() to determine whether this is a good or bad submit
    if form.is_valid():
        list_ = List.objects.create()
        item = Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        # If invalid, we pass the form down to the template, instead of
        # hardcoded error string
        return render(request, 'home.html', {"form": form})