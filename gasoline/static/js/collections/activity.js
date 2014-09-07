var app = app || {};
app.collections = app.collections || {};

app.collections.Activity = Backbone.Collection.extend({
    model: app.models.Activity,
    url: '/api/v1/activity'
});
