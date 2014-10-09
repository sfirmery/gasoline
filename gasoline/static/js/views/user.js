var app = app || {};
app.views = app.views || {};

app.views.UserView = Backbone.View.extend({
    tagName: 'div',
    className: 'userView',
    template: _.template( $( '#userTemplate' ).html() ),

    el: '#content',

   initialize: function(model) {
        console.log("init user view");
        var self = this;
        this.model = model;

        _.bindAll(this, 'render');
        this.model.bind('change', this.render);
        this.model.bind('reset', this.close);
        // this.model.bind('add:comments', this.renderComment); 
        // this.model.bind('add:tags', this.renderTag); 

        this.model.fetch({
            success: function() {
                // console.log("start render user");
                // self.render();
                console.log("self.user");
                console.log(self.model);
            }
        });
    },

    // render a user by creating a UserView and appending the
    // element it renders to the view's element
    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html( this.template( this.model.toJSON() ) );

        console.log("render done");
    }

});
