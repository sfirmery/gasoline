var app = app || {};
app.models = app.models || {};

app.models.User = Backbone.Model.extend({
    urlRoot: '/api/v1/users',

    defaults: {
        name: 'Unknown'
    }
});
