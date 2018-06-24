from config import EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_LIST
from email.mime.text import MIMEText
from smtplib import SMTP


def send_available(hotel: str, to=EMAIL_LIST):
    with open('templates/hotel_available.html', 'r') as f:
        email_contents = f.read()
    
    message = MIMEText(email_contents.format(hotel=hotel), 'html')
    message['From'] = f'Dragoncon Scrape <{EMAIL_USERNAME}>'
    message['To'] = ','.join(to)
    message['Subject'] = f'{hotel} available'

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USERNAME, to, message.as_string())
    server.quit()
