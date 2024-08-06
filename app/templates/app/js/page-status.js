/*{% load i18n %}
{% comment %}
NOTE: this is a Django template that renders a JavaScript file that is inlined
in the base template. This way it can easily be edited as a JS file, and keeps
the base template simple.

Django template comments are used to reduce the payload.

This requires care to test well. Scenarios:
 * Fresh load of pages 200 / 404.
 * From freshly loaded 200 click on 404.
 * From freshly loaded 404 click on 200.
 * From a 200 page, click on anything while server is down.
 * From a 404 page, click on anything while server is down.
In each case the error box should appear/disappear as necessary.

Furthermore:
 - Test with JS disabled.
 - Test with HTMX not (yet) loaded.

{% endcomment %}*/
function handleAfterRequest(evt) {
    const errorBlock = document.getElementById("error-block");
    if (evt.detail.successful) {
        errorBlock.setAttribute("hidden", "true")
    } else {
	if (typeof evt.detail.failed === "undefined") {
            //{# Not an error page. Probably network problems. #}
            const errorTitle = document.getElementById("error-title");
            errorTitle.innerText = "{% trans 'Network error' %}";
            const errorMessage = document.getElementById("error-message");
            errorMessage.innerText = "{% trans 'Couldn’t load the page. Check your network connection and try to refresh the page.' %}";
        }
        errorBlock.removeAttribute("hidden");
        errorBlock.scrollIntoView();
   }
}
if (typeof htmx !== "undefined") htmx.on("htmx:afterRequest", handleAfterRequest);
