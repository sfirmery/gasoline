var app = app || {};
app.collections = app.collections || {};

app.collections.Documents = Backbone.Collection.extend({
    model: app.models.Document,
    url: function() {
        return '/api/v1/documents/' + this.space;
    },

    initialize: function(args, options) {
        console.log('init collection');
        console.log(options);
        this.space = options.space
    },

});
