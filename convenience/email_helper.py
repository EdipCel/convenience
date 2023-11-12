import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.wdp_api_util import read_wdp_apixml
from utils.ConfigUtils import Config
from datetime import datetime


def send_email(body, _to=None, subject=None, reply_to=None):
    """
    Sends email using the account provided in the config file and authentication xml, and account details are hardcoded.
    https://pythoncircle.com/post/36/how-to-send-email-from-python-and-django-using-office-365/
    """
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart("alternative")

    # We need to get default email settings from the config ini file
    config = Config()

    if _to == None:
        msg['To'] = config.MAIL['To']
    else:
        msg['To'] = _to

    if subject == None:
        msg['Subject'] = config.MAIL['Subject']
    else:
        msg['Subject'] = subject

    msg['Reply-To'] = reply_to

    # see the code below to use template as body
    body_html = body
    
    # get encrypted authentication details from auth file.
    user, password = read_wdp_apixml(config.MAIL['AuthXmlFile'])
    
    msg['From'] = user

    # Create the body of the message (a plain-text and an HTML version).
    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(body_text, "plain")
    message_part = MIMEText(body_html, "html")

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    # msg.attach(part1)
    msg.attach(message_part)

    # Send the message via local SMTP server.
    mail = smtplib.SMTP("smtp.outlook.office365.com", 587, timeout=20)
  
    # if tls = True
    mail.starttls()
  
    mail.login(user, password)

    
    mail.sendmail(msg['From'], msg['To'], msg.as_string())
    mail.quit()

    
def send_activity_email(message_body):
    """
    this function is used to send email notifications about critical errors.
    If the database is not available and we are not able to log the problem we will be sending out emails.
    """
    console = Console(log_path=False)
    maildatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = maildatetime + " <br> " + message_body
    send_email(body=body)
    console.log("Notification email sent: " + body)
