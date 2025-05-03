from django.urls import path, include
from . import views


urlpatterns = [
	path('list/', views.NotesList.as_view(), name="note_list"),
	path('create/', views.NotesCreate.as_view(), name="note_create"),
	path('update/<int:pk>/', views.NotesUpdate.as_view(), name="note_update"),
	path('delete/<int:pk>/', views.NotesDelete.as_view(), name="note_delete"),
	path('detail/<int:pk>/', views.NotesDetail.as_view(), name="note_detail"),

]