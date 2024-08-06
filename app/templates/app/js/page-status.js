{% comment %}
NOTE: this is a Django template that renders a JavaScript file that is inlined
in the base template. This way it can easily be edited as a JS file, and keeps
the base template simple.

Django template comments are used to reduce the payload.
{% endcomment %}
const errorTag = document.getElementById("error");
const errorText = document.getElementById("error-text");
{# Some response, so can just render page normally. Hide error. #}
function handleSuccess(evt) {
    errorTag.setAttribute("hidden", "true")
    errorText.innerText = "";
}
{# Not an HTTP error like 500. Maybe network error. #}
function handleError(evt) {
    errorTag.removeAttribute("hidden");
    errorText.innerText = "Couldn’t load the page. Check your network connection and try to refresh the page.";
    errorTag.scrollIntoView();
    {# If the currently showing page is an error page (e.g. 404), hide it. #}
    errorPage = document.getElementById("error-page");
    if (errorPage) {
        errorPage.setAttribute("hidden", "true");
    }
}
htmx.on("htmx:afterRequest", handleSuccess);
htmx.on("htmx:responseError", handleSuccess);{# Got an error page, hide #error #}
htmx.on("htmx:sendError", handleError);
htmx.on("htmx:timeout", handleError);
