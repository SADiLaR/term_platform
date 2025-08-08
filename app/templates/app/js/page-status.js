/*{% load i18n %}
{% comment %}
NOTE: this is a Django template that renders a JavaScript file that is inlined
in the base template. This way it can easily be edited as a JS file, and keeps
the base template simple.

Django template comments are used to reduce the payload. Furthermore JavaScript
comments are used to hide Django code from syntax highlighting. Note the use of
the `escapejs` filter when we create JS strings for correct escaping.

This requires care to test well. Scenarios:
 * Fresh load of pages 200 / 404.
 * From freshly loaded 200 click on 404.
 * From freshly loaded 404 click on 200.
 * From a 200 page, click on anything while server is down.
 * From a 404 page, click on anything while server is down.
 * Error page from a proxy inbetween that doesn't contain the HTMX target, e.g.
   a 502 or 429 error raised by Apache. This can be emulated by removing our
   custom 404.html template temporarily and causing a 404. See handleBeforeSwap.
In each case the error box should appear/disappear as necessary. Screen readers
should announce the error as an alert. Support is (as of 2024) not consistently
great.

Furthermore:
 - Test with JS disabled.
 - Test with HTMX not (yet) loaded.

 If an HTMX event takes too long, #loader gives a visual indication and we set
 the text for accessibility purposes. This will be quite chatty if done on
 every request, so we only add the text if it takes longer than a timeout. If
 things are working well, the new content should be announced (and announced in
 good time), so the loader is only needed to confirm that the request is
 submitted if things are taking long enough that the user might have doubts.

 Below we translate a few strings by Django, so we don't need the JavaScript
 i18n infrastructure.
{% endcomment %}
{% trans 'Loading...' as loading %}
{% trans "Error" as error %}
{% trans "Network error" as title %}
{% trans 'Couldn’t load the page. Check your network connection and try to refresh the page.' as message %}
*/
function handleAfterRequest(evt) {
    if (evt.detail.successful) {
        clearTimeout(timeoutID);
        document.getElementById("loader-text").innerText = "";
    } else {
        if (typeof evt.detail.failed === "undefined") {
            //{# Not an error page. Probably network problems. #}
            document.getElementById("error-title").innerText = "{{ title | escapejs }}";
            document.getElementById("error-message").innerText = "{{ message | escapejs }}";
        }
        const errorBlock = document.getElementById("error-block");
        errorBlock.removeAttribute("hidden");
        errorBlock.scrollIntoView();
   }
}

function handleBeforeRequest(evt) {
    document.getElementById("error-block").setAttribute("hidden", "");
    timeoutID = setTimeout(function () {
        document.getElementById("loader-text").innerText = "{{ loading | escapejs }}";
    }, 1000)
}

function handleBeforeSwap(evt) {
    if (!evt.detail.successful && evt.detail.xhr.responseText.indexOf('id="main"') < 0) {
        evt.detail.shouldSwap = false;
        evt.detail.isError = true;
        document.title = "{{ error | escapejs }}";
        document.getElementById("error-title").innerText = "{{ error | escapejs }}";
        document.getElementById("error-message").innerText = evt.detail.xhr.statusText;
    }
}

document.body.addEventListener("htmx:beforeRequest", handleBeforeRequest);
document.body.addEventListener("htmx:afterRequest", handleAfterRequest);
document.body.addEventListener("htmx:beforeSwap", handleBeforeSwap);
