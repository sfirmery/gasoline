var app = app || {};

$(function() {

  app.root = '/frontend/';

  app.currentUser = new app.models.User(app.currentUser)

  app.GasolineRouter = Backbone.Router.extend({
    routes: {
      '': 'dashboard',
      'dashboard': 'dashboard',
      'dashboard/:space': 'dashboard',
      'document/display/:space/:docId': 'displayDocument',
      'document/edit/:space/:docId': 'editDocument',
      'user/:user': 'viewUser',
    },

    dashboard: function(space){
      space = space || 'main';
      app.dashboardView = new app.views.DashboardView({'space': space});
    },

    displayDocument: function(space, docId){
      console.log('start view document');
      var doc = new app.models.Document({'space': space, 'id': docId});
      app.documentView = new app.views.DocumentView(doc, 'display');
    },

    editDocument: function(space, docId){
      console.log('start edit document');
      var doc = new app.models.Document({'space': space, 'id': docId});
      app.documentView = new app.views.DocumentView(doc, 'edit');
    },

    viewUser: function(user){
      console.log('start view user');
      app.userView = new app.views.UserView(new app.models.User({'id': user}));
    },

  });

  app.gasolineRouter = new app.GasolineRouter();
  // Backbone.history.start();
  Backbone.history.start({ 'pushState': true, 'root': app.root });

  $(document).on('click', 'a', function(event) {
    var href, passThrough, url;
    if (!$(event.currentTarget).attr('href')) { return false; };
    href = $(event.currentTarget).attr('href');
    console.log(href);
    passThrough = href.indexOf('sign_out') >= 0;
    if (!passThrough && !event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey) {
      event.preventDefault();
      url = href.replace('^\/', '').replace('#\!', '').replace(app.root, '');
      app.gasolineRouter.navigate(url, { trigger: true });
      return false;
    }
  });

  Backbone.Events.bind('comment:rendered', function(options){
    app.utils.formatTime(options);
  });

  Backbone.Events.bind('document:rendered', function(options){
    app.utils.formatTime(options);
  });
  Backbone.Events.bind('tag:rendered', function(options){
    console.log('tag:rendered', options);
  });

});
