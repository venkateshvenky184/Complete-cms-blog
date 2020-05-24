
from django.urls import path,re_path
from blog.views import index
from blog.views import category_buttons,SearchPostView
from blog.views import post_form_view,post_edit_form_view,PostListView,PostDetailView,PostFormView,ContactFormView,PostFormUpdateView,like_post







urlpatterns = [
  
    path('',PostListView.as_view(),name='index'),
    path('',PostListView.as_view(),name='home'),
    path('filter/<int:id>', category_buttons, name='category_buttons'),
    path('search', SearchPostView.as_view(), name='search'),
    path('like',like_post,name='like_post'),
    path('posts',PostFormView.as_view(),name='posts'),
    path('posts/<int:id>/',post_edit_form_view),
    path('contact',ContactFormView.as_view()),
    path('posts/<slug:slug>',PostFormUpdateView.as_view()),
    path('<slug:slug>',PostDetailView.as_view(),name='post-detail'),
    
]

















































































