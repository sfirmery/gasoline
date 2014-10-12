@Gasoline.module "SpacesApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.Controller extends App.Controllers.Base

        initialize: (options) ->
            @layout = @getLayoutView()

            # render region when render layout
            @listenTo @layout, "show", =>
                @showHeader space
                @spaceView space

            if options.space != null
                space = App.request "get:spaces:entities", options.space
                
                App.execute "when:fetched", space, =>
                    @show @layout
            else
                space = options.model
                @show @layout

        spaceView: (space) ->
            spaceView = @getUserView space
            @show spaceView, region: @layout.spaceRegion
        
        showHeader: (space) ->
            App.execute "show:spaces:header", "edit", space, @layout.spaceHeaderRegion
        
        getUserView: (space) ->
            new Edit.Space
                model: space
        
        getLayoutView: ->
            new Edit.LayoutView
