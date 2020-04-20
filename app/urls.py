from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('class/', views.classes, name="classes"),
    path('class/<pk>/', views.classroom_dashboard, name="classroom"),
    path('class/<pk>/messages/', views.messages, name="messages"),
    path('class/<pk>/settings/', views.classroom_settings, name="classroom-settings"),
    path('class/<pk>/invite/', views.invite_member, name="add-member"),
    path('class/<pk>/invite?=<to>', views.add_member, name="add-member"),
    path('class/<pk>/add/admin/<code>', views.add_admin, name="add-admin"),
    path('class/<pk>/leave/<code>', views.leave_class, name="leave-class"),
    path('class/<pk>/remove/<code>', views.remove_member, name="remove-member"),
    path('class/<pk>/remove/admin/<code>', views.remove_admin, name="remove-admin"),
    path('create/classroom/', views.new_classroom, name="new-classroom"),

]
 