@Gasoline.module "HeaderApp.List", (List, App, Backbone, Marionette, $, _) ->

	class List.LayoutView extends App.Views.LayoutView
        template: "header/list/templates/list_layout"

		regions:
			fooRegion: "#foo-region"