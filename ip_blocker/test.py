import unittest
from django.http import HttpResponseForbidden
from .middleware import BlockIpMiddleware


class Request:
    def __init__(self) -> None:
        self.session = {}
        self.META = {}

    def set_ip(self, ip: str) -> None:
        self.META["REMOTE_ADDR"] = ip


class TestBlockIpMiddleware(unittest.TestCase):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__()
        self.req = Request()
        self.middleware = BlockIpMiddleware()
        
    def test_session_banned(self):
        self.req.session["is_banned"] = True
        result = self.middleware.process_request(self.req)
        self.assertEqual(result,HttpResponseForbidden())


if __name__ == "__main__":
    unittest.main()
