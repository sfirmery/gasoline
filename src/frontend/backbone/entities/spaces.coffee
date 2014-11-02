@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/spaces"

    class Entities.Space extends Entities.Model
        urlRoot: baseUrl

    class Entities.SpacesCollection extends Entities.Collection
        model: Entities.Space
        url: baseUrl

        parse: (resp) ->
            resp

    API =
        getSpaces: (params = {}) ->
            _.defaults params, {}
            
            spaces = new Entities.SpacesCollection
            spaces.fetch
                reset: true
                data: params
            spaces

        getSpace: (id, params = {}) ->
            _.defaults params, {}

            space = new Entities.Space id: id
            space.fetch
                reset: true
                data: params
            space

    # request a spaces
    App.reqres.setHandler "spaces:entity", (space) ->
        API.getSpace $.trim(space)

    # request list of spaces
    App.reqres.setHandler "spaces:entities", ->
        API.getSpaces()

    # request a new space
    App.reqres.setHandler "new:space:entity", ->
        new Entities.Space
