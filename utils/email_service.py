from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_email(subject, to, context, template_name):
    try:
        html_message = render_to_string(template_name=template_name, context=context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[to],
            html_message=html_message,
        )
    except:
        pass

# def send_email(subject, to, context, template_name):
#     try:
#         html_message = render_to_string(template_name=template_name, context=context)
#         plain_message = strip_tags(html_message)
#         from_email = settings.EMAIL_HOST_USER
#         email = EmailMessage(
#             subject=subject,
#             body=plain_message,
#             from_email=from_email,
#             to=[to]
#         )
#         email.content_subtype = "html" # Set the content type to HTML
#         # email.attach(html_message, "text/html") # Attach the HTML content
#
#         email.send()
#     except:
#         pass