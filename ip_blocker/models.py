from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete


class BlockedIp(models.Model):
    address = models.CharField(max_length=39)
    reason = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"address {self.address} blocked for: {self.reason}"

    class Meta:
        db_table = "blocked_ip_addresses"
        verbose_name = "blocked IP"
        verbose_name_plural = "blocked IPs"


def set_cache(sender, instance, **kwargs):
    blocked_ips = [i.address for i in BlockedIp.objects.all()]
    cache.set("blockedip:list",blocked_ips)


post_save.connect(set_cache, sender=BlockedIp)
post_delete.connect(set_cache, sender=BlockedIp)
