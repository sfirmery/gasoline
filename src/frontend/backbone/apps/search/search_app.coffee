@Gasoline.module "SearchApp", (SearchApp, App, Backbone, Marionette, $, _) ->

    class SearchApp.Router extends Marionette.AppRouter
        appRoutes:
            "search/:query": "list"
        
    API =
        list: (query) ->
            new SearchApp.List.Controller
                query: query

        liveList: (region) ->
            new SearchApp.LiveList.Controller
                region: region

    App.reqres.setHandler "get:live:search", (region) ->
        API.liveList region

    App.vent.on "live:search:typed", (query) ->
        API.liveList query

    App.addInitializer ->
        new SearchApp.Router
            controller: API
