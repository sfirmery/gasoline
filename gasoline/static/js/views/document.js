var app = app || {};

app.DocumentView = Backbone.View.extend({
    tagName: 'div',
    className: 'documentContainer',
    template: _.template( $( '#documentTemplate' ).html() ),

    events: {
        'click .delete': 'deleteDocument'
    },

    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html( this.template( this.model.toJSON() ) );

        return this;
    },

    deleteDocument: function() {

        console.log(this)
        //Delete model
        this.model.destroy();

        //Delete view
        this.remove();
    },

});
