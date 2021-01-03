from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetDoneView
from .views import AccLoginView, AccRegisterView, AccActivateView, ProfileView, \
    AccPasswordChangeView, AccPasswordResetView, AccPasswordResetConfirmView
#     ProfileEditView

app_name = 'accounts'

urlpatterns = [
    path('profile/<slug:slug>/', ProfileView.as_view(),
          name='profile'),  # профиль

    path('password_reset/<uidb64>/<token>/',
          AccPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),  # сброс пароля

    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='messages/reset_done.html'),
        name='password_reset_done'),  # уведомление об отправке письма

    path('password_reset/', AccPasswordResetView.as_view(),
         name='password_reset'),  # ввод email для сброса

    path('password_change/', AccPasswordChangeView.as_view(),
         name='password_change'),  # смена пароля

    path('activate/<uid64>/<token>', AccActivateView.as_view(),
         name='activate'),  # активация аккаунта

    path('registration/', AccRegisterView.as_view(),
         name='registration'),  # регистрация

    path('login/', AccLoginView.as_view(), name='login'),  # вход

    path('logout/', LogoutView.as_view(next_page='main:index'),
         name='logout'),  # выход
    #     path('settings/', ProfileEditView.as_view(), name='settings'),
]
