var app = app || {};
app.views = app.views || {};

app.views.TagView = Backbone.View.extend({
    tagName: 'span',
    className: 'label label-info',
    template: _.template( "<%= tag %> <i id=\"tag-delete\" class=\"fa fa-times\"></i>" ),
    mode: 'display',

    events: {
        'click #tag-delete': 'deleteTag',
    },

   initialize: function(options) {
        console.log("initialize tag", options);
        this.model = options.model;
        this.doc = options.doc;

        // _.bindAll(this, 'render');
        // this.model.bind('sync', this.render);
    },

    render: function() {
        console.log("enter render tag");

        this.el.id = 'tag-' + this.model.get('tag');
        switch ( this.mode ) {
            default:
                console.log('init display tag view');
                this.renderDisplay();
        };
        return this;
    },

    renderDisplay: function() {
        this.$el.html( this.template( this.model.toJSON(), mode=this.mode ) );
    },

    displayTag: function() {
        this.mode = 'display';
        this.render();
    },

    deleteTag: function() {
        console.log("start delete tag", this.model);
        //Delete model
        this.model.destroy();

        //Delete view
        this.remove();
    },

});

app.views.TagsView = Backbone.View.extend({
    el: '#document-tag-list',

    events: {
        'submit #document-tag-add-form': 'addTag',
    },

   initialize: function(doc, collection) {
        console.log("init tag view");
        var self = this;
        this.collection = collection;
        this.doc = doc;

        this.listenTo( this.collection, 'add', this.renderSingleTag );
        this.listenTo( this.collection, 'reset', this.renderTags );

        console.log(this.collection);
    },

    renderTag: function(item) {
        console.log("init render tag", item);
        var tagView = new app.views.TagView({ model: item, doc: this.doc });
        this.$el.children('.tag-list-items').append( tagView.render().el );
        return tagView.el;
    },

    renderSingleTag: function(item) {
        var el = this.renderTag(item);

        Backbone.Events.trigger('tag:rendered', el);
    },

    renderTags: function() {
        this.$el.children('.tag-list-items').children('span').remove()
        this.collection.each(function( item ) {
            this.renderTag(item);
        }, this );

        Backbone.Events.trigger('tag:rendered', this.el);
    },

    addTag: function( e ) {
        console.log("enter add tag");
        var self = this;

        e.preventDefault();

        var formData = {};
        // set doc and space values
        formData['doc'] = this.doc.get('id');
        formData['space'] = this.doc.get('space');

        $('#document-tag-add-form').children('input').each( function(i, el) {
            if( $(el).val() != '' )
            {
                formData[el.name] = $(el).val();
            }
            $(el).val('');
        });

        console.log('add tag formdata', formData);
        this.collection.create(formData, { wait: true });
    },

});
