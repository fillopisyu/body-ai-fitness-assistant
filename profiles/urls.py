# profiles/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('generate-plan/', views.generate_workout_view, name='generate_plan'),
    path('chat/', views.chat_page_view, name='chat_page'),
    path('chat/api/send_message/', views.chat_api_view, name='chat_api_send_message'),
    path('save-program/', views.save_program_view, name='save_program'),
    path('my-programs/', views.my_programs_view, name='my_programs'),
    path('my-programs/<int:program_id>/toggle-status/', views.toggle_program_status_view, name='toggle_program_status'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/generate-plan/', views.generate_plan_api_view, name='generate_plan_api'),
    path('chat/clear/', views.clear_chat_history_view, name='clear_chat_history'),
    path('my-programs/<int:program_id>/delete/', views.delete_program_view, name='delete_program'),
]