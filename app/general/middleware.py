from django.utils.cache import patch_vary_headers


class ExtraVaryMiddleware:
    """Ensure HTML pages vary on HX-Request

    This is needed so that incomplete responses based on base_htmx.html are not
    reused as full-page responses, for example on browser restore of a page."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if "text/html" in response.headers.get("Content-Type", ""):
            patch_vary_headers(response, ["HX-Request"])
        return response
