var app = app || {};
app.models = app.models || {};

app.models.Tag = Backbone.Model.extend({
    urlRoot: function() {
        return '/api/v1/documents/' + this.get('space') + '/' + this.get('doc') + '/tags';
    },

});
