from django.contrib import admin
from blog.models import Post,Like
from blog.models import Category

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','content','status')
    
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Like)