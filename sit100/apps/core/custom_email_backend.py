# core/custom_email_backend.py
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
from django.core.mail.backends.smtp import EmailBackend


class SSLNotVerifyingEmailBackend(EmailBackend):
    def send_messages(self, email_messages):
        """Send messages using SMTP_SSL with unverified context."""
        sent_count = 0
        with smtplib.SMTP_SSL(
            self.host,
            self.port,
            context=ssl._create_unverified_context()
        ) as server:
            server.login(self.username, self.password)
            for message in email_messages:
                msg = MIMEMultipart('alternative')
                msg['From'] = message.from_email
                msg['To'] = ', '.join(message.to)
                msg['Subject'] = message.subject

                # Aggiungi prima la versione testo
                if message.body:
                    msg.attach(MIMEText(message.body, 'plain'))

                # Cerca contenuto HTML nelle alternative
                html_content = None
                for content, mimetype in message.alternatives:
                    if mimetype == 'text/html':
                        html_content = content
                        break

                # Se c'è contenuto HTML, aggiungilo
                if html_content:
                    msg.attach(MIMEText(html_content, 'html'))
                # Altrimenti usa il body come HTML se non c'è già una versione testo
                elif not message.body:
                    msg.attach(MIMEText(message.body, 'html'))

                server.sendmail(
                    message.from_email,
                    message.to,
                    msg.as_string()
                )
                sent_count += 1
        return sent_count
