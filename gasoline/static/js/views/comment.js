var app = app || {};
app.views = app.views || {};

app.views.CommentView = Backbone.View.extend({
    tagName: 'li',
    className: 'commentView',
    template: _.template( $( '#commentTemplate' ).html() ),

    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html( this.template( this.model.toJSON() ) );

        console.log("render comment");
        console.log(this.model);

        return this;
    },

    deleteComment: function() {
        //Delete model
        this.model.destroy();

        //Delete view
        this.remove();
    },

});

app.views.CommentsView = Backbone.View.extend({
    el: '#comments',

   initialize: function(collection) {
        console.log("init comment view");
        var self = this;
        this.collection = collection;

        _.bindAll(this, 'render');
        this.collection.bind('change', this.render);
        this.collection.bind('reset', this.close);
        // this.model.bind('add:comments', this.renderComment); 
        // this.model.bind('add:tags', this.renderTag); 

        // this.collection.fetch({
        //     success: function() {
        //         self.render();
        //         console.log("self.collection");
        //         console.log(self.collection);
        //     }
        // });

        this.render();

    },

    // render a comment by creating a CommentView and appending the
    // element it renders to the view's element
    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function

        this.$el.children('#comments').remove()
        this.collection.each(function( item ) {
            var commentView = new app.views.CommentView({ model: item });
            this.$el.append( commentView.render().el );
        }, this );

        // this.$el.html( this.template( this.model.toJSON() ) );
        app.utils.formatTime();
    }

});
