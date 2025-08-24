from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import smtplib

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / ".." / ".." / "templates" / "letters"


def send_email_token(
    token: str,
    addr_recipient: str,
    url_confirm,
    email_sender,
    email_server_addr,
    email_server_port,
    passwd_email_sender,
):
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = addr_recipient
    msg["Subject"] = Header("Подтверждение регистрации", "utf-8")
    msg["Date"] = formatdate(localtime=True)
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("letter_accept_email.html")
    html_content = template.render(confirm_link=f"{url_confirm}?token={token}")
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    try:
        smtp = smtplib.SMTP(email_server_addr, email_server_port, timeout=10)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(email_sender, passwd_email_sender)
        smtp.sendmail(email_sender, addr_recipient, msg.as_string())
    except Exception as ex:
        print(ex)
    finally:
        smtp.quit()
