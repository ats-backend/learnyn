from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, DetailView

from results.models import Result, Token
from results.utils import render_to_pdf


class ResultView(DetailView):
    model = Result
    template_name = 'results.html'


class ResultDetailView(View):

    def get(self, request):
        token = Token.objects.create(student=request.user)
        print(token)

        context = {
            'token': token
        }
        return render(request, 'result/', context)


class GeneratePdf(View):

    def get(self, request, *args, **kwargs):
        data = {
            'today': "Today",
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('../templates/result/pdf/student_result.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
