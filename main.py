import time
import hashlib
from urllib.request import urlopen, Request
import smtplib
import ssl
from email.message import EmailMessage

"""
Open url
Read contents
Hash contents
compare hash contents every 10 sec
"""
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
                continue
        except Exception as e:
            print(e)
