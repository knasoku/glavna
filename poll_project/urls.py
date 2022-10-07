from django.contrib import admin
from django.urls import path, include, reverse_lazy
from poll import views as poll_views
from django.contrib.auth import views as auth_views

app_name = 'poll'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', poll_views.home, name='home'),
    path('upravitel/', include('upravitel.urls')),
    path('vote/<poll_id>/', poll_views.vote, name='vote'),
    path('result/<poll_id>/', poll_views.result, name='result'),
    path('pollpage/', poll_views.pollPage, name='pollPage'),
    path('register/', poll_views.registerPage, name='register'),
    path('login/', poll_views.loginPage, name='login'),
    path('logout/', poll_views.logoutUser, name='logout'),
    path('user/', poll_views.userPage, name='user-page'),
    path('contact/', poll_views.contact, name='contact'),
    path('account/', poll_views.accountSettings, name='account'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='poll/change_password.html', success_url=reverse_lazy('passwordChanged')) ,name='change_password'),
    path('passwordchanged/', poll_views.passwordChanged, name='passwordChanged'),
    path('announcementpage/', poll_views.announcementPage, name='announcementPage'),
    path('announcement_view/<announcement_id>/', poll_views.announcementView, name='announcement_view'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="poll/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="poll/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="poll/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="poll/password_reset_done.html"), 
        name="password_reset_complete"),

]
