from .models import BlockedIp
from django.core.cache import cache
from django.http import HttpResponseForbidden



class IpHelper:
    @staticmethod
    def get_ip(request) -> str:
        """returns ip address of given request object"""
        return request.META.get("REMOTE_ADDR")


class BlockIpMiddleware(object):
    def process_request(self, request):
        is_banned = request.session["is_banned"]
        
        if not is_banned:
            ip = IpHelper.get_ip(request)  # request ip
            blocked = []
            try:
                blocked = cache.get("blockedip:list") # list of blocked ip from django cache
                if blocked is None:
                    blocked = [i.address for i in BlockedIp.objects.all()]
                    cache.set("blockedip:list", blocked)
            except Exception as e:
                print("something went wrong while getting blocked ip from cache", e)
            

            if ip in blocked:
                is_banned = True
                request.session["is_banned"] = True
            
        if is_banned:
            return HttpResponseForbidden("access denied!")
