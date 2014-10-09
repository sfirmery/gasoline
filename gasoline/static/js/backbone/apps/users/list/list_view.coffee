@Gasoline.module "UsersApp.List", (List, App, Backbone, Marionette, $, _) ->
	
	class List.LayoutView extends App.Views.LayoutView
		template: "users/list/templates/list_layout"
		regions:
			resultsRegion: 		"#results-region"
			usersRegion:		"#users-region"
			paginationRegion:	"#pagination-region"

	class List.User extends App.Views.ItemView
		template: "users/list/templates/_user"
		tagName: "tr"

	class List.Users extends App.Views.CompositeView
		template: "users/list/templates/_users"
		childView: List.User
		childViewContainer: "tbody"
	
	class List.Results extends App.Views.ItemView
		template: "users/list/templates/_results"
	
	class List.Pagination extends App.Views.ItemView
		template: "users/list/templates/_pagination"
		className: "pull-right"
