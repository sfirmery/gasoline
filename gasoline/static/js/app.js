var app = app || {};

$(function() {

  app.GasolineRouter = Backbone.Router.extend({
    routes: {
      "": "dashboard",
      "dashboard": "dashboard",
      "document/:space/view/:docId": "viewDocument",
      "user/:user": "viewUser",
    },

    dashboard: function(){
      app.dashboardView = new app.views.Dashboardiew();
    },

    viewDocument: function(space, docId){
      console.log("start view document");
      app.docView = new app.views.DocumentView(new app.models.Document({'space': space, 'id': docId}));
    },

    viewUser: function(user){
      console.log("start view user");
      console.log(user);
      console.log(new app.User({'id': user}).fetch());
      app.userView = new app.views.UserView(new app.User({'id': user}));
    },

  });

  app.gasolineRouter = new app.GasolineRouter();
  Backbone.history.start();

});
