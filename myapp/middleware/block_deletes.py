# myapp/middleware/block_deletes.py
from django.http import HttpResponseForbidden

class BlockStaffDeletesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.user.is_staff and not request.user.is_superuser and
            request.method == 'DELETE'):
            return HttpResponseForbidden("Staff cannot delete records")
        return self.get_response(request)