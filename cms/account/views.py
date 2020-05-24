from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from account.forms import SignUpForm,UserUpdateForm, ProfileUpdateForm
from account.models import Profile
from blog.models import Post
# Create your views here.


class UserCreateView(CreateView):
    template_name = "account/signup.html"
    form_class = SignUpForm
    success_url = "/blogs"


def profile_page_view(request):
    user = request.user.id
    author_posts = Post.objects.filter(author_id=user)
    context = {
        'author_posts':author_posts
    }
    return render(request, 'account/profile.html',context)    



@login_required
def profile_page(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': user_form,
        'p_form': profile_form
    }

    return render(request, 'account/profile_update.html', context)    