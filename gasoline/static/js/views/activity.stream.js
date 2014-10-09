var app = app || {};
app.views = app.views || {};

app.views.ActivityStreamItemView = Backbone.View.extend({
    tagName: 'div',
    className: 'activityStreamView',
    template: _.template( $( '#activityStreamItemTemplate' ).html() ),

    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html( this.template( this.model.toJSON() ) );
        return this;
    },

    deleteActivity: function() {
        //Delete model
        this.model.destroy();

        //Delete view
        this.remove();
    },

});

app.views.ActivityStreamView = Backbone.View.extend({
    el: '#activity-stream',
    template: _.template( $( '#activityStreamTemplate' ).html() ),

   initialize: function(options) {
        this.space = options.space;
        console.log("init activity stream view");

        this.collection = new app.collections.Activity({space: this.space});

        this.listenTo( this.collection, 'add', this.renderActivityItem );
        this.listenTo( this.collection, 'reset', this.render );

        // empty $el
        this.$el.html( this.template );

        this.collection.fetch({reset: true});
    },

    // render view by rendering each activity in its collection
    render: function() {
        // remove childrens
        this.$el.children('.activityStreamView').remove()
        this.collection.each(function( item ) {
            this.renderActivityItem( item );
        }, this );
        
        app.utils.formatTime();
    },

    // render a activity by creating a ActivityStreamItemView and appending the
    // element it renders to the view's element
    renderActivityItem: function( item ) {
        var activityItemView = new app.views.ActivityStreamItemView({
            model: item
        });
        this.$el.append( activityItemView.render().el );
    },
});
