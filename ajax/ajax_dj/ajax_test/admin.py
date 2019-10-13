from django.contrib import admin
from ajax_test.models import search

class search_admin(admin.ModelAdmin):
    """docstring for search_admin"""
    list_display = ('key_word', 'times')
        

# Register your models here.
admin.site.register(search, search_admin)
