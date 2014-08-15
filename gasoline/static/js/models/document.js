var app = app || {};

app.Document = Backbone.Model.extend({
    urlRoot: '/api/v1/main/documents',

    defaults: {
        title: 'No title',
        author: 'Unknown',
        content: 'No content',
        space: 'main',
    }

});
