from django.core.mail import EmailMessage


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
                  f"student id: {receiver.student.id}\n" \
                  f"Class: {receiver.classroom}\n" \
                  f"You can set your password here: {action_url}"
    else:
        message = f"Hi {receiver.firstname}, \n" \
                  f"We are happy to you your child's result. Kindly visit the link below to download it." \
                  f"{action_url}"
    mail = EmailMessage(subject, message, to=[receiver.email], from_email='noreply@learnyn.com')

    mail.send()
