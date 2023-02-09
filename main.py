import time
import hashlib
from urllib.request import urlopen, Request
import smtplib
import ssl
from email.message import EmailMessage


#setting User-Agent header to make the script appear as a legitimate browser
url=Request('https://news.ycombinator.com/', headers={'User-Agent': 'Mozilla/5.0'})


with urlopen(url) as response:
    contents = response.read()
    current_website_hash=hashlib.sha224(contents).hexdigest()
    print("<==hashing current website content==>")
    
    while True:
        try:
            time.sleep(30)
            new_contents=urlopen(url).read()
            new_website_hash=hashlib.sha224(new_contents).hexdigest()
            if current_website_hash == new_website_hash:
                continue
            else:
                print("There's been content updated on the site")
                newer_contents=urlopen(url).read()
                newer_website_hash=hashlib.sha224(newer_contents).hexdigest()
                current_website_hash=newer_website_hash
                time.sleep(30)
                
                port = 465
                smtp_server = "smtp.gmail.com"
                sender_email="sender.email@gmail.com"
                receiver_email="receiver.email@gmail.com"
                password="xxxxxxxxxxxxxxxx"
                subject="Website has been updated with changes"
                body=f"""
                Hi {receiver_email.split('@')[0]}
                The site has been updated with new content.
                
                """
                em=EmailMessage()
                em["From"]=sender_email
                em["To"]=receiver_email
                em["Subject"]=subject
                em.set_content(body)
                #for secure communication
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email,password)
                    server.sendmail(sender_email, receiver_email, em.as_string())
                continue
        except Exception as e:
            print(e)
