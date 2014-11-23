@Gasoline.module "HeaderApp.List.Modules.Search", (Search, App, Backbone, Marionette, $, _) ->

    class Search.LayoutView extends App.Views.LayoutView
        template: "header/list/_modules/search/search_layout"
        tagName: "li"

        regions:
            searchResultsRegion: '#header-searchbox-results-region'

        ui:
            input: '#header-searchbox input'
            searchbox: '#header-searchbox'
            iconSearch: 'i.fa-search'
            iconSpinner: 'i.fa-spinner'
            searchResult: 'ul.search-results li a'

        events:
            "focus @ui.input" : 'focus'
            "click @ui.searchResult": 'unFocus'
            "submit" : (e) -> @submit e
            "input @ui.input" : ->
                # trigger search update if input not too small
                @trigger "update:search", @ui.input.val() if @ui.input.val().length > 2

        initialize: (options) ->
            @listenTo @, "end:search", => @hideSpinner()
            @listenTo @, "start:search", => @showSpinner()

        onShow: ->
            @bindUIElements()

        focus: ->
            if not @ui.searchbox.hasClass 'focus'
                @ui.searchbox.addClass "focus"
                # register click event anywhere
                $('body').on 'click', (e, target) =>
                    # if click outside searchbox or results box
                    if not $(e.target).closest(@ui.searchbox).length
                        @unFocus()
            # select current search query
            select = _.bind @ui.input.select, @ui.input
            _.delay select, 200

        unFocus: ->
            # unregister event
            $('body').off 'click'
            @ui.searchbox.removeClass "focus"

        showSpinner: ->
            @ui.iconSearch.addClass "fade"
            @ui.iconSpinner.removeClass "fade"

        hideSpinner: ->
            @ui.iconSpinner.addClass "fade"
            @ui.iconSearch.removeClass "fade"

        submit: (e) ->
            e.preventDefault()

    class Search.SearchResult extends App.Views.ItemView
        template: "header/list/_modules/search/_search_result"
        tagName: "li"

        modelEvents:
            "updated" : "render"

    class Search.SearchResults extends App.Views.CompositeView
        template: "header/list/_modules/search/_search_results"
        tagName: "ul"
        className: "dropdown-menu search-results"

        childView: Search.SearchResult
