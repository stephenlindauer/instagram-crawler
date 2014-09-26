from django.contrib import admin

from apps.accounts.models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'account_id', 'status', 'follower_count', 'followed_by_count')

admin.site.register(Account, AccountAdmin)