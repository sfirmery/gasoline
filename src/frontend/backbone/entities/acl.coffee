@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1"

    class Entities.ACE extends Entities.Model
        urlRoot: ->
            "#{baseUrl}/documents/#{@space}/#{@docId}/acl/"

        initialize: (options) ->
            {@space, @docId} = options

    class Entities.ACLCollection extends Entities.Collection
        model: Entities.ACE

        url: ->
            "#{baseUrl}/documents/#{@space}/#{@docId}/acl" if @space and @docId
            "#{baseUrl}/documents/#{@space}/#{@docId}/acl" if not @space or not @docId

        initialize: (options) ->
            {@space, @docId} = options

        parse: (resp) ->
            resp

    API =
        getACL: (space, docId, params = {}) ->
            _.defaults params, {}

            acl = new Entities.ACLCollection
                space: space
                docId: docId
            acl.fetch
                data: params
            acl

    # request an ACE
    App.reqres.setHandler "acl:entity", (space = {}, docId = {}) ->
        API.getACE $.trim(space), $.trim(docId)

    # request ACL
    App.reqres.setHandler "acl:entities", (space = {}, docId = {}) ->
        console.log "query acl:entities"
        API.getACL $.trim(space), $.trim(docId)

    # request a new space
    App.reqres.setHandler "new:acl:entity", ->
        new Entities.ACE
