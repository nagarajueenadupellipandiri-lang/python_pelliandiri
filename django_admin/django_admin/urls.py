from django.contrib import admin
from django.urls import path
from admin_app import views
from admin_app import front_view

urlpatterns = [     
    path("admin/", views.login_view, name="login"),
    path("login/", views.login_view, name="login" ),     
    path("dashboard/", views.dashboard_view, name="dashboard" ), 
    path("logout/", views.logout_view, name="logout" ), 
    path("users/", views.user_view, name="users"), 
    path("occupationAsWorking/", views.occupations_as_working, name="occupationAsWorking" ),
    path("occupationsAsNotWorking/", views.occupations_as_not_working, name="occupationsAsNotWorking" ),
    path("createUser/", views.createUser, name="createUser"),
    path("banners/", views.banners_view, name="banners"),
    path("packageCategories/", views.pacakges_view, name="packageCategories"),
    path("packages/", views.subPacakges_view, name="packages"),
    path("liveEvents/", views.liveEvents_view, name="liveEvents"),
    
    # go to front end
    path("reactApplication/", front_view.home, name="reactApplication"),
]
