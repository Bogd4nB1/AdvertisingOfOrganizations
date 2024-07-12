from django.contrib import admin
from .models import Organitathion, AdressOrg, Tag, Comment, Account

@admin.register(Organitathion)
class OrganitathionAdmin(admin.ModelAdmin):
    list_display = ['name', 'web_site', 'phone', 'adress', 'created_at', 'short_description',]

@admin.register(AdressOrg)
class AdressAdmin(admin.ModelAdmin):
    list_display = ['country', 'region', 'city', 'street',]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {"slug": ("title",)} 

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['organitathion', 'created_at', 'author',]

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'organitathion',]

