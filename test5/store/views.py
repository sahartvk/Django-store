from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product
from .tableview import TableView
from datatableview import Datatable, columns

# Create your views here.

@method_decorator(login_required(login_url="/login"), name="dispatch")
class ProductView(TableView):
    model = Product
    queryset = Product.objects.select_related('collection').order_by('id')
    template_name = 'datatableview/index.html'
    translation = {
        'کد محصول': 'id',
        'نام': 'title',
        'قیمت': 'unit_price',
        'کالکشن': 'collection__title',
        'توضیحات': 'collection__description'
    }
    filename = 'export_products.csv'

    def get_numerical_fields(self):
        return ["unit_price"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_name"] = 'products'
        return context

    class datatable_class(Datatable):
        collection_title = columns.TextColumn('کالکشن', sources=['collection__title'])
        collection_description = columns.TextColumn('توضیحات', sources=['collection__description'])

        class Meta:
            model = Product
            ordering = ["id"]
            page_length = 5
            columns = ["id", "title", "unit_price", "collection_title", "collection_description"]
            labels = {
                "id": 'کد محصول',
                "title": "نام",
                "unit_price": 'قیمت',
            }
