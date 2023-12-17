from django.urls import path
from .import views


urlpatterns = [
    path('',views.home,name="home"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('register',views.register,name="register"),
    path('login',views.login,name="login"),
    path('create-task',views.createTask,name="create-task"),
    path('update-task/<str:pk>/',views.updateTask,name="update-task"),
    path('delete-task/<str:pk>/',views.deleteTask,name="delete-task"),
    path('update-task-status/<int:pk>/', views.update_task_status, name='update-task-status'),
    path('verify-otp/<str:username>/<str:otp>/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
   

]




