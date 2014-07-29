var app = app || {};

app.User = Backbone.Model.extend({
    urlRoot: '/api/v1/users',

    defaults: {
        name: 'Unknown'
    }
});
