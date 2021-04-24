from django.conf import settings
from django.urls import path
from . import views
from .views import *
app_name="Blogapp"
urlpatterns = [
    path('',views.index,name="index"),
    path('blog/',views.blog,name="blog"),
    path('post/<id>/',views.post,name="post"),
    path('post/update/<id>/',views.post_update,name="update"),
    path('post/delete/<id>/',views.post_delete,name="delete"),
    path('create/',views.post_create,name="create"),
    path('search/',views.search,name="search"),  
    path('vote/up/<id>/',views.post_vote_up,name="post-vote-up"),  
    path('vote/down/<id>/',views.post_vote_down,name="post-vote-down"),
    path("contact/",views.Contact,name="contact"),
    path("profile/<id>",views.profile,name="profile"),
    # Admin Urls
    path('dashboard/posts/',views.Admin,name="admin"),
    path('dashboard/posts/update/<id>/',views.Admin_Post_Update,name="admin-update"),
    path('dashboard/posts/delete/<id>/',views. Admin_Post_Delete,name="admin-delete"),    
    path('dashboard/user/delete/<id>/',views. Admin_User_Delete,name="admin-user-delete"),    
]


