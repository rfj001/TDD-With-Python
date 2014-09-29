from django.shortcuts import render, redirect
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        # objects.create() is shorthand for creating a new Item, without
        # needing to call .save()
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
        
    items = Item.objects.all()
    return render(request, 'home.html', {'items' : items})
    
