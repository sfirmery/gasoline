@Gasoline.module "SearchApp.LiveList", (LiveList, App, Backbone, Marionette, $, _) ->

    class LiveList.Controller extends App.Controllers.Application

        initialize: (options) ->
            console.log "initialize LiveList Controller"
            searchResults = App.request "new:search:entities"
            # console.log "search result entities", searchResults

            searchResultsView = @getSearchResultsView searchResults
            # console.log 'searchResultsView', searchResultsView
            # @setMainView searchResultsView

            @listenTo @, "update:live:search", (query) =>
                # console.log "LiveList.Controller event update:live:search"
                # results = App.request "search:query", query
                searchResults.query query, =>
                    @trigger "search:query:done", query
                    # console.log "results fetched", searchResults

            @show searchResultsView

        getSearchResultsView: (collection) ->
            new LiveList.SearchResults
                collection: collection
