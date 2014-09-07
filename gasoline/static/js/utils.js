var app = app || {};
app.utils = app.utils || {};

// format time
app.utils.formatTime = function() {
    $("time.timeago").timeago();
    $('time.timeago').tooltip({container: 'body', delay: {show: 400}})
}