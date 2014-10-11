@Gasoline = do (Backbone, Marionette) ->
    
    App = new Marionette.Application        
    
    App.addRegions
        headerRegion: "#header-region"
        mainRegion: "#main-region"
        footerRegion: "#footer-region"
    
    App.rootRoute = "documents/main"

    App.reqres.setHandler "default:region", ->
        App.mainRegion

    App.addInitializer ->
        App.module("HeaderApp").start()
        App.module("FooterApp").start()

    App.commands.setHandler "register:instance", (instance, id) ->
        App.register instance, id
    
    App.commands.setHandler "unregister:instance", (instance, id) ->
        App.unregister instance, id

    App.on "start", (options) ->
        @startHistory
            pushState: true
            root: ''
        @navigate(@rootRoute, trigger: true) unless @getCurrentRoute()

        # navigate on hash links
        $(document).on "click", "a", (event) =>
            return false unless $(event.currentTarget).attr("href")
            href = $(event.currentTarget).attr("href")
            passThrough = href.indexOf("sign_out") >= 0
            # if not sign_out or modified by key, navigate
            if not passThrough and not event.altKey and not event.ctrlKey and not event.metaKey and not event.shiftKey
                event.preventDefault()
                url = href.replace("^/", "").replace("#!", "").replace(app.root, "")
                @navigate url,
                    trigger: true
            # open link
            else
                window.open "#{Backbone.history.root}#{Backbone.history.getFragment href}"
                false

    App
