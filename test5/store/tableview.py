from datatableview.views import DatatableView
from datatableview import Datatable, columns
from .ExportReserves import ExportReserves


class TableView(DatatableView, ExportReserves):
    model = None
    queryset = None
    template_name = 'datatableview/index.html'
    translation = None
    filename = 'data.csv'

    def get_numerical_fields(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_name"] = 'your table name'
        context["datatableview_options"] = self.datatable_class._meta
        context["numeric_fields"] = self.get_numerical_fields()
        return context

    class datatable_class(Datatable):
        class Meta:
            model = None
            ordering = ["id"]
            page_length = 10
