from django.shortcuts import render,redirect
from django.http import HttpResponse
from blog.models import Post,Category,Like
from blog.models import Category
from blog.forms import ContactForm
from django.views.generic import FormView
from blog.forms import Postform
from  django.views import View
from django.views.generic import ListView,DetailView,FormView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from account.models import User as User
from django.db.models import Q

# Create your views here.

def index(request, *args, **kwargs):
    posts = Post.objects.filter(status = "P")
    category = Category.objects.all()
    user = request.user()

    context = {
    'posts' : posts,
    'category' : category,
    'user':user
    }
    return render(request, 'stories.html', context)

def like_post(request):
    user = request.user
    if request.method =="POST":
        posts_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=posts_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)    

        like,created = Like.objects.get_or_create(user=user, post_id=posts_id)  

        if not created:
            if like.value=='Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'   

        like.save()           
    return redirect('index')


def post_form_view(request, *args, **kwargs):
    if request.method =="GET":
        form  = Postform()
        return render (request,'post.html',context ={'form':form})
     
    else:
        form  = Postform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Thank You")
        else:
            return render (request,'post.html',context ={'form':form}) 

def post_edit_form_view(request, id, *args, **kwargs):
    try:
        post = Post.objects.get(id = id)   

    except:
        return HttpResponse("Invalid Post ID")     

    if request.method =="GET":
        form = Postform(instance = post)
        return render(request, 'post.html',context ={'form':form})

    else:
        form = Postform(request.POST,request.FILES,instance = post)
        if form.is_valid():
            form.save()

        return render(request, 'post.html',context ={'form':form})

def category_buttons(request, id, *args, **kwargs):
    category = Category.objects.all()
    posts = Post.objects.filter(category__id = id)
    context = {
    'posts' : posts,
    'category': category,
    }
    return render(request, 'stories.html', context)          

class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(status = "P")
    template_name = 'stories.html'
    context_object_name = 'posts'


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class PostDetailView(LoginRequiredMixin,DetailView):
    login_url ='login'
    model = Post
    # queryset = Post.objects.filter(status = "P")
    template_name = 'details.html'

   
class PostFormView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    # model = Post 
    # fields = ['title', 'content', 'status', 'category', 'image'] 
    # success_url = 'posts'
    login_url = 'login'
    permission_required = 'blog.add_post'
    template_name = 'post.html'
    form_class = Postform
   
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = User.objects.get(username= self.request.user)
        kwargs.update({'initial':{'author': user}})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   


class PostFormUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = "login"
    permission_required = 'blog.change_post'
    model = Post
    form_class = Postform
    template_name = 'post.html'  


    def test_func(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        post = Post.objects.get(slug = slug)
        if self.request.user.get_username() == post.author.get_username():
            return True
        else:
            return False

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = User.objects.get(username= self.request.user)
        kwargs.update({'initial':{'author': user}})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class SearchPostView(ListView):
    model = Post
    queryset = Post.objects.filter(status = "P")
    template_name = "stories.html"
    context_object_name = "posts"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Post.objects.filter(title__icontains=query)
        return HttpResponse("Product not found")






# def contact_view(request,*args,**kwargs):
#     # print(request.GET)
#     # print(request.POST)

#     if request.method == 'GET':
#         form = ContactForm()  
#         return render(request, 'contact.html',context ={'form':form})
#     else:
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             return HttpResponse("Thank You Visit Again")
#         else:
#             return render(request, 'contact.html',context ={'form':form})

#     form = ContactForm()
#     return render(request, 'contact.html',context ={'form':form})    

class ContactFormView(FormView):
    form_class = ContactForm
    success_url = "contact"
    template_name = 'contact.html'

    def form_valid(self,form):
        # print(form.cleaned_data)
        return super().form_valid(form)
 


def home(request, *args, **kwargs):
    posts = Post.objects.filter(status = "P")
    category = Category.objects.all()
    user = request.user()

    context = {
    'posts' : posts,
    'category' : category,
    'user':user
    }
    return render(request, 'stories.html', context)




























        