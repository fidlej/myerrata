(function(w, d, e) {
    if (w.MyErrata) {
        w.MyErrata.toggleEditing();
    } else {
        w.MyErrata = {
            host:'http://www.myerrata.com',
            start:true
        };
        e = d.createElement('script'); e.type = 'text/javascript';
        e.src = w.MyErrata.host + '/static/js/myerrata.min.js';
        (d.getElementsByTagName('head')[0]||d.body).appendChild(e);
    }
})(window, document, '0.1');
