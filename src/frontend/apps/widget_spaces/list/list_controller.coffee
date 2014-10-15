@Gasoline.module "WidgetSpacesApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Base

        initialize: ->
            spaces = App.request "spaces:entities"

            App.execute "when:fetched", spaces, =>
                spaces.reset spaces.sortBy "name"
                @spacesView spaces

        spacesView: (spaces) ->
            spacesView = @getSpacesView spaces
            @show spacesView
        
        getSpacesView: (spaces) ->
            new List.Spaces
                collection: spaces
