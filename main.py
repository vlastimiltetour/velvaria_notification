from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def scrape():
    url = 'https://www.velvaria.cz/#free'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table',{'class':'table table-condensed'})

    headers = []
    data_list = []

    for h in table.find_all('th'):
        title = h.text
        headers.append(title)

    for row in table.find_all('tr'):
        data = row.find_all('td')
        row_data = [td.text.strip() for td in data]
        data_list.append(row_data)

    df = pd.DataFrame(data=data_list, columns=headers)
    return df

def simple_pandas_scraper():
    url = 'https://www.velvaria.cz/#free'
    pd_scraper = pd.read_html(url)
    return pd_scraper[0]



def send_mail(data):
    port = 587
    password = 'wbfdyjqbrpodzufw'
    sender_email = 'vlkscraper@outlook.com'
    receiver_email = 'v.tetour@gmail.com'
    smtp_server = 'smtp.outlook.com'

    message = MIMEMultipart()
    message['Subject'] = 'Velvaria Apartmany'
    message['From'] = sender_email
    message['To'] = receiver_email

    html = MIMEText(data.to_html(index=False), 'html')

    message.attach(html)

    context = ssl.create_default_context()


    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()

    print('sending was successful')

if __name__ == "__main__":
    scrape()
    data = scrape()
    send_mail(data)


