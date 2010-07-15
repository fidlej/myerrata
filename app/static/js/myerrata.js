
(function() {
// It is OK to load myerrata.js twice.
if (window.MyErrata && window.MyErrata.toggleEditing) {
    window.MyErrata.toggleEditing();
    return;
}

// A simple placeholder for toggleEditing().
// It will be redefined after loading of jQuery.
window.MyErrata = window.MyErrata || {};
window.MyErrata.toggleEditing = function() {
    window.MyErrata.start = true;
}

function logError() {
    if (window.console && window.console.error) {
        window.console.error('error', arguments);
    } else {
        var args = Array.prototype.slice.call(arguments, 0);
        var msg = args.join(', ');
        setTimeout(function() {
            throw new Error(msg);
        }, 0);
    }
}

var mainCode = function($) {
// Default options
window.MyErrata = $.extend({
        host: 'http://www.myerrata.com',
        start: false
    }, window.MyErrata);

var state = {
    editingEnabled: false,
    fixes: undefined
};

var startEditing = (function() {
    function rebind(jq, eventType, handler) {
        return jq.unbind(eventType).bind(eventType, handler);
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

        if (callback) {
            xhr.onload = function() {
                var result = xhr.responseText;
                if (dataType === 'json') {
                    result = $.parseJSON(xhr.responseText);
                }
                callback(result);
            };
        }
        xhr.onerror = logError;
        xhr.send($.param(data));
    }

    /**
     * Posts the data to another domain via a hidden iframe.
     * Nested data are not supported.
     */
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

    // --- Event callbacks.
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
            if (state.editingEnabled) {
                rebind(wrapper, 'click.myerrata', addSubmitButtons);
            } else {
                // Disabling editing also on the arrived marked text.
                wrapper.find('*').attr('contentEditable', false);
            }
        }

        saveButton.insertAfter(this)
            .click(function() {
                wrapper.find('.myerrata-space').each(function() {
                    var appended = $(this).text();
                    $(this).text($.trim(appended));
                });

                var newText = wrapper.clone(false)
                    .find('del').remove()
                    .end().text();
                var pos = wrapper.data('pos.myerrata') || 0;
                var page_order = wrapper.data('pageOrder.myerrata');
                var target = window.MyErrata.host + '/api/save';
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
                            wrapper.html(markEditable(data.marked));
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
        rebind(wrapper, 'click.myerrata', ignoreClick);
        return false;
    }

    // --- Helper functions.
    function markEditable(markedText) {
        // The extra space allows to add unstyled text.
        var suffix = '<span class="myerrata-space"> </span></span>';
        return '<span contenteditable="true">' + markedText + suffix;
    }

    function createStopButton() {
        $('<div id="myerrata_stopbutton">Stop Editing X</div>').hide()
            .click(stopEditing)
            .appendTo(document.body);
    }

    // Applies the existing fixes
    function applyFixes(fixes, origTextWrappers) {
        var gone = [];
        var ungone = [];
        // Ignore an incompatible toJSON from Prototype.js.
        gone.toJSON = ungone.toJSON = undefined;

        for (var i = 0, fix; fix = fixes[i]; i++) {
            var wrapperEl = (origTextWrappers[fix.orig] || [])[fix.pos];
            if (wrapperEl) {
                $(wrapperEl).data('origText.myerrata', fix.orig)
                    .html(markEditable(fix.marked));
                if (fix.gone) {
                    ungone.push({
                        orig: fix.orig,
                        pos: fix.pos
                    });
                }
            } else {
                if (!fix.gone) {
                    gone.push({
                        orig: fix.orig,
                        pos: fix.pos
                    });
                }
            }
        }

        if (gone.length === 0 && ungone.length === 0) {
            return;
        }

        // Only the newer browsers will report gone fixes.
        if (window.JSON && window.JSON.stringify && isCrossPostSupported()) {
            var target = window.MyErrata.host + '/api/update-gone';
            var data = window.JSON.stringify({
                url: window.location.href,
                gone: gone,
                ungone: ungone
            });
            crossPost(target, {json: data}, null, null);
        }
    }

    function createWrappers(fixes) {
        var textNodes = $('*', document.body).not('script, iframe, .myerrata-noneditable').add(document.body).contents().filter(function() {
            return this.nodeType === 3 && $.trim(this.nodeValue) !== '';
        });

        // Wraps all text nodes into
        // a non-editable <div/> and an editable <span/>.
        // The editable <span/> could be modified or duplicated by the user.
        //
        // A <div/> is used instead <span/> to get around a FF bug:
        // https://bugzilla.mozilla.org/show_bug.cgi?id=546662
        textNodes.each(function() {
            var wrapper = $('<div style="display:inline" class="myerrata-text"><span /></span>');
            wrapper.insertBefore(this);
            wrapper.children().append(this);
        });

        var origTextWrappers = {};
        textNodes.each(function(i) {
            var wrapperEl = this.parentNode.parentNode;
            var list = origTextWrappers[this.nodeValue] || [];
            list.push(wrapperEl);
            origTextWrappers[this.nodeValue] = list;
            $.data(wrapperEl, 'pageOrder.myerrata', i);
        });
        textNodes = null;

        // Remembering wrappers with non-zero pos
        for (var orig in origTextWrappers) {
            var nodes = origTextWrappers[orig];
            for (var i = 1, wrapperEl; wrapperEl = nodes[i]; i++) {
                $(wrapperEl).data('pos.myerrata', i);
            }
        }

        return origTextWrappers;
    }

    var origTextWrappers = undefined;

    return function() {
        state.editingEnabled = true;
        if (origTextWrappers === undefined) {
            origTextWrappers = createWrappers(state.fixes);
            createStopButton();
        }
        $("#myerrata_stopbutton").show('fast');

        if (state.fixes === undefined) {
            // We will wait for the Ajax result.
            return;
        } else if (state.fixes !== null) {
            applyFixes(state.fixes, origTextWrappers);
            origTextWrappers = null;
            state.fixes = null;
        }

        $('.myerrata-text').bind('mouseenter.myerrata', lightBg)
            .bind('mouseleave.myerrata', revertBg)
            .bind('click.myerrata', addSubmitButtons)
            .find('*').attr('contentEditable', true);
    };
})();

function fetchFixes() {
    $.ajax({
        url: window.MyErrata.host + '/api/fixes',
        data: {
            url: window.location.href
        },
        dataType: 'jsonp',
        error: logError,
        success: function(data) {
            state.fixes = data.fixes;
            if (state.editingEnabled) {
                startEditing();
            }
        }
        });
}

function insertDefaultCss() {
    var head = $('head').eq(0);
    if (head.length < 1) {
        head = $('<head/>').insertBefore(document.body);
    }
    $('<style type="text/css">\n' +
    '.myerrata-hover { background-color: #95d6ff}\n' +
    '.myerrata-text del { color: #ff6347}\n' +
    '.myerrata-text ins { background-color: #97FF97; color: #003800; text-decoration: none}\n' +
    '#myerrata_stopbutton { position: fixed; top: 0; right: 0;' +
        'border: 2px groove black; padding: 0 5px 2px;' +
        'background-color: red; color: white;' +
        'font-family: sans-serif; font-size: 10pt; font-weight: bold}\n' +
    '</style>').prependTo(head);
}

function stopEditing() {
    state.editingEnabled = false;
    $("#myerrata_stopbutton").hide();
    $('.myerrata-text').unbind('.myerrata')
        .find('*').attr('contentEditable', false);
}

window.MyErrata.toggleEditing = function() {
    if (state.editingEnabled) {
        stopEditing();
    } else {
        startEditing();
    }
};

$(document).ready(function() {
    fetchFixes();
    insertDefaultCss();
    if (window.MyErrata.start) {
        startEditing();
    }
});
// Firefox 3.5 or older don't have document.readyState.
// Let's assume that the bookmarklet is clicked after onload.
// http://dev.jquery.com/ticket/4196
if (typeof document.readyState === 'undefined') {
    $.ready();
}

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

// We need jQuery 1.4.1+ to have $.parseJSON.
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


