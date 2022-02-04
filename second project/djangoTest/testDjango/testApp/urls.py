
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import ListView, DetailView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm
urlpatterns = [

    path('', views.indexAuth, name='home'),
    path('indexNotAuth', views.indexNotAuth, name='indexNotAuth'),
    path('myFollow', views.myFollow, name='myFollow'),
    path('favorite', views.favorite, name='favorite'),
    path('export_data', views.export_data, name='export_data'),
    path('formRecipe', views.formRecipe, name='formRecipe'),
    path('register', views.RegisterFormView.as_view(), name='register'),
    path('login', views.LoginFormView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile_view/<int:author_id>/', views.profile_view, name='profile_view'),
    path('recipe/<int:recipe_id>/', views.mono, name='mono'),
    path('delete/<int:recipe_id>/', views.delete_task, name='delete'),
    path('indexNotAuth', views.indexNotAuth, name='indexNotAuth'),
    path('changePassword', views.PasswordsChangeView.as_view(template_name='testApp/changePassword.html'), name='changePassword'),
    path('shopList', views.shopList, name='shopList'),
    path('deleteuser/<int:chat_id>', views.DeleteChatUser, name='deleteuser'),
    path('api-auth/', include('rest_framework.urls')),
    path('purchases/<int:recipe_id>/', views.purchases, name='purchases'),
    path('favorites/<int:recipe_id>/', views.favorites, name='favorites'),
    path('edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('send', views.send, name='send'),
    path('DeleteChatUser/<int:recipe_id>/', views.DeleteChatUser, name='DeleteChatUser'),
    path('subscriptions/<int:recipe_id>/', views.subscriptions,
         name='subscriptions'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

