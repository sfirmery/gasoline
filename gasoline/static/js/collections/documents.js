var app = app || {};

app.Documents = Backbone.Collection.extend({
    model: app.Document,
    url: '/api/v1/main/documents'
});
