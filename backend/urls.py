from django.contrib import admin
from django.urls import path, include
from tasks import views

urlpatterns = [
    path('', views.render_index, name='home'),
    path('admin/', admin.site.urls),
    # tasks app ki URLs ko '/api/tasks/' path se jodo
    path('api/tasks/', include('tasks.urls')), 
]