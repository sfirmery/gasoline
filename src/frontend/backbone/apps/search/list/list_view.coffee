@Gasoline.module "SearchApp.List", (List, App, Backbone, Marionette, $, _) ->
    
    class List.LayoutView extends App.Views.LayoutView
        template: "search/list/list_layout"
        regions:
            panelRegion:            "#panel-region"
            sidebarRegion:          "#sidebar-region"
            searchResultsRegion:    "#search-results-region"
            paginationRegion:       "#pagination-region"

    class List.SearchResult extends App.Views.ItemView
        template: "search/list/_search_result"
        tagName: "tr"

        modelEvents:
            "updated" : "render"

    class List.SearchResults extends App.Views.CompositeView
        template: "search/list/_search_results"
        childView: List.SearchResult
        childViewContainer: "tbody"
    
    class List.Panel extends App.Views.ItemView
        template: "search/list/_panel"

        triggers:
            "click #search" : "search:button:clicked"

        collectionEvents:
            "add": "render"
            "remove": "render"

        templateHelpers: ->
            query: @collection.q

    class List.Sidebar extends App.Views.ItemView
        template: "search/list/_sidebar"

        collectionEvents:
            "add": "render"
            "remove": "render"

    class List.Pagination extends App.Views.ItemView
        template: "search/list/_pagination"
        className: "pull-right"

        collectionEvents:
            "add": "render"
            "remove": "render"
