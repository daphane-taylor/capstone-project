from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def item_list_view(request):
	return render(request, 'items/item_list.html')

def item_detail_view(request, id):
	return render(request, 'items/item_detail.html', {'id': id})

@login_required
def item_update_view(request, id):
	return render(request, 'items/item_update.html', {'id': id})

@login_required
def item_delete_view(request, id):
	return render(request, 'items/item_delete.html', {'id': id})

@login_required
def item_create_view(request):
	return render(request, 'items/item_create.html')

