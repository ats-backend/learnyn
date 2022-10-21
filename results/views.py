from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from accounts.models import Student, ClassAdmin
from results.forms import TokenForm, StudentResultForm, ResultFormset
from results.models import Result, Token
from results.utils import render_to_pdf, send_mail


class AddStudentResultView(View):
    def get(self, request):
        form = StudentResultForm()
        result_form = ResultFormset()

        if request.user.is_superuser:
            form = StudentResultForm()
        elif ClassAdmin.objects.filter(id=request.user.id):
            form.fields['student'].queryset = Student.objects.filter(classroom__teacher=request.user)
        context = {
            'form': form,
            'result_form': result_form
        }
        return render(request, 'result/add-result.html', context)

    def post(self, request):
        form = StudentResultForm(request.POST)
        result_form = ResultFormset(request.POST)

        if form.is_valid() and result_form.is_valid():
            student = form.cleaned_data.get('student')
            print(student, form.cleaned_data)
            if not Result.objects.filter(student=student).exists():
                for result in result_form.cleaned_data:
                    Result.objects.create(
                        student=student,
                        **result
                    )
                user_token = Token.objects.create(student=student)
                subject = "Result"
                send_mail(student, subject, user_token.token)
                return HttpResponseRedirect(
                    reverse('results:result_detail', args=[student.id])
                )
            messages.error(self.request, 'Make sure the student result is not exists before..')
            return redirect('results:add-result')
        return redirect('results:add-result')


class ResultView(View):

    def get(self, request):
        students = []
        if request.user.is_superuser:
            students = Student.objects.all()
        elif ClassAdmin.objects.filter(id=request.user.id).exists():
            students = Student.objects.filter(classroom__teacher=request.user)
        else:
            messages.info(self.request, "You need to obtain token to access this page.")
            return redirect('results:check-result')

        context = {
            'students': students
        }
        return render(request, 'results.html', context)


class ResultDetailView(View):

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        results = Result.objects.filter(student=student)

        context = {
            'student': student,
            'results': results
        }
        return render(request, 'result/result_detail.html', context)


class CheckResultView(View):
    def get(self, request):
        # student = Student.objects.get(id=request.user.id)
        # user_token = Token.objects.create(student=student)
        # print(user_token.token)
        form = TokenForm()
        context = {
            # 'user_token': user_token,
            'form': form
        }
        return render(request, 'result/check_result.html', context)

    def post(self, request):
        form = TokenForm(request.POST)

        if form.is_valid():
            user_token = form.cleaned_data.get('token')
            print(user_token)
            print(type(user_token))
            student_id = Token.objects.get(token=user_token)
            token = Token.objects.filter(token=user_token)
            if token.exists() and token.count() < 6:
                student_id.count += 1
                student_id.save()
                return redirect('results:result_detail', student_id.student.id)
            return redirect('results:check-result')


class GeneratePdf(View):

    def get(self, request, pk):
        student = Student.objects.get(pk=pk)
        results = Result.objects.filter(student=student)
        data = {
            'student': student,
            'results': results
        }
        pdf = render_to_pdf('../templates/result/pdf/student_result.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
