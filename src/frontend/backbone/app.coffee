@Gasoline = do (Backbone, Marionette) ->
  
  App = new Marionette.Application        
  
  App.addRegions
    headerRegion:   "#header-region"
    mainRegion:     "#main-region"
    footerRegion:   "#footer-region"
  
  App.rootRoute = "documents/main"

  App.reqres.setHandler "default:region", -> App.mainRegion

  App.addInitializer ->
    App.module("HeaderApp").start()
    App.module("FooterApp").start()

  App.on "start", ->
    ## create our specialized dialog region
    @addRegions dialogRegion: { selector: "#dialog-region", regionClass: App.Regions.Dialog }

    ## starts listening to Backbone History
    @startHistory
      pushState: true
      root: ''

    ## navigates us to the root route unless we're already navigated somewhere else
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
        destination = if passThrough then '_top' else '_blank'
        window.open "#{Backbone.history.root}#{Backbone.history.getFragment href}", destination
        false

  App
