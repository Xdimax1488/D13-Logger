from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','text_news')

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(CategorySubscribers)
