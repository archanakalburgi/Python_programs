import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import urllib.request 


content = urllib.request.urlopen('https://www.ioptechnologies.com')
req = requests.get("https://www.ioptechnologies.com")
soup = BeautifulSoup(req.content, 'html.parser')
for soup in content:
    words=len(soup.split())
    plt.hist(len(soup),50)
    plt.xlabel('Length of a sample')
    plt.ylabel('Number of samples')
    plt.title('Sample length distribution')
    plt.show()
#print(np.median(words))

