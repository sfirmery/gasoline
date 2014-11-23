@Gasoline.module "SearchApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: (options) ->
            searchResults = App.request "search:query", options.query

            App.execute "when:fetched", searchResults, =>
                @layout = @getLayoutView()

                console.log "searchResults", searchResults.q

                @listenTo @layout, "show", =>
                    @panelRegion searchResults
                    @getSidebarRegion searchResults
                    @searchResultsRegion searchResults
                    @paginationRegion searchResults

                @show @layout

        panelRegion: (searchResults) ->
            panelView = @getPanelView searchResults

            @listenTo panelView, "search:button:clicked", ->
                App.vent.trigger "search:clicked", searchResults

            @show panelView, region: @layout.panelRegion

        getSidebarRegion: (searchResults) ->
            sidebarView = @getSidebarView searchResults

            @show sidebarView, region: @layout.sidebarRegion
        
        searchResultsRegion: (searchResults) ->
            searchResultsView = @getSearchResultsView searchResults

            @show searchResultsView, region: @layout.searchResultsRegion

        paginationRegion: (searchResults) ->
            paginationView = @getPaginationView searchResults
            @show paginationView, region: @layout.paginationRegion

        getPanelView: (searchResults) ->
            new List.Panel
                collection: searchResults

        getSidebarView: (searchResults) ->
            new List.Sidebar
                collection: searchResults

        getPaginationView: (searchResults) ->
            new List.Pagination
                collection: searchResults

        getSearchResultsView: (searchResults) ->
            new List.SearchResults
                collection: searchResults

        getLayoutView: ->
            new List.LayoutView
