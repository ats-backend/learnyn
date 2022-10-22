from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import View

from accounts.models import Student, ClassAdmin
from results.forms import TokenForm, StudentResultForm, ResultFormset, ResultForm
from results.models import Result, Token
from results.utils import render_to_pdf, send_mail
from school.models import Subject, Term, Session


class AddStudentResultView(LoginRequiredMixin, View):
    def get(self, request):
        form = StudentResultForm()
        result_forms = ResultFormset()
        result_form = []
        for result_form in result_forms:
            if not request.user.is_superuser:
                result_form.fields['subject'].queryset = Subject.objects.filter(classroom__teacher=request.user)

        if request.user.is_superuser:
            form = StudentResultForm()
        elif ClassAdmin.objects.filter(id=request.user.id):
            form.fields['student'].queryset = Student.objects.filter(classroom__teacher=request.user)
        context = {
            'form': form,
            'result_forms': result_forms
        }
        return render(request, 'result/add-result.html', context)

    def post(self, request):
        form = StudentResultForm(request.POST)
        result_form = ResultFormset(request.POST)

        if form.is_valid() and result_form.is_valid():
            student = form.cleaned_data.get('student')
            r_term = form.cleaned_data.get('r_term')
            r_session = form.cleaned_data.get('session')
            print(r_term, type(r_term))
            print(r_session, type(r_session))
            try:
                term = Term.objects.get_or_create(session=r_session, term=r_term)
                get_term = Term.objects.get(session=r_session)
                print(get_term.id)
            except IntegrityError:
                return redirect('results:add-result')

            if not Result.objects.filter(student=student, session=r_session, term=get_term).exists():
                print(student)
                for result in result_form.cleaned_data:
                    Result.objects.create(
                        student=student,
                        session=r_session,
                        term=get_term,
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
        print(form.errors)
        print(result_form.errors)
        print(result_form.non_form_errors())
        return redirect('results:add-result')


class ResultView(LoginRequiredMixin, View):

    def get(self, request):
        # students = []
        if request.user.is_superuser:
            results = Result.objects.all().values_list('student', flat=True)
            print(results)
            students = Student.objects.filter(id__in=results).exclude(is_suspended=True)
        elif ClassAdmin.objects.filter(id=request.user.id).exists():
            results = Result.objects.filter(student__classroom__teacher=request.user).values_list('student', flat=True)
            print(results)
            students = Student.objects.filter(id__in=results)
        else:
            messages.info(self.request, "You need to obtain token to access this page.")
            return redirect('results:check-result')

        context = {
            'students': students
        }
        return render(request, 'results.html', context)


class ResultDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        results = Result.objects.filter(student=student)
        student_result = Result.objects.filter(student=student).first()

        context = {
            'student': student,
            'results': results,
            'student_result': student_result
        }
        return render(request, 'result/result_detail.html', context)


class CheckResultView(LoginRequiredMixin, View):
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
            try:
                student_id = Token.objects.get(token=user_token)
                print(student_id)
            except Token.DoesNotExist:
                return redirect('results:check-result')
            token = Token.objects.filter(token=user_token)
            if token.exists() and token.count() < 6:
                student_id.count += 1
                student_id.save()
                return redirect('results:result_detail', student_id.student.id)
            return redirect('results:check-result')


class GeneratePdf(LoginRequiredMixin, View):

    def get(self, request, pk):
        student = Student.objects.get(pk=pk)
        results = Result.objects.filter(student=student)
        student_result = Result.objects.filter(student=student).first()
        data = {
            'student': student,
            'results': results,
            'student_result': student_result,
        }
        pdf = render_to_pdf('../templates/result/pdf/student_result.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
