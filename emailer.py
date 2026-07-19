import os
import smtplib

from email.message import EmailMessage

from config import (
    EMAIL,
    APP_PASSWORD,
    DESTINATION,
    SMTP_SERVER,
    SMTP_PORT
)


def send_email(subject, body, attachment):

    if not os.path.exists(attachment):
        print("Fișierul nu există:", attachment)
        return False

    msg = EmailMessage()

    msg["From"] = EMAIL
    msg["To"] = DESTINATION
    msg["Subject"] = subject

    msg.set_content(body)

    with open(attachment, "rb") as f:
        file_data = f.read()

    filename = os.path.basename(attachment)

    msg.add_attachment(
        file_data,
        maintype="text",
        subtype="csv",
        filename=filename
    )

    try:

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        server.starttls()

        server.login(
            EMAIL,
            APP_PASSWORD
        )

        server.send_message(msg)

        server.quit()

        print("Email trimis cu succes.")

        return True

    except Exception as e:

        print("Eroare la trimiterea emailului:")

        print(e)

        return False