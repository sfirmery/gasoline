@Gasoline.module "ACLApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: (options) ->
            {@space} = options.model
            @docId = options.model.id

            acl = App.request "acl:entities", @space, @docId

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @panelRegion acl
                @aclRegion acl

            @listenTo @layout, "new:ace:clicked", (type) =>
                $('#acl-dropdown').dropdown('toggle')
                @addAce acl, type

            App.execute "when:fetched", acl, =>
                @show @layout

        addAce: (acl, type, options) ->
            data = Backbone.Syphon.serialize @layout
            console.log "add:ace:clicked with", type, data, 'predicate' in _.keys(data)
            if type == 'ANY'
                throw new Error "predicate already exists" if acl.get type
                ace = App.request "new:acl:entity", type, @space, @docId
                console.log 'is ANY', ace
            else if 'predicate' in _.keys(data)
                data.predicate = $.trim(data.predicate)
                if type == 'user'
                    throw new Error "predicate already exists" if acl.get "u:#{data.predicate}"
                    ace = App.request "new:acl:entity", "u:#{data.predicate}", @space, @docId
                    console.log 'is user', ace
                else if type == 'group'
                    throw new Error "predicate already exists" if acl.get "g:#{data.predicate}"
                    ace = App.request "new:acl:entity", "g:#{data.predicate}", @space, @docId
                    console.log 'is group', ace
                else
                    throw new Error "unknown predicate type #{data.predicate}"
            else
                throw new Error "need a predicate"

            acl.add ace
            ace.save()
            console.log 'new acl', acl, ace

        panelRegion: (acl) ->
            panelView = @getPanelView acl
            @show panelView, region: @layout.panelRegion

        aclRegion: (acl) ->
            aclView = @getACLView acl
            @show aclView, region: @layout.aclRegion

            @listenTo aclView, "all", (options) ->
                console.log "event aclView", options
            @listenTo aclView, "childview:delete:ace:clicked", (iv, args) ->
                console.log "childview:delete:ace:clicked"
                args.model.destroy
                    wait: true

        getPanelView: (acl) ->
            new List.Panel
                collection: acl

        getACLView: (acl) ->
            new List.ACL
                collection: acl

        getLayoutView: ->
            new List.LayoutView
