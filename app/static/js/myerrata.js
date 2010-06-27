
(function() {
var mainCode = function($) {
// Default options
var MyErrata = $.extend({
        host: 'http://www.myerrata.com',
        start: false
    }, window.MyErrata);

var startEditing = (function() {
    $.fn.rebind = function(eventType, handler) {
        return this.unbind(eventType).bind(eventType, handler);
    }

    function isCrossPostSupported() {
        return ((window.XMLHttpRequest &&
                'withCredentials' in new XMLHttpRequest) ||
            typeof window.XDomainRequest !== 'undefined');
    }

    /**
     * Submits bigger data to a CORS enabled URL.
     * We cannot use JSONP, because the data could be too big for GET.
     */
    function crossPost(url, data, callback, dataType) {
        var method = 'POST';
        var xhr = new XMLHttpRequest();
        if ('withCredentials' in xhr) {
            xhr.open(method, url, true);
            // Make the Content-Type to be a "simple header"
            // as defined by CORS.
            // http://dev.w3.org/2006/waf/access-control/
            xhr.setRequestHeader('Content-Type',
                    'application/x-www-form-urlencoded');
        } else if (typeof window.XDomainRequest !== 'undefined') {
            xhr = new window.XDomainRequest();
            xhr.open(method, url);
        } else {
            alert('Your browser is too old. It does not support Cross-Origin Resource Sharing.');
            return;
        }

        xhr.onload = function() {
            var result = xhr.responseText;
            if (dataType === 'json') {
                result = $.parseJSON(xhr.responseText);
            }
            callback(result);
        };
        xhr.onerror = logError;
        xhr.send($.param(data));
    }

    function asyncFormPost(url, data) {
        var iframe = $('#myerrata_iframe');
        if (iframe.length !== 1) {
             iframe = $('<iframe id="myerrata_iframe" name="myerrata_iframe" src="about:blank" style="display:none"/>');
            iframe.appendTo(document.body);
        }

        var form = $('#myerrata_form');
        if (form.length !== 1) {
            form = $('<form id="myerrata_form" method="POST" target="myerrata_iframe" style="display:none"/>');
            form.appendTo(document.body);
        }

        form.attr('action', url);
        form.empty();
        for (var name in data) {
            var input = $('<input type="hidden"/>');
            input.attr('name', name);
            input.attr('value', data[name]);
            form.append(input);
        }

        form.submit();
        // We cannot remove the form quickly. It would cancel the request.
    }

    function logError() {
        if (window.console && window.console.error) {
            window.console.error('error', arguments);
        }
    }

    // Event callbacks.
    function lightBg() {
        $(this).addClass('myerrata-hover');
    }

    function revertBg() {
        $(this).removeClass('myerrata-hover');
    }

    function ignoreClick() {
        return false;
    }

    function addSubmitButtons() {
        var wrapper = $(this);
        var unchangedHtml = wrapper.html();
        var origText = wrapper.data('origText.myerrata');
        if (!origText) {
            origText = wrapper.text();
            wrapper.data('origText.myerrata', origText);
        }

        var saveButton = $('<button type="button">Save</button>');
        var cancelButton = $('<button type="button">Cancel</button>');

        function removeButtons() {
            saveButton.remove();
            cancelButton.remove();
            wrapper.rebind('click.myerrata', addSubmitButtons);
        }

        saveButton.insertAfter(this)
            .click(function() {
                var newText = wrapper.clone(false).find('del').remove()
                    .end().text();
                //TODO: detect the origText position.
                var pos = 0;
                // TODO: use more stable page_order
                var page_order = wrapper.offset().top;
                var target = MyErrata.host + '/api/save';
                var data = {
                        url: window.location.href,
                        orig: origText,
                        'new': newText,
                        pos: pos,
                        page_order: page_order
                };

                if (isCrossPostSupported()) {
                    crossPost(target, data,
                        function(data) {
                            wrapper.html(data.marked);
                            removeButtons();
                        },
                        'json'
                    );
                } else {
                    // Falling back to iframe+form post without callback.
                    asyncFormPost(target, data);
                    removeButtons();
                }

                return false;
            });

        cancelButton.insertAfter(saveButton)
            .click(function() {
                wrapper.html(unchangedHtml);
                removeButtons();
                return false;
            });

        // Prevent to visit a URL.
        wrapper.rebind('click.myerrata', ignoreClick);
        return false;
    }

    function createWrappers() {
        // Wraps all non-empty text nodes into
        // non-editable and editable <span/>.
        // The editable <span/> could be modified or duplicated by the user.
        //
        // A <div/> is used instead <span/> to get around a FF bug:
        // https://bugzilla.mozilla.org/show_bug.cgi?id=546662
        var textNodes = $("*", document.body).not('script').not('.myerrata-noneditable').add(document.body).contents().filter(function() {
            return this.nodeType === 3 && $.trim(this.nodeValue) !== '';
        }).wrap('<div style="display:inline" class="myerrata-text"><span contenteditable="true" /></span>');
        return textNodes.parent().parent();
    }

    return function() {
        var wrappers = createWrappers();
        wrappers.hover(lightBg, revertBg).bind(
                'click.myerrata', addSubmitButtons);
    };
})();

function insertDefaultCss() {
    var head = $('head').eq(0);
    if (head.length < 1) {
        head = $('<head/>').insertBefore(document.body);
    }
    $('<style type="text/css">\n' +
    '.myerrata-hover { background-color: #95d6ff}\n' +
    '.myerrata-text del { color: red}\n' +
    '.myerrata-text ins { color: green}\n' +
    '</style>').prependTo(head);
}

$(document).ready(function() {
    insertDefaultCss();
    if (MyErrata.start) {
        startEditing();
    }
});

};

// Startup
(function() {

// Returns true if the major version number is equal
// and the other numbers are greater-or-equal.
function isCompatibleGeVersion(v1, v2) {
    var numbers1 = v1.split('.');
    var numbers2 = v2.split('.');
    if (numbers1[0] !== numbers2[0]) {
        return false;
    }
    if (numbers1[1] < numbers2[1]) {
        return false;
    }
    if (numbers1[1] === numbers2[1] && (numbers1[2]||0) < (numbers2[2]||0)) {
        return false;
    }
    return true;
}

// We need jQuery 1.4.1 to have $.parseJSON.
if (window.jQuery && isCompatibleGeVersion(window.jQuery.fn.jquery, '1.4.1')) {
    mainCode(window.jQuery);
} else {
    var script = document.createElement('script');
    script.src = 'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js';
    var head = document.getElementsByTagName('head')[0]||document.body;
    var done = false;
    // Attach handlers for all browsers (taken from jQuery).
    script.onload = script.onreadystatechange = function() {
        if (!done && (!this.readyState ||
                    this.readyState === 'loaded' ||
                    this.readyState === 'complete')) {
            done = true;
            script.onload = script.onreadystatechange = null;
            mainCode(window.jQuery.noConflict(true));
        }
    };

    head.appendChild(script);
}
})();

})();


