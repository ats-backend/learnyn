from io import BytesIO
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import get_template

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def send_mail(receiver, subject, user_token):
    message = f"Hi {receiver.first_name}, \n" \
              f"Your result has been released. This is token to check your result: {user_token}"
    mail = EmailMessage(subject, message, to=[receiver.email], from_email='noreply@learnyn.com')

    mail.send()
