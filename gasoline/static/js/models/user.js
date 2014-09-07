var app = app || {};
app.models = app.models || {};

app.User = Backbone.Model.extend({
    urlRoot: '/api/v1/users',

    defaults: {
        name: 'Unknown'
    }
});
