from django.contrib import admin
from .models import Post,Comments

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','content','date_posted','author']

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['post','name','email','body','created','updated','active']

admin.site.register(Post,PostAdmin)
admin.site.register(Comments,CommentsAdmin)