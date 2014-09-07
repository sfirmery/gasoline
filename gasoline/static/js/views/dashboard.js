var app = app || {};
app.views = app.views || {};

app.views.Dashboardiew = Backbone.View.extend({
    el: '#documents',
    template: _.template( $( '#dashboardTemplate' ).html() ),

   initialize: function() {
        console.log("init dashboard view");
        this.$el.html( this.template );
        this.docListView = new app.views.DocumentsListView();
        this.activsityStreamView = new app.views.ActivityStreamView();
    },
});
