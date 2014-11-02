@Gasoline.module "Views", (Views, App, Backbone, Marionette, $, _) ->

    _.extend Marionette.View::,

        addOpacityWrapper: (init = true, options = {}) ->
            _.defaults options,
                className: "opacity"

            @$el.toggleWrapper options, @cid, init

        setInstancePropertiesFor: (args...) ->
            for key, val of _.pick(@options, args...)
                @[key] = val

        templateHelpers: ->

            linkTo: (name, url, options = {}) ->
                _.defaults options,
                    external: false

                url = "#" + url unless options.external

                "<a href='#{url}'>#{@escape(name)}</a>"
