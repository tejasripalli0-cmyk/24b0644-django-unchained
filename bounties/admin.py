from django.contrib import admin
from .models import Bounty


@admin.register(Bounty)
class BountyAdmin(admin.ModelAdmin):
    list_display = ('target_name', 'reward', 'status', 'owner', 'created_at')
    search_fields = ('target_name', 'owner__username')
    list_filter = ('status', 'created_at')
