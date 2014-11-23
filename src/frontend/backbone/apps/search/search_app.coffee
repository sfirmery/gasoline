@Gasoline.module "SearchApp", (SearchApp, App, Backbone, Marionette, $, _) ->

    class SearchApp.Router extends Marionette.AppRouter
        appRoutes:
            "search?q=:query": "list"
        
    API =
        list: (query) ->
            new SearchApp.List.Controller
                query: query

    App.addInitializer ->
        new SearchApp.Router
            controller: API
