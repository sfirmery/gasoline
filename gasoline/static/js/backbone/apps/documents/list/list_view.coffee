@Gasoline.module "DocumentsApp.List", (List, App, Backbone, Marionette, $, _) ->
	
	class List.LayoutView extends App.Views.LayoutView
		template: "documents/list/templates/list_layout"
		regions:
			resultsRegion: 		"#results-region"
			documentsRegion:		"#documents-region"
			paginationRegion:	"#pagination-region"

	class List.Document extends App.Views.ItemView
		template: "documents/list/templates/_document"
		tagName: "tr"

	class List.Documents extends App.Views.CompositeView
		template: "documents/list/templates/_documents"
		childView: List.Document
		childViewContainer: "tbody"
	
	class List.Results extends App.Views.ItemView
		template: "documents/list/templates/_results"
	
	class List.Pagination extends App.Views.ItemView
		template: "documents/list/templates/_pagination"
		className: "pull-right"
