import os
import base64

from datetime import datetime as dt
import pandas as pd

import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

email_smtp_api = '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'
from_email = 'pomprawit@hotmail.com'

def send_email(to_email, msg, f_data):
    # send noti. to email
    try:
        if to_email == '':
            raise Exception("Email is invalid")
        # send email message to sendgrid mail server
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject='Sending with DeepOcean',
            html_content=f'<strong>{msg}</strong>',
        )

        encoded_file = base64.b64encode(f_data).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('attachment.pdf'),
            FileType('application/pdf'),
            Disposition('attachment')
        )
        message.attachment = attachedFile

        sg = SendGridAPIClient(email_smtp_api)
        response = sg.send(message)
        print("Send email response: " + response)
    except Exception as e:
        print("Error send email noti.:", e)

def read_pdf(file_name):
    data = None
    with open(file_name, 'rb') as f:
        data = f.read()
        f.close()
    return data

def read_txt(file_name):
    data = None
    with open(file_name, 'r', encoding="utf-8") as f:
        data = f.read()
        f.close()
    return data

if __name__ == "__main__":
    src_df = pd.read_excel("performance_report.xlsx")
    src_df = src_df.reset_index()  

    for index, row in src_df.iterrows():
        strategy = row["strategy"][:-3]
        perf_rpt_pdf = read_pdf(f'pdf/{row["name"]}.pdf')
        email_msg_txt = read_txt(f"result/{strategy}_{row['name']}.txt")
        send_email("pomprawit@hotmail.com", email_msg_txt, perf_rpt_pdf)