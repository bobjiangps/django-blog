from django.contrib import admin
from .models import Post,Tag,Category
#import xadmin


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)

#xadmin.site.register(Category)
#xadmin.site.register(Tag)
#xadmin.site.register(Post)
