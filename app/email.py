import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.forms import ContactForm
from flask import render_template, url_for

def send_email():
    form = ContactForm()
    context = {
        'recipient': 'Peter Charland',
        'sender_name': form.name.data,
        'message': form.message.data,
        'sender_email': form.email.data,
        'form': form
    }
    message = Mail(
        from_email='no-reply@campaignforthequest.com',
        to_emails='petercharlandsilence@gmail.com',
        subject='Contact Form Submission',
        html_content=render_template('/email/email.html', **context))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e.message)
    return context
