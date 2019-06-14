"""urls live here"""

from django.urls import reverse_lazy, path
from django.contrib.auth import views as auth_views

from . import views

app_name = "siteuser"

urlpatterns = []

urlpatterns = [
    path("new/", views.new_siteuser, name="new"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("deactivate-account/", views.deactivate_account, name="deactivate_account"),
    path("activate-account/", views.activate_account, name="activate_account"),
    path("edit-profile/", views.SiteUserEdit.as_view(), name="edit_profile"),
    path("activate/<int:pk>/<str:screen_name>/", views.activate_siteuser, name="new_activation"),
]

urlpatterns += [
    path('new-api-key/', views.get_api_key, name='new_api_key'),
    path('reset-api-key/', views.reset_api_key, name='reset_api_key'),
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
