(function(w, d, e) {
    if (w.MyErrata) {
        w.MyErrata.toggleEditing();
    } else {
        w.MyErrata = {
            host:'http://frontend:9999',
            start:true
        };
        e = d.createElement('script'); e.type = 'text/javascript';
        e.src = w.MyErrata.host + '/static/js/myerrata.js';
        (d.getElementsByTagName('head')[0]||d.body).appendChild(e);
    }
})(window, document, '0.1');
