@Gasoline.module "SpacesApp.List", (List, App, Backbone, Marionette, $, _) ->
	
	class List.LayoutView extends App.Views.LayoutView
		template: "spaces/list/list_layout"
		regions:
			resultsRegion: 		"#results-region"
			spacesRegion:		"#spaces-region"
			paginationRegion:	"#pagination-region"

	class List.Space extends App.Views.ItemView
		template: "spaces/list/_space"
		tagName: "tr"

	class List.Spaces extends App.Views.CompositeView
		template: "spaces/list/_spaces"
		childView: List.Space
		childViewContainer: "tbody"
	
	class List.Results extends App.Views.ItemView
		template: "spaces/list/_results"
	
	class List.Pagination extends App.Views.ItemView
		template: "spaces/list/_pagination"
		className: "pull-right"
