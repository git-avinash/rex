import smtplib
import imghdr
from email.message import EmailMessage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def wait_for(webdriver, web_element: str) -> None:
    delay: int = 60
    try:
        WebDriverWait(webdriver, delay).until(
            EC.presence_of_element_located((By.XPATH, web_element)))
    except TimeoutException as e:
        pass


def mail_qr(mail_address: str, mail_password: str, mail_to: str, qr_img_path: str) -> None:
    EMAIL_ADDRESS: str = mail_address
    EMAIL_PASS: str = mail_password

    mail: EmailInit = EmailMessage()
    mail['Subject'] = 'QR Expires in 1 minutes'
    mail['From'] = EMAIL_ADDRESS
    mail['To'] = mail_to
    mail.set_content('QR Expires in 1 minute')

    with open(qr_img_path, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    mail.add_attachment(file_data, maintype='image',
                        subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(mail)
