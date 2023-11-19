import smtplib
import ssl
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


def send_mail(send_to, subject, text, send_from, password, fileName=None,
              smtp_server="smtp.gmail.com", port=465):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    if fileName is not None:
        with open(fileName, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(fileName)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(fileName)
        msg.attach(part)

    ssl_pol = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=ssl_pol) as server:
        server.login(send_from, password)
        server.sendmail(send_from, send_to, msg.as_string())
