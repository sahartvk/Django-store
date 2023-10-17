from django.http import HttpResponse
import csv


class ExportReserves():
    # columns = None
    translation = None
    queryset = None
    filename = 'table.cdv'

    def post(self, request):
        columns = list(self.translation.keys())

        data = request.POST

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={self.filename}'
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)

        writer.writerow(columns)

        data_queryset = self.queryset

        for key in data:
            if len(data[key]) != 0:
                data_queryset = data_queryset.filter(**{f"{self.translation[key]}__icontains": data[key]})

        data_queryset = data_queryset.values_list(*self.translation.values())

        for record in list(data_queryset):
            writer.writerow(record)
        return response
