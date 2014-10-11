@Gasoline.module "TMPLApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Base

        initialize: (id) ->
            tmpl = App.request "tmpl:entities:one", id

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @tmplView tmpl

            App.execute "when:fetched", tmpl, =>
                @show @layout

        tmplView: (tmpl) ->
            tmplView = @getUserView tmpl
            @show tmplView, region: @layout.tmplRegion
        
        getUserView: (tmpl) ->
            new Show.User
                model: tmpl
        
        getLayoutView: ->
            new Show.LayoutView
