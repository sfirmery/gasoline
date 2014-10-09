@Gasoline.module "DashboardApp.Show", (Show, App, Backbone, Marionette, $, _) ->

	class Show.LayoutView extends App.Views.LayoutView
		template: _.template($('#dashboardShowLayout').html())

		regions:
			usersRegion: "#users-region"
