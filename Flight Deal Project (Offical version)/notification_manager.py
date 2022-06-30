from smtplib import SMTP
import os,ssl
from dotenv import load_dotenv
from email.message import EmailMessage

# my secret info
load_dotenv('C:/Users/n7kic/PycharmProjects/mysecret/.env')


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.host_name= 'smtp.gmail.com'
        self.sender_mail = SENDER_EMAIL
        self.pass_mail = PASS_EMAIL
        self.receiver_mail = 'tritht2607@gmail.com'
        self.message = EmailMessage()
        self.port = 587
        self.header = 'Good deal for new flight'

    def create_message(self,price, de_city, de_iata, arr_city, arr_iata, outbound_date,inbound_date):
        content = f'Only ${price} to fly from {de_city}-{de_iata} to {arr_city}-{arr_iata}, from {outbound_date} to {inbound_date} '
        self.message['Subject'] = self.header
        self.message.set_content(content)
        body = self.message.get_content()
        print({'Subject': self.header,
                'Body': body})
        del self.message['Subject']

    # def send_message(self):
    #     #     context = ssl.create_default_context()
    #     #     try:
    #     #         with SMTP(self.host_name, self.port) as server:
    #     #             server.starttls(context=context)
    #     #             server.login(user=self.sender_mail, password=self.pass_mail)
    #     #             server.send_message(msg=self.message, from_addr=self.sender_mail, to_addrs=self.receiver_mail)
    #     #             # server.sendmail(msg=message_as_string,from_addr=SENDER_EMAIL,to_addrs=RECEIVER)
    #     #     except Exception as e:
    #     #         print(e)
    #     #     finally:
    #     #         del self.message['Subject']