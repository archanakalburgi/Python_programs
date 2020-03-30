import urllib.request 
from bs4 import BeautifulSoup 
import requests
from difflib import get_close_matches

urls = ['https://www.ioptechnologies.com',
        'https://www.bitjini.net',
        'https://www.coursera.org',
        'https://www.gehealthcare.com']

keyword_educational = ['Course',
                       'Certificate',
                       'Skills',
                       'Tutorial',
                       'Textbook',
                       'Learning',
                       'Education',
                       'Lessons',
                       'Books']

keyword_IT_Business = ['App',
                       'Software',
                       'Software solution',
                       'IT solution',
                       'Hacking',
                       'Clients',
                       'Computing',
                       'E_commerce'
                       'Delivering',
                       'Team']

keyword_health = ['Healthcare',
                  'Care',
                  'Health',
                  'Testing',
                  'Clinical',
                  'Bone',
                  'Surgical',
                  'Diagnostic',
                  'ECG',
                  'Ultrasound',
                  'X-ray',
                  'Health solution']

def comparing_keywords(txt):

    if (str(keyword_educational) in txt):
                print("It's an educational website")
            
    elif (str(keyword_IT_Business) in txt):
                print("It's an IT Business website")

    else:
                print("It's a healthcare website")

try:
    for url in urls:
        print("\n") 
        print('url --> ', url)
        content = urllib.request.urlopen(url,timeout=60)
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        for p in soup.find_all('p'):
            print("\n")
            txt=p.get_text()
            print (txt)
            print("\n")
        comparing_keywords(txt)

except IndexError:
    print("Out of loop range")