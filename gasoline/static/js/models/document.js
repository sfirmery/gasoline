var app = app || {};
app.models = app.models || {};

app.models.Document = Backbone.Model.extend({
    // urlRoot: '/api/v1/documents/',
    urlRoot: function() {
        return '/api/v1/documents/' + this.get('space');
    },

    defaults: {
        title: 'No title',
        author: 'Unknown',
        content: 'No content',
        space: 'main',
    },

    attrsBlacklist: [
        'tags',
        'comments',
        'attachments',
        'acl',
        'uri',
    ],

    save: function (attrs, options) { 
        attrs = attrs || this.toJSON();
        options = options || {};

        attrs.author = this.get('author').name
        attrs.last_author = this.get('last_author').name

        // If model defines attrsBlacklist, replace attrs with trimmed version
        if (this.attrsBlacklist) attrs = _.omit(attrs, this.attrsBlacklist);

        // Move attrs to options
        options.attrs = attrs;

        // Call super with attrs moved to options
        Backbone.Model.prototype.save.call(this, attrs, options);
    },
});
