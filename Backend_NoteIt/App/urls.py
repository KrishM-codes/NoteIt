from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import NoteListCreateView, NoteDetailView

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', views.Home.as_view(), name='home'),
    path('profile/', views.UserProfile.as_view(), name='user_profile'),
    path('register/', views.RegisterUser.as_view(), name='register_user'),
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('categories/', views.UserCategoriesView.as_view(), name='user-categories'),
]