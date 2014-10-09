var app = app || {};
app.views = app.views || {};

app.views.DashboardView = Backbone.View.extend({
    el: '#content',
    template: _.template( $( '#dashboardTemplate' ).html() ),

   initialize: function(options) {
        this.space = options.space;
        console.log("init dashboard view");
        this.$el.html( this.template );
        this.documentsListView = new app.views.DocumentsListView(new app.collections.Documents(null, {space: this.space}));
        this.activsityStreamView = new app.views.ActivityStreamView({space: this.space});
    },
});
