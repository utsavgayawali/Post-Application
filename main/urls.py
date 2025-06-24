from django.contrib import admin
from django.urls import path,include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post_list/', views.post_list, name='post_list'),
    path('post_create/', views.post_create, name='post_create'),
    path('<int:post_id>/edit_post/', views.edit_post, name='edit_post'),
    path('<int:post_id>/delete_post/', views.delete_post, name='delete_post'),

    path('register/',views.register_view,name='register_view'),
    path('login/',views.login_view,name='login_view'),
    path('logout/',views.logout_view,name='logout_view'),
]
