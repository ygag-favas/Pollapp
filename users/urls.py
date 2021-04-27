from django.urls import path, reverse_lazy, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm, CustomEmailValidationOnForgotPassword

app_name = 'users'

urlpatterns = [

    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('activate/<uidb64>/<token>/', views.Activate.as_view(),
         name='activate'),

    path('login/', auth_views.LoginView.as_view(
        template_name='account/login.html', redirect_field_name='next',
        authentication_form=LoginForm,
        extra_context={
            'next': 'polls:index',
        },
    ), name='signin'),

    path('logout', views.LoginOutView.as_view(), name='logout'),

    path(
        'change-password/', views.CustomPasswordChangeView.as_view(
            template_name='account/change-password.html',
            success_url=reverse_lazy('polls:index'),
        ),
        name='change_password'
    ),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name="account/password/reset_password.html",
        email_template_name='account/password/password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done'),
        form_class=CustomEmailValidationOnForgotPassword),
         name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name="account/password/password_reset_done.html"),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="account/password/password_reset_confirm.html",
             success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="account/password/password_reset_complete.html"),
         name='password_reset_complete'),

    path('api/', include('users.api.urls')),

]
