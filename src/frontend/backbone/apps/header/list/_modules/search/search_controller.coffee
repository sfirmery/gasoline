@Gasoline.module "HeaderApp.List.Modules.Search", (Search, App, Backbone, Marionette, $, _) ->

    class Search.Controller extends App.Controllers.Application

       initialize: (options) ->
            @searchResults = App.request "new:search:entities"

            # throttle search update
            @updateSearch = _.throttle @updateSearch, 1000
            @searchInProgress = 0

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @searchResultsRegion @searchResults

            @listenTo @layout, "update:search", (query) =>
                @updateSearch query

            @show @layout

        updateSearch: (query) ->
            # trigger search update
            @searchResults.query query, =>
                @searchInProgress--
                if @searchInProgress < 1
                    @layout.trigger "end:search"

            @searchInProgress++
            @layout.trigger "start:search"

        searchResultsRegion: (searchResults) ->
            searchResultsView = @getSearchResultsView searchResults
            @show searchResultsView, region: @layout.searchResultsRegion

        getSearchResultsView: (collection) ->
            new Search.SearchResults
                collection: collection

        getLayoutView: ->
            new Search.LayoutView

    App.reqres.setHandler "get:live:search", (region) ->
        new Search.Controller
            region: region
