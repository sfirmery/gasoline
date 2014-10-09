var app = app || {};
app.views = app.views || {};

app.views.DocumentListView = Backbone.View.extend({
    tagName: 'li',
    className: 'documentListView',
    template: _.template( $( '#documentListItemTemplate' ).html() ),

    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html( this.template( this.model.toJSON() ) );

        return this;
    },

});

app.views.DocumentsListView = Backbone.View.extend({
    el: '#documents-list',
    template: _.template( $( '#documentListTemplate' ).html() ),

   initialize: function(collection) {
        console.log('init documents list view');
        console.log(collection);
        this.collection = collection;

        this.listenTo( this.collection, 'add', this.renderDocument );
        this.listenTo( this.collection, 'reset', this.render );

        this.collection.fetch({reset: true, data: {details: false}});
        // empty $el
        this.$el.html( this.template );
    },

    // render view by rendering each document in its collection
    render: function() {
        // remove childrens
        this.$el.children('.documentListView').remove()
        console.log('redner collection');
        console.log(this.collection);
        this.collection.each(function( item ) {
            console.log(item);
            this.renderDocument( item );
        }, this );
        app.utils.formatTime();
    },

    // render a document by creating a DocumentListView and appending the
    // element it renders to the view's element
    renderDocument: function( item ) {
        console.log('render doc');
        console.log(item);
        var documentView = new app.views.DocumentListView({
            model: item
        });
        this.$el.append( documentView.render().el );
    },

});
