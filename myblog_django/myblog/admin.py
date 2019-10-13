# -*- coding=utf-8 -*-
from django.contrib import admin
from myblog.models import *

class AdAdmin(admin.ModelAdmin):
    """docstring for LinkAdmin"""
    list_display = ('title', 'desc', 'date_published')
    list_display_links = ('title', 'desc',)
    fieldsets = (
        ('基础设置', {
            'fields': ('title', 'desc',)
            }
        ),
        ('高级设置', {
            'classes': ('collapse'),
            'fields': ('image_url', 'callback_url', 'index',)
            }
        )
    )



class ArticleAdmin(admin.ModelAdmin):
    """docstring for ArticleAdmin"""
    class Media:
        js = (
            '/static/js/kindeditor-4.1.7/kindeditor-min.js',
            '/static/js/kindeditor-4.1.7/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.7/config.js',
        )
        
        
# Register your models here.
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Cateory)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
#admin.site.register(Links)
#admin.site.register(Ad, AdAdmin)
