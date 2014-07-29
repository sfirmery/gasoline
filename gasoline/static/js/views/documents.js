var app = app || {};

app.DocumentsView = Backbone.View.extend({
    el: '#documents',

    events:{
        'click #add':'addDocument'
    },

   initialize: function() {
        this.collection = new app.Documents();
        this.collection.fetch({reset: true});
        this.render();

        this.listenTo( this.collection, 'add', this.renderDocument );
        this.listenTo( this.collection, 'reset', this.render ); // NEW
    },

    // render library by rendering each document in its collection
    render: function() {
        // remove childrens
        this.$el.children('.documentContainer').remove()
        this.collection.each(function( item ) {
            this.renderDocument( item );
        }, this );
    },

    // render a document by creating a DocumentView and appending the
    // element it renders to the library's element
    renderDocument: function( item ) {
        var documentView = new app.DocumentView({
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

        console.log('addDocument started');

        // this.collection.add( new app.Document( formData ) );
        this.collection.create( formData );

    },

});
