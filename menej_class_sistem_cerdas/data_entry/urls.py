from django.urls import path
from . import views

app_name = 'data_entry'  # Untuk namespacing di template dengan {% url 'data_entry:nama_url' %}

urlpatterns = [
    path('', views.set_data_entry, name='set_data_entry'),
    path('pengguna/', views.set_pengguna, name='set_pengguna'),
    path('pengguna/view/<int:id>/', views.view_pengguna, name='view_pengguna'),
    path('pengguna/edit/<int:id>/', views.edit_pengguna, name='edit_pengguna'),
    path('pengguna/listpenggunabystate/', views.search_pengguna_by_state, name='search_pengguna_by_state'),
    path('api/pengguna/<int:id>/', views.get_pengguna_detail_api, name='get_pengguna_detail_api'),
    path('content/', views.set_content, name='set_content'),
    path('content/view/<int:id>/', views.view_konten, name='view_konten'),
    path('content/edit/<int:id>/', views.edit_konten, name='edit_konten'),  
]
