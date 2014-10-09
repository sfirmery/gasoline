var app = app || {};
app.collections = app.collections || {};

app.collections.Tags = Backbone.Collection.extend({
    model: app.models.Tag,
    url: function() {
        return '/api/v1/documents/' + this.doc.get('space') + '/' + this.doc.get('id') + '/tags';
    },

    initialize: function(args, options) {
        this.doc = options.doc
    },

    add: function(models, options) {
        // set model id for each models
        if (_.isArray(models)) {
            console.log("is an array");
            models.forEach(function(model) {
                model.id = model.tag;
            });
        }
        else {
            models.id = models.tag;
        }

        Backbone.Collection.prototype.add.call(this, models, options);
    },

    create: function(attributes, options) {
        Backbone.Collection.prototype.create.call(this, attributes, _.extend(options, {success: function(model) {
            model.id = model.get('tag');
            model.set('id', model.get('tag'));
        }}));
    }
});
