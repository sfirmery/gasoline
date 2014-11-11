@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1"

    class Entities.ACE extends Entities.Model
        urlRoot: ->
            {@space, @docId} = @collection if @collection
            return "#{baseUrl}/documents/#{@space}/#{@docId}/acl" if @space and @docId
            return "#{baseUrl}/spaces/#{@space}/acl" if @space and not @docId

        defaults:
            predicate: ''
            permissions:
                read: ''
                write: ''

        initialize: (attributes, options) ->
            @permissionsKeys = @getTruthKeys()

        # get ordered permission name
        getTruthKeys: ->
            _.keys(@attributes.permissions).sort (a, b) ->
                return -1 if a == 'read'
                return 1 if b == 'read'
                return -1 if a == 'write'
                return 1 if b == 'write'
                return 0

    class Entities.ACLCollection extends Entities.Collection
        model: Entities.ACE

        url: ->
            return "#{baseUrl}/documents/#{@space}/#{@docId}/acl" if @space and @docId
            return "#{baseUrl}/spaces/#{@space}/acl" if @space and not @docId

        # custom sort
        comparator: (a, b) ->
            # if a predicate is ANY, set it upper index
            return -1 if a.get('predicate') == 'ANY'
            # if b predicate is ANY, set it upper index
            return 1 if b.get('predicate') == 'ANY'

            a_g = a.get('predicate').search('g:')
            b_g = b.get('predicate').search('g:')
            # if a predicate is group and b not, set it upper index
            return -1 if a_g == 0 and b_g != 0
            # if b predicate is group and a not, set it upper index
            return 1 if a_g != 0 and b_g == 0

            a_u = a.get('predicate').search('u:')
            b_u = b.get('predicate').search('u:')
            # if a predicate is user and b not, set it upper index
            return -1 if a_u == 0 and b_u != 0
            # if b predicate is user and a not, set it upper index
            return 1 if a_u != 0 and b_u == 0
            return 0

        initialize: (models, options) ->
            {@space, @docId} = options

        parse: (resp) ->
            resp

    API =
        getACL: (space, docId, params = {}) ->
            _.defaults params, {}

            acl = new Entities.ACLCollection null,
                space: space
                docId: docId
            acl.fetch
                data: params
            acl

    # request an ACE
    App.reqres.setHandler "new:acl:entity", (predicate, space, docId) ->
        new Entities.ACE 'predicate': predicate,
            space: space
            docId: docId

    # request ACL
    App.reqres.setHandler "acl:entities", (space = {}, docId = {}) ->
        API.getACL space, docId

