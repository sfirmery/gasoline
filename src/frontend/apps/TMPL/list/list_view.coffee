@Gasoline.module "TMPLApp.List", (List, App, Backbone, Marionette, $, _) ->
	
	class List.LayoutView extends App.Views.LayoutView
		template: "tmpl/list/templates/list_layout"
		regions:
			resultsRegion: 		"#results-region"
			tmplRegion:		"#tmpl-region"
			paginationRegion:	"#pagination-region"

	class List.User extends App.Views.ItemView
		template: "tmpl/list/templates/_tmpl"
		tagName: "tr"

	class List.TMPL extends App.Views.CompositeView
		template: "tmpl/list/templates/_tmpl"
		childView: List.User
		childViewContainer: "tbody"
	
	class List.Results extends App.Views.ItemView
		template: "tmpl/list/templates/_results"
	
	class List.Pagination extends App.Views.ItemView
		template: "tmpl/list/templates/_pagination"
		className: "pull-right"
