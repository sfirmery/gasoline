var app = app || {};
app.collections = app.collections || {};

app.collections.Comments = Backbone.Collection.extend({
    model: app.models.Comment,
    url: '/api/v1/main/documents/53ef733171ba59670f83b6f2/comments'
});
