/*{% load i18n %}
{% comment %}
NOTE: this is a Django template that renders a JavaScript file that is inlined
in the base template. This way it can easily be edited as a JS file, and keeps
the base template simple.

Django template comments are used to reduce the payload. Furthermore JavaScript
comments are used to hide Django code from syntax highlighting. Note the use of
the `escapejs` filter when we create JS strings for correct escaping. Check
that wording corresponds to the error templates in 404.html, etc.

This is mostly about error handling when HTMX is active, to ensure:
 * That server errors are swapped in correctly if they can.
 * That proxy errors that can't be swapped in, are not swapped in.
 * That network errors are handled, since the browser won't show an error.

This requires care to test well. Scenarios:
 * Fresh load of pages 200 / 404.
 * From freshly loaded 200 click on 404.
 * From freshly loaded 404 click on 200.
 * From a 200 page, click on anything while server is down.
 * From a 404 page, click on anything while server is down.
 * Error page from a proxy inbetween that doesn't contain the HTMX target, e.g.
   a 502 or 429 error raised by Apache. This can be emulated by removing our
   custom 404.html template temporarily and causing a 404. See handleBeforeSwap.
 * With/without DEBUG, since DEBUG error pages are different from our own.
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

We avoid the HTMX API, since this could execute before that is available.

 Below we translate a few strings by Django, so we don't need the JavaScript
 i18n infrastructure.
{% endcomment %}
{% trans "Too many requests" as e429 %}
{% trans "Upstream server error" as e502 %}
{% trans "Service unavailable" as e503 %}
{% trans "Upstream server timeout" as e504 %}
{% trans 'Loading...' as loading %}
{% trans "Error" as error %}
{% trans "Network error" as network_title %}
{% trans 'Couldn’t load the page. Check your network connection and try to refresh the page.' as network_message %}
{% trans "Something unexpected prevented the server from fulfilling the request." as server_message %}
*/

get = document.getElementById.bind(document);
eBlock = get("error-block");
eTitle = get("error-title");
eMessage = get("error-message");
loader = get("loader-text");
messages = {
    429: "{{ e429 | escapejs }}",
    502: "{{ e502 | escapejs }}",
    503: "{{ e503 | escapejs }}",
    504: "{{ e504 | escapejs }}"
 };

function handleAfterRequest(evt) {
    if (evt.detail.successful) {
        clearTimeout(timeoutID);
        loader.innerText = "";
    } else {
        if (typeof evt.detail.failed === "undefined") {
            /*{# Not an error page. Probably network problems. #}*/
            eTitle.innerText = "{{ network_title | escapejs }}";
            eMessage.innerText = "{{ network_message | escapejs }}";
        }
        eBlock.removeAttribute("hidden");
        eBlock.scrollIntoView();
   }
}

function handleBeforeRequest(evt) {
    eBlock.setAttribute("hidden", "");
    timeoutID = setTimeout(function () {
        loader.innerText = "{{ loading | escapejs }}";
    }, 1000)
}

function handleBeforeSwap(evt) {
    detail = evt.detail;
    if (!detail.successful && detail.xhr.responseText.indexOf('id="main"') < 0) {
        detail.shouldSwap = false;
        detail.isError = true;
        e = messages[detail.xhr.status] || "{{ error | escapejs }}";
        document.title = e;
        eTitle.innerText = e + " (" + detail.xhr.status + ")";
        eMessage.innerText = "{{ server_message | escapejs }}";
    }
}

document.body.addEventListener("htmx:beforeRequest", handleBeforeRequest);
document.body.addEventListener("htmx:afterRequest", handleAfterRequest);
document.body.addEventListener("htmx:beforeSwap", handleBeforeSwap);
