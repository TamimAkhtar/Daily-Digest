import dd_content
import datetime
import smtplib
from email.message import EmailMessage

class DailyDigestEmail:
    def __init__(self):
        self.content = {'quote' : {'include' : True, 'content': dd_content.get_random_quote()},
                        'weather' : {'include' : True, 'content': dd_content.get_weather_forecast()},
                        'googletrends' : {'include' : True, 'content': dd_content.get_google_trends()},
                        'wikipedia' : {'include' : True, 'content': dd_content.get_wikipedia_article()}
                        }

        self.recepient_list = ['curlytwirly1998@gmail.com',
                                'tamimakhter3@gmail.com']

        self.sender_credentials = {'email' : 'tamimakhter_3@hotmail.com',
                                    'password' : 'Aaalllmmm00'}
    
    """
    Send Digest Email to all recepients
    """
    def send_email(self):
        #build message
        msg = EmailMessage()
        msg['Subject'] = f'Daily Digest - {datetime.date.today().strftime("%d-%b-%Y")}'
        msg['From'] = self.sender_credentials['email']
        msg['To'] = ', '.join(self.recepient_list)

        #add Plaintext and HTML content
        msg_body = self. format_message()
        msg.set_content(msg_body['text'])
        msg.add_alternative(msg_body['html'], subtype = 'html')

        #Secure Connection with smtp server and ssend email
        with smtplib.SMTP('smtp.office365.com' , 587) as server:
            server.starttls()
            server.login(self.sender_credentials['email'],
                        self.sender_credentials['password'])
            server.send_message(msg)


    def format_message(self):
        #########################
        ## Generate PlainText ##
        ########################
        text = f'*~*~*~*~* Daily Digest - {datetime.date.today().strftime("%d %b %Y")} *~*~*~*~*\n\n'
        
        #format quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            text+= '*~*~* Quote of the Day *~*~* \n\n'
            text+= f'{self.content["quote"]["content"]}\n\n'

        #format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            text += f'*~*~* Forecast for {self.content["weather"]["content"]["country"]}, {self.content["weather"]["content"]["city"]} is {self.content["weather"]["content"]["condition"]} with a temperature of {self.content["weather"]["content"]["temp"]}*~*~*\n\n'
        
        #format google trends
        if self.content['googletrends']['include'] and self.content['googletrends']['content']:
            text += '*~*~* Top Ten Google Trends for today *~*~*\n\n'
            for trend in self.content['googletrends']['content'][0:10]:
                text += f'{trend}\n'
            text += '\n'

        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            text += '*~*~* Daily Random Learning *~*~*\n\n'
            text += f'{self.content["wikipedia"]["content"]["title"]}\n{self.content["wikipedia"]["content"]["extract"]}'

        ####################
        ## Generate HTML ##
        ###################
        
        html = f"""<html>
    <body>
    <center>
        <h1>Daily Digest - {datetime.date.today().strftime("%d %b %Y")}</h1>
        """

        #format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            html += f"""<h2>Quote of the Day</h2>
            <i>"{self.content['quote']['content']}"</i>
            """

        #format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            html += f"""<h2>Weather of the Day</h2>
            <p>Forecast for {self.content["weather"]["content"]["country"]}, {self.content["weather"]["content"]["city"]} is {self.content["weather"]["content"]["condition"]} with a temperature of {self.content["weather"]["content"]["temp"]}</p>
            """
        
        #format google trends
        if self.content['googletrends']['include'] and self.content['googletrends']['content']:
            html += f"""<h2>Top 10 Google Trends</h2>
                    """
            for trend in self.content['googletrends']['content'][0:10]:
                html+= f"""
            <li><b>{trend}</b></li>
            """

        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            html += f"""
        <h2>Daily Random Learning</h2>
        <h3><a href="{self.content['wikipedia']['content']['Link']}">{self.content['wikipedia']['content']['title']}</a></h3>
        <table width="800">
            <tr>
                <td>{self.content['wikipedia']['content']['extract']}</td>
            </tr>
        </table>
                    """
        # footer
        html += """
        </center>
        </body>
        </html>
                """

        return {'text': text, 'html': html}

if __name__=='__main__':
    email = DailyDigestEmail()

    #testing format_message()
    print('\nTesting email body generation')
    message = email.format_message()

    #testing send_email()
    print('\nSending Test Email....')
    email.send_email()

    #print plaintext and HTML message
    print('\nPlaintext email body is...')
    print(message['text'])
    print('\n------------------------------------------------------------')
    print('\nHTML email body is...')
    print(message['html'])
    
    
    # save Plaintext and HTML messages to file
    with open('message_text.txt', 'w', encoding='utf-8') as f:
        f.write(message['text'])
    with open('message_html.html', 'w', encoding='utf-8') as f:
        f.write(message['html'])