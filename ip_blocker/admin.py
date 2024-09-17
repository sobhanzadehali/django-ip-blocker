from django.contrib import admin
from .models import BlockedIp


@admin.register(BlockedIp)
class BlockedIpAdmin(admin.ModelAdmin):
    pass
