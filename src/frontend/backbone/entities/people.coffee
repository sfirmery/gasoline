@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/people"

    class Entities.User extends Entities.Model
        urlRoot: baseUrl

    class Entities.UsersCollection extends Entities.Collection
        model: Entities.User
        url: baseUrl
        
        parse: (resp) ->
            resp

    API =
        getPeople: (params = {}) ->
            _.defaults params, {}
            
            people = new Entities.UsersCollection
            people.fetch
                reset: true
                data: params
            people

        getUser: (uid, params = {}) ->
            _.defaults params, {}

            user = new Entities.User id: uid
            user.fetch
                reset: true
                data: params
            user

    # request an user
    App.reqres.setHandler "people:entity", (uid) ->
        API.getUser $.trim(uid)

    # request list of people
    App.reqres.setHandler "people:entities", ->
        API.getPeople()

    # request a new user
    App.reqres.setHandler "new:user:entity", ->
        new Entities.User
