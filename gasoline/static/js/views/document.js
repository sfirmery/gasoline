var app = app || {};
app.views = app.views || {};

app.views.DocumentView = Backbone.View.extend({
    tagName: 'div',
    className: 'documentView',
    template: _.template( $( '#documentTemplate' ).html() ),

    el: '#documents',

   initialize: function(model) {
        console.log("init document view");
        var self = this;
        this.model = model

        _.bindAll(this, 'render');
        this.model.bind('change', this.render);
        this.model.bind('reset', this.close);
        // this.model.bind('add:comments', this.renderComment); 
        // this.model.bind('add:tags', this.renderTag); 

        this.model.fetch({
            success: function() {
                // console.log("start render document");
                // self.render();
                console.log("self.document");
                console.log(self.model);
            }
        });
    },

    // render a document by creating a DocumentView and appending the
    // element it renders to the view's element
    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html( this.template( this.model.toJSON() ) );

        console.log("render comment view");
        console.log(new app.collections.Comments(this.model.get('comments')));
        app.commentsView = new app.views.CommentsView(new app.collections.Comments(this.model.get('comments')));

        app.utils.formatTime();
    }

});
