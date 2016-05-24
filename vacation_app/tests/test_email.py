from django.core import mail

from django.test import TestCase


class EmailTest(TestCase):

    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
                       'arseniysychev@gmail.com', ['arseniys@ua.fm'],
                       fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
