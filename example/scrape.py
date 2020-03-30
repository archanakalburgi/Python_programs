import requests
import re
from bs4 import BeautifulSoup
import csv
#from googletrans import Translator
import multiprocessing
import os
import time

#translator = Translator()

# MAX_LINKS = 20
WEIGHT_COL = 5

pages_list = ["About", "services", "products", "home"]

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'nav']:
    # if element.parent.name in ['head']:
        return False
    return True

def get_keywords(file_path):
    keywords_list = []
    weights = []
    with open(file_path, 'rt') as f:
        data = csv.reader(f)
        i = 0                                       #i=0,1,2
        for row in data:                            #Managed Services	Information Services	ITIL			20
            if i != 0:                              #true
                key_row = []                        #key_row = []
                j = 0                               #j=0
                for col in row:                     #col=managed services
                    if j == WEIGHT_COL:             #(0==5, 1==5, 2==5, 3==5, 4==5, 5==5) true
                        weights.append(col)         #weights=[20]
                    else:                           #false 
                        key_row.append(col)         #key_row[]
                    j = j + 1                       #j=0+1=1+1=2+1=3+1=4+1=5+1=6
                keywords_list.append(key_row)       #keywords_list=[[Iaas,Infracture as a service,cloud service,cloud solutions,cloud]]
            i = i + 1                               #i=0+1=1+1=2

    return ([keywords_list, weights])

def get_urls(file_path):
    urls = []
    with open(file_path, 'rb') as f:
        data = csv.reader(f)
        try:
            for row in data:      #row=[www.cht.com.tw]
                if not row:       #false
                    continue      
                if 'http' in row[0]:    #row[0]=www.cht.com.tw -----> false
                    urls.append(row[0])  #urls=[http://www.chinasonangol.com]  
                elif 'www' in row[0]:   #true  
                    if row[0].startswith('http'): #false
                        urls.append(row[0])
                    else:                           
                        urls.append('http://' + row[0]) #urls=[[http://www.chinasonangol.com], [http://www.cht.com.tw]]  
        except Exception as e:
            print('Exception in get_urls : ', e)
    return (urls)

def process_scores(keywords_list, weights, url,q):
    starttime = time.time() 
    scores = []
    url_result = []
    # for url in urls:
    print('url ---------> ', url)
    try:
        response = requests.get(url)            
        soup = BeautifulSoup(response.text, 'html5lib')
        url_count = 0
        ddos = 0
        keywords_vault = []
        stored_keyword = []
        link_count = 0
        # page_count = 0
        found = False
        tags_list = []

        for page in pages_list:             #page=about,services,porudcts,home
            for tag in soup.find_all(['a'], string=re.compile(page, re.IGNORECASE)): #about,services,products,home
                tags_list.append(tag) #tags_list=[about,services,products,home]
                if len(tags_list) > 0: #true,true,true
                    found = True  #found=true,true,true,true...

        for a in remove(tags_list): #tag_list=[about,services,products],a=about
            page_count = 0      #page_count=0
            link = a.get('href')  #link="all the contents in the href page"      

            if link is not None:    #true
                if not 'htt' in link:       
                    if url.endswith('/'):
                        link = url + link
                    else:
                        link = url + '/' + link

            # link_count = link_count + 1
            # if link_count > MAX_LINKS:
            #     break

            if found:
                try:
                    page_count = 0
                    response2 = requests.get(link)
                    html_text = response2.content
                    soup2 = BeautifulSoup(html_text, 'html5lib')
 
                    lang_texts = ' '.join(map(lambda p: p.text, soup2.find_all('p')))
                    texts = soup2.findAll(text=True)
                    visible_texts = filter(tag_visible, texts)
                    # visible_texts = ""

                    if len(lang_texts) > 0:
                        detect = translator.detect(lang_texts)
                        if detect.lang != 'en':
                            translated = translator.translate(lang_texts)
                            visible_texts = translated.text
                    else:
                        continue
                    for text in visible_texts:
                        text = text.strip()

                        for synonyms in keywords_list:  #synonym=IaaS
                            if synonyms == "":
                                continue
                            key_count = 0               #key_count=0
                            main_keyword = synonyms[0]  #main_keyword=IaaS
                            for keyword in synonyms:    #keyword=IaaS

                                if keyword != "":       #true
                                    count_keyword = len(re.findall(keyword, text)) #count_keyword=1
                                    if count_keyword > 0:           #true
                                        #page_count = page_count + count_keyword
                                        key_count = key_count + count_keyword      #key_count=0+1=1

                                        if main_keyword not in keywords_vault: #true (Iaas not in [])
                                            keywords_vault.append(main_keyword) #keyword_vault=[IaaS]
                                            stored_keyword.append({main_keyword: key_count}) #stored_keyword=[{IaaS:1}]
                                        else:
                                            i = 0                           #i=0
                                            for keys in stored_keyword:     #keys=services
                                                if list(keys)[0] == main_keyword:
                                                    stored_keyword[i][main_keyword] = stored_keyword[i][main_keyword] + key_count
                                                    page_count = page_count + key_count
                                                i = i + 1
                                                
                                    else:
                                        if main_keyword not in keywords_vault:
                                            keywords_vault.append(main_keyword)
                                            stored_keyword.append({main_keyword: 0})

                except Exception as e:
                    # print('exception error',e)
                    ddos = 1
            url_count = url_count + page_count
        weighted_score = 0
        i = 0
        for stored_keys in stored_keyword:
            for keyword, count in stored_keys.items():
                weighted_score = (weighted_score + (count * float(weights[i])) / 100)
                i = i + 1
        weighted_score = weighted_score / (url_count)
        scores.append({'URL': url, 'keywords': stored_keyword, 'score': url_count,'weighted_score': (weighted_score), 'ddos': ddos})
        
    except Exception as e:
        # print('error',e)                 #handle the max entries error and pass 163 to line 167
        url_count = 0
        weighted_score = 0
        stored_keyword = []
        ddos = 1
        scores.append({'URL': url,'keywords': stored_keyword, 'score': url_count,'weighted_score': weighted_score, 'ddos': ddos})
        pass
    endtime = time.time()
    print('process took = ', endtime - starttime)
    q.put(scores)

def output_csv(file_path, scores):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['URL', 'score', 'weighted_score', 'ddos'])
        for score in scores:
            writer.writerow([score[0]['URL'],score[0]['score'], score[0]['weighted_score'], score[0]['ddos']])

def remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

def multi_process(process_scores,keywords_list, weights, urls):
    starttime = time.time()
    processes = []
    scores = []
    score = []
    for url in urls:
        q = multiprocessing.Queue()
        p1 =multiprocessing.Process(target=process_scores, args=(keywords_list, weights, url,q))
        processes.append(p1)
        p1.start()
        scores = q.get()
        p1.join()
        score.append(scores)    
        
    endtime = time.time()
    print('Main Process Complete - Total time taken = ', endtime - starttime)
    return score

def main():
    keywords_weights = get_keywords('/Users/archana/learn-code/git-what/example/keywords.csv')
    # print('keywords_weights', keywords_weights)
    urls = get_urls('/Users/archana/learn-code/git-what/example/company_urls_orig.csv')
    # print('urls', urls)
    scores = multi_process(process_scores, keywords_weights[0], keywords_weights[1], urls)
    # scores = process_scores(keywords_weights[0], keywords_weights[1], urls)
    print('scores', scores)
    output_csv('/Users/archana/learn-code/git-what/example/scores.csv', scores)

if __name__ == "__main__":
    main()