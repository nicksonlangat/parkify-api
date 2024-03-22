from __future__ import annotations

import logging
from email.mime.image import MIMEImage
from functools import lru_cache

from celery import shared_task
from django.contrib.staticfiles import finders
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags


@shared_task
def send_queued_email(data):
    mail = Mail(
        from_email=data["from"],
        to=data["to"],
        subject=data["subject"],
        body=data["body"],
        alternatives=data["alternatives"],
        attachments=data["attachments"],
    )

    mail.send()

    return "sent"


class Mail(EmailMultiAlternatives):
    template_name = None
    template_data = None

    def __init__(
        self, template_name=template_name, template_data=template_data, *args, **kwargs
    ):
        self.template_name = template_name
        self.template_data = template_data

        super().__init__(*args, **kwargs)

    def template(self, name: object, data: object = None) -> Mail:
        self.template_name = name
        self.template_data = data

        return self

    def text(self, text):
        self.template("email_text.html", {"text": text})
        return self

    def set_from_email(self, email, name=None):
        if name is None:
            self.from_email = email
        else:
            self.from_email = f"{name} <{email}>"

    def _prepare(self):
        if self.template_name is not None:
            html = get_template(self.template_name).render(self.template_data)
            self.attach_alternative(html, "text/html")

            if self.body is None or self.body == "":
                self.body = strip_tags(html)

    def send(self, *args, **kwargs):
        self._prepare()
        # self.attach_images()
        super().send(*args, **kwargs)

    @lru_cache()
    def attach_images(self):
        default_images = {
            "logo": "logo.png",
            "email_icon": "ico-email.png",
            "phone_icon": "ico-phone.png",
            "web_icon": "ico-web.png",
            "facebook_icon": "facebook.png",
            "twitter_icon": "twitter.png",
            "linkedin_icon": "linkedin.png",
            "instagram_icon": "instagram.png",
        }

        for key, file in default_images.items():
            if key in self.body or file in self.body:
                self.attach_inline_image(key, file)
            else:
                alternatives = self.alternatives
                for alternative in alternatives:
                    body = alternative[0]
                    if key in body or file in body:
                        self.attach_inline_image(key, file)

    def attach_inline_image(self, cid, path, location="static/resources/"):
        with open(finders.find(location + path), "rb") as f:
            file_data = f.read()

        file_mime = MIMEImage(file_data)
        file_mime.add_header("Content-ID", "<" + cid + ">")
        self.attach(file_mime)

        return self

    def queue(self):
        self._prepare()

        email_data = {
            "to": self.to,
            "from": self.from_email,
            "subject": self.subject,
            "body": self.body,
            "alternatives": self.alternatives,
            "attachments": self.attachments,
        }

        try:
            send_queued_email.delay(email_data)
        except Exception:
            self.send()
            logging.exception("Could not queue email, sent synchronously")
