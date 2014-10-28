@Gasoline.module "FooterApp.Show", (Show, App, Backbone, Marionette, $, _) ->

	class Show.LayoutView extends App.Views.LayoutView
        template: "footer/show/show_layout"

		regions:
			fooRegion: "#foo-region"