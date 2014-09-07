var app = app || {};
app.collections = app.collections || {};

app.collections.Documents = Backbone.Collection.extend({
    model: app.models.Document,
    url: '/api/v1/main/documents'
});
