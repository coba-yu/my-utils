import os
from smtplib import SMTP
from email.header import Header
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def send(path: str, subject: str = '実験結果', body: str = '', config_path: str = 'gmail.conf',
         split: str = 'csv') -> None:

    if os.path.isfile(config_path):
        # ここはもうちょっとうまくやれるはずです
        with open(config_path, 'r') as f:
            lines = map(lambda x: x.rstrip('\n').split(':')[-1].replace(' ', ''), f.readlines())
            gmail_account, gmail_password, mail_to = lines
            print(gmail_account, gmail_password, mail_to)

        # MIME
        encoding = 'utf-8'
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, encoding)
        msg['To'] = mail_to
        msg['From'] = gmail_account

        # body
        body = MIMEText(body)
        msg.attach(body)

        # attach file
        attach = MIMEBase('application', split)
        with open(path, 'rb') as f:
            attach.set_payload(f.read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
        msg.attach(attach)

        # send
        gmail = SMTP("smtp.gmail.com", 587)
        gmail.starttls() # SMTP通信のコマンドを暗号化し、サーバーアクセスの認証を通す
        gmail.login(gmail_account, gmail_password)
        gmail.send_message(msg)

    else:
        with open(config_path, 'w') as f:
            f.write('gmail_account: 自分のGmailアドレス\n')
            f.write('gmail_password: パスワード\n')
            f.write('mail_to: 送信先アドレス(カンマ区切りで複数に遅れる)\n')
        raise FileNotFoundError(f'Fill information about gmail in {config_path}.')
