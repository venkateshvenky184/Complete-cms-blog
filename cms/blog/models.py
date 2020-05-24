from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from account.models import User
from tinymce import models as tinymce_models
from bs4 import BeautifulSoup
from django.conf import settings
User = settings.AUTH_USER_MODEL



# from account.models import Profile

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


   



class Post(models.Model):
    statuses = [
        ("D","Draft"),
        ("P","Published"),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length = 250, unique=True,blank=True)
    content = tinymce_models.HTMLField()
    likes  = models.ManyToManyField(User,default = 'None',related_name='likes',blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,choices=statuses)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="blog/post",blank = "True")
    author = models.ForeignKey(User,on_delete= models.CASCADE)

    

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)    
        super().save(*args,**kwargs)


    def get_absolute_url(self):
        return  reverse('post-detail', kwargs = {'slug':self.slug}) 


    def html_to_text(self):
        soup   = BeautifulSoup(self.content, features="html.parser")
        text = soup.get_text()
        return text


    @property
    def num_likes(self):
        return self.likes.count()


LIKE_CHOICES = [
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
]


class Like(models.Model):
    user =  models.ForeignKey(User,on_delete= models.CASCADE)
    post =  models.ForeignKey(Post,on_delete= models.CASCADE)      
    value = models.CharField(choices=LIKE_CHOICES, default='like', max_length=10)



    def __str__(self):
        return str(self.post)