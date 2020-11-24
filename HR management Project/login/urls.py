from django.contrib import admin
from django.urls import path
from login import views
from django.urls import path
from .views import View,EntryShow
urlpatterns = [
   path("",views.index,name='login'),
   path("reset",views.reset,name='reset'),
   path("home",views.home,name='home'),
   path("milestones",views.milestones,name='milestones'),
   path("workbench",views.workbench,name='workbench'),
   path("profile",views.profile,name='profile'),
   path("logout",views.logout,name='logout'),
   path("edit",views.edit,name='edit'),
   path("feedback",views.feedback,name='feedback'),
   path('homemade/',views.View,name='ViewYourWork'),
   path('entryshow/',views.EntryShow,name='showthe work'),
#    path('savetimer/',)

]
