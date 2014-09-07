var app = app || {};
app.models = app.models || {};

app.models.Comment = Backbone.Model.extend({
    urlRoot: '/api/v1/main/documents/comments',
});
