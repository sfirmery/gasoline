@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/search"

    class Entities.SearchResult extends Entities.Model
        urlRoot: baseUrl

    class Entities.SearchResultsCollection extends Entities.Collection
        model: Entities.SearchResult
        url: baseUrl

        query: (query, callback) ->
            @fetch
                reset: true
                success: callback
                error: callback
                data:
                    q: query

        parse: (resp) ->
            resp.results

    API =
        getResults: (params = {}) ->
            _.defaults params, {}
            
            search = new Entities.SearchResultsCollection
            search.fetch
                reset: true
                data: params
            search

        getEmptySearchResultsCollection: ->
            new Entities.SearchResultsCollection

    # request a search
    App.reqres.setHandler "search:query", (query) ->
        API.getResults
            q: $.trim(query)

    App.reqres.setHandler "new:search:entities", (spaces) ->
        API.getEmptySearchResultsCollection()
