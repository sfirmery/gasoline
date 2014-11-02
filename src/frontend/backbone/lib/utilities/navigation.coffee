@Gasoline.module "Utilities", (Utilities, App, Backbone, Marionette, $, _) ->

  _.extend App,

    navigate: (route, options = {}) ->
      Backbone.history.navigate route, options
      @historyHits++

    navigateBack: (options = {}) ->
      if @historyHits > 0
        window.history.back()
        @historyHits--

    getCurrentRoute: ->
      frag = Backbone.history.fragment
      if _.isEmpty(frag) then null else frag

    startHistory: (options) ->
      if Backbone.history
        @historyHits = 0
        Backbone.history.start(options)
