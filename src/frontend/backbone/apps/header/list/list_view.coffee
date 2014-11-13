@Gasoline.module "HeaderApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.LayoutView extends App.Views.LayoutView
        template: "header/list/list_layout"
        tagName: "nav"
        className: "navbar navbar-default navbar-fixed-top"
        attributes:
            role: "navigation"

        regions:
            navLeftRegion: '#nav-left-region'
            navRightRegion: '#nav-right-region'

    class List.NavLeft extends App.Views.CollectionView
        template: "header/list/_nav_left"
        tagName: "ul"
        className: "nav navbar-nav navbar-left"

        getChildView: (item) ->
            if item.get('childView') then item.get('childView') else throw new Error "childView not found"

        serializeData: ->
            currentUser: App.currentUser

    class List.NavRight extends App.Views.CollectionView
        template: "header/list/_nav_right"
        tagName: "ul"
        className: "nav navbar-nav navbar-right"

        getChildView: (item) ->
            if item.get('childView') then item.get('childView') else throw new Error "childView not found"

        serializeData: ->
            currentUser: App.currentUser

    class List.NavCreate extends App.Views.ItemView
        template: "header/list/_nav_create"
        tagName: "li"

    class List.NavTests extends App.Views.ItemView
        template: "header/list/_nav_tests"
        tagName: "li"
        className: "dropdown"

    class List.NavSpacesList extends App.Views.ItemView
        template: "header/list/_nav_spaces_list"
        tagName: "li"

    class List.NavSpaces extends App.Views.CompositeView
        template: "header/list/_nav_spaces"
        tagName: "li"
        className: "dropdown"
        childView: List.NavSpacesList
        childViewContainer: "ul"

        initialize: (options) ->
            @collection = App.request "spaces:entities"

            @$el.on "show.bs.dropdown", (options) =>
                @collection.fetch()

        onDestroy: ->
            @$el.off "show.bs.dropdown"

    class List.NavSearch extends App.Views.LayoutView
        template: "header/list/_nav_search"
        tagName: "li"
        # className: "dropdown"

        regions:
            searchResultsRegion: '#header-searchbox-results-region'

        ui:
            input: '#header-searchbox input'
            searchbox: '#header-searchbox'
            iconSearch: 'i.fa-search'
            iconSpinner: 'i.fa-spinner'
            searchResults: 'ul.search-results'

        events:
            "focus @ui.input" : ->
                @ui.searchbox.addClass "focus"
                @ui.searchResults.show()
            "blur @ui.input" : ->
                @ui.searchbox.removeClass "focus"
                @ui.searchResults.hide()
            "submit" : (e) ->
                @submit e
            "input @ui.input" : ->
                # trigger throttled search update if input not too small
                @updateSearch() if @ui.input.val().length > 2

        initialize: (options) ->
            # throttle search update
            @updateSearch = _.throttle @updateSearch, 1000
            @searchInProgress = 0

            @listenTo @, "show", =>
                @liveSearchView = @getLiveSearchView @searchResultsRegion
                @bindUIElements()

                @listenTo @liveSearchView, "search:query:done", (query) => 
                    @searchInProgress--
                    if @searchInProgress < 1
                        @hideSpinner()
                    # console.log "search end, current search in progress", query, @searchInProgress

        getLiveSearchView: (region) ->
            App.request "get:live:search", region            

        updateSearch: ->
            # trigger search update
            @liveSearchView.trigger "update:live:search", @ui.input.val()
            @searchInProgress++
            @showSpinner()
            # console.log "start search, current search in progress", @ui.input.val(), @searchInProgress
            # @ui.searchResults.show()

        showSpinner: ->
            @ui.iconSearch.addClass "fade"
            @ui.iconSpinner.removeClass "fade"

        hideSpinner: ->
            @ui.iconSpinner.addClass "fade"
            @ui.iconSearch.removeClass "fade"

        submit: (e) ->
            e.preventDefault()

    class List.NavUserMenu extends App.Views.ItemView
        template: "header/list/_nav_user_menu"
        tagName: "li"
        className: "dropdown"

        serializeData: ->
            currentUser: App.currentUser
