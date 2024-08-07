/*{% comment %}
NOTE: this is a Django template that renders a JavaScript file that is inlined
in the base template. This way it can easily be edited as a JS file, and keeps
the base template simple.

Since we use HTMX, add the event handler as recommended here:
https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#htmx
{% endcomment %}*/
if (typeof window.htmx !== "undefined") {
    htmx.on("htmx:afterSettle", function(detail) {
        if (
            typeof window.djdt !== "undefined"
            && detail.target instanceof HTMLBodyElement
        ) {
            djdt.show_toolbar();
        }
    });
}
