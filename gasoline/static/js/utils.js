var app = app || {};
app.utils = app.utils || {};

// format time
app.utils.formatTime = function(el) {
    el = typeof el !== 'undefined' ? $(el).find('time.timeago') : $('time.timeago')
    el.timeago();
    el.tooltip({container: 'body', delay: {show: 400}})
};

app.utils.getDateTime = function() {
    return new Date().toJSON()
};