@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->
	
	App.commands.setHandler "when:fetched", (entities, callback) ->

		# append callback to entities fetch
		_.chain([entities]).flatten().forEach (item) ->
			$.when(item.fetch()).done ->
				callback()
