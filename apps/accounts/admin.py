from django.contrib import admin

from apps.accounts.models import Account, Word

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'account_id', 'status', 'follower_count', 'followed_by_count')
    list_filter = ('status',)

class WordAdmin(admin.ModelAdmin):
    list_display = ('word',)

admin.site.register(Account, AccountAdmin)
admin.site.register(Word, WordAdmin)