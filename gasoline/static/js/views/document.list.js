var app = app || {};
app.views = app.views || {};

app.views.DocumentListView = Backbone.View.extend({
    tagName: 'li',
    className: 'documentListView',
    template: _.template( $( '#documentListItemTemplate' ).html() ),

    events: {
        'click .delete': 'deleteDocument'
    },

    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html( this.template( this.model.toJSON() ) );

        return this;
    },

    deleteDocument: function() {
        //Delete model
        this.model.destroy();

        //Delete view
        this.remove();
    },

});

app.views.DocumentsListView = Backbone.View.extend({
    el: '#documents-list',
    template: _.template( $( '#documentListTemplate' ).html() ),

    events:{
        'click #add':'addDocument'
    },

   initialize: function() {
        console.log("init documents list view");
        this.collection = new app.collections.Documents();
        this.collection.fetch({reset: true});
        // empty $el
        this.$el.html( this.template );
        this.render();

        this.listenTo( this.collection, 'add', this.renderDocument );
        this.listenTo( this.collection, 'reset', this.render );
    },

    // render view by rendering each document in its collection
    render: function() {
        // remove childrens
        this.$el.children('.documentListView').remove()
        this.collection.each(function( item ) {
            this.renderDocument( item );
        }, this );
        app.utils.formatTime();
    },

    // render a document by creating a DocumentListView and appending the
    // element it renders to the view's element
    renderDocument: function( item ) {
        var documentView = new app.views.DocumentListView({
            model: item
        });
        this.$el.append( documentView.render().el );
    },

    addDocument: function( e ) {
        e.preventDefault();

        var formData = {};

        $( '#addDocument div' ).children( 'input' ).each( function( i, el ) {
            if( $( el ).val() != '' )
            {
                formData[ el.id ] = $( el ).val();
            }
        });

        this.collection.create( formData );

    },

});
