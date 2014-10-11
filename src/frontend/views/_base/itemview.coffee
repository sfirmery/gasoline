@Gasoline.module "Views", (Views, App, Backbone, Marionette, $, _) ->

	class Views.ItemView extends Marionette.ItemView

        constructor: ->
            super

            @listenTo this, 'show', ->
                @formatDate()

        # render date with timeago
        formatDate: ->
            $(@el).find("time.timeago").timeago()
            $(@el).find("time.timeago").tooltip
                container: "body"
                delay:
                    show: 400