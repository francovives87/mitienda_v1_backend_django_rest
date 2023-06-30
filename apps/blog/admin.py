from django.contrib import admin
from .models import (Category_blog,Entry,Tag,Images,Comment_entry)

# Register your models here.


admin.site.register(Category_blog)
admin.site.register(Entry)
admin.site.register(Tag)
admin.site.register(Images)
admin.site.register(Comment_entry)