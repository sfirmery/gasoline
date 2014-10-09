var app = app || {};
app.models = app.models || {};

app.models.Comment = Backbone.Model.extend({
    urlRoot: function() {
        return '/api/v1/documents/' + this.get('space') + '/' + this.get('doc') + '/comments';
    },

    defaults: {
        author: 'doe',
        content: 'No content',
        date: app.utils.getDateTime(),
    },

    attrsBlacklist: [
        'uri',
    ],

    save: function (attrs, options) { 
        attrs = attrs || this.toJSON();
        options = options || {};

        if (this.get('author').hasOwnProperty('name')) {
            attrs.author = this.get('author').name;
        }

        // If model defines attrsBlacklist, replace attrs with trimmed version
        if (this.attrsBlacklist) attrs = _.omit(attrs, this.attrsBlacklist);

        // Move attrs to options
        options.attrs = attrs;

        // Call super with attrs moved to options
        Backbone.Model.prototype.save.call(this, attrs, options);
    },

});
