from django.contrib import admin
# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

class LockedDownUserAdmin(admin.ModelAdmin):
    # Block ALL modification attempts
    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path
        protected_urls = [
            path('<path:object_id>/delete/',
                 self.admin_site.admin_view(self.disallow_delete),
                 name='auth_user_delete')
        ]
        return protected_urls + urls

    def disallow_delete(self, request, object_id):
        return HttpResponseForbidden("Deletion not allowed for staff users")

admin.site.unregister(User)
admin.site.register(User, LockedDownUserAdmin)