from typing import Dict

from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings


def send_mail(receiver, subject, action_url):
    if "new account" in subject and "student" not in subject:
        message = f"Hi {receiver.first_name}, \n" \
                  f"You've been made a class administrator for {receiver.classroom}. The details for your access " \
                  f"account are:\n" \
                  f"email: {receiver.email}\n" \
                  f"You can set your password here: {action_url}"
    elif "student" in subject:
        message = f"Hi {receiver.first_name}, \n" \
                  f"The details to access your school account are:\n" \
                  f"email: {receiver.email}\n" \
                  f"student id: {receiver.student_id}\n" \
                  f"Class: {receiver.classroom}\n" \
                  f"You can set your password here: {action_url}"
    else:
        message = f"Hi {receiver.firstname}, \n" \
                  f"We are happy to you your child's result. Kindly visit the link below to download it." \
                  f"{action_url}"
    mail = EmailMessage(subject, message, to=[receiver.email], from_email='noreply@learnyn.com')

    mail.send()


def send_password_reset_mail(email_body: Dict, context: Dict):
    """
       Send mail function to the specified email
       """
    print(email_body)
    print(context)
    try:
        message_template = get_template("password_mail.html").render(context)

        subject = email_body['subject']
        message = message_template
        email_from = settings.EMAIL_HOST_USER
        recipient_list = email_body['recipient']

        msg = EmailMessage(
            subject,
            message,
            email_from,
            to=[recipient_list]
        )
        print(message)
        print(context)
        print(msg)
        msg.send()
        print("email sent successfully")
    except Exception as e:
        print(e)
        return False
