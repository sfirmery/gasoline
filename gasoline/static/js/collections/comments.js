var app = app || {};
app.collections = app.collections || {};

app.collections.Comments = Backbone.Collection.extend({
    model: app.models.Comment,
    url: function() {
        return '/api/v1/documents/' + this.doc.get('space') + '/' + this.doc.get('id') + '/comments';
    },

    initialize: function(args, options) {
        this.doc = options.doc
    },

});
