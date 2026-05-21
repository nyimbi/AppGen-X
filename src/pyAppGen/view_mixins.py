# view_mixins.py

from flask_appbuilder import expose, AppBuilder
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _



hide_list = ['created_by', 'changed_by', 'created_on', 'changed_on']

"""
The SearchableModelViewMixin class defines a custom search view that uses the DocMixin search functionality. 
The _get_search_query method retrieves the search query from the request arguments, and the _get_search_widgets method 
creates a list of widgets for the search results.

The on_model_change method updates the search vector when a record is added or modified. 
This ensures that the search vector is always up-to-date.

To use the SearchableModelViewMixin in your application, simply import it and include it as a base class when defining your views:
# views.py

from flask_appbuilder import ModelView
from .models import MyDocument
from .view_mixins import SearchableModelViewMixin

class MyDocumentModelView(SearchableModelViewMixin, ModelView):
    datamodel = SQLAInterface(MyDocument)
    list_columns = ["id", "title", "content"]
    search_template = "search_template.html"

"""
class SearchableModelViewMixin(object):
    @expose("/search/", methods=["GET", "POST"])
    def search(self):
        """
        Custom search view that uses the DocMixin search functionality.
        """
        search_query = self.appbuilder.get_session.query(self.datamodel.obj).search
        query = self._get_search_query()
        results = search_query(self.appbuilder.get_session, query)

        widgets = self._get_search_widgets(results)
        return self.render_template(
            self.search_template,
            title=_("Search"),
            widgets=widgets,
            appbuilder=self.appbuilder,
        )

    def _get_search_query(self):
        return self.appbuilder.request.args.get("q", "")

    def _get_search_widgets(self, results):
        widgets = []

        for result in results:
            item_view = self.__class__(self.appbuilder, datamodel=SQLAInterface(type(result)))
            widgets.extend(item_view.show_widget(result.id, show_in_modal=True))

        return widgets

    def on_model_change(self, form, model, is_created):
        """
        Update the search vector when a record is added or modified.
        """
        model.search_vector = model.doc_title + " " + model.doc_text + " " + model.comments
