@Gasoline.module "ACLApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: (options) ->
            {model} = options

            acl = App.request "acl:entities", model.space, model.id

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @panelRegion acl
                @aclRegion acl

            App.execute "when:fetched", acl, =>
                console.log "fetched", acl.models
                @show @layout

        panelRegion: (acl) ->
            panelView = @getPanelView acl
            @show panelView, region: @layout.panelRegion
        
        aclRegion: (acl) ->
            aclView = @getACLView acl
            @show aclView, region: @layout.aclRegion
        
        paginationRegion: (acl) ->
            paginationView = @getPaginationView acl
            @show paginationView, region: @layout.paginationRegion
        
        getPanelView: (acl) ->
            new List.Panel
                collection: acl
        
        getACLView: (acl) ->
            new List.ACL
                collection: acl
        
        getLayoutView: ->
            new List.LayoutView
