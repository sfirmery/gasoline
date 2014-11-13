@Gasoline.module "SearchApp.LiveList", (LiveList, App, Backbone, Marionette, $, _) ->

    class LiveList.SearchResult extends App.Views.ItemView
        template: "search/live_list/_search_result"
        tagName: "li"

        modelEvents:
            "updated" : "render"

        # ui:
        #     edit: '#edit'
        #     delete: '#delete'

        # triggers:
        #     "click @ui.edit": "edit:space:clicked"
        #     "click @ui.delete" : "delete:space:clicked"

    class LiveList.SearchResults extends App.Views.CompositeView
        template: "search/live_list/_search_results"
        tagName: "ul"
        className: "dropdown-menu search-results"

        childView: LiveList.SearchResult
