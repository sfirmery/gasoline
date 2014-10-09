var app = app || {};
app.models = app.models || {};

app.models.Activity = Backbone.Model.extend({
    urlRoot: '/api/v1/activity',
});
