# dBSolutionV3/middleware/tenant_required.py
class TenantRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not hasattr(request.user, "societe"):
            raise RuntimeError("Utilisateur sans tenant associé")
        return self.get_response(request)
