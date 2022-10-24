from .models import ResetPasswordToken
from classadmins.models import ClassAdmin
from students.models import Student

import datetime


def get_current_user(request):

    student = Student.objects.filter(id=request.user.id).first()
    class_admin = ClassAdmin.objects.filter(id=request.user.id).first()
    if student:
        current_user = student
    elif class_admin:
        current_user = class_admin
    else:
        current_user = None

    return dict(current_user=current_user)


def check_class_admin(request):
    is_class_admin = ClassAdmin.objects.filter(id=request.user.id).exists()

    return dict(is_class_admin=is_class_admin)


def delete_old_token(request):
    context = {}
    tokens = ResetPasswordToken.objects.all()
    for token in tokens:
        if token.date_created.isoformat() > (token.date_created + datetime.timedelta(minutes=5)).isoformat():
            token.delete()

    return context



