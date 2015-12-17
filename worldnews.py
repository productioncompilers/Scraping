import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import os
import httplib2
from multiprocessing import Pool
c=0
import requests
from datetime import datetime
import multiprocessing
from multiprocessing import current_process
import time
import os
import sys
FORMAT = '%d-%m-%Y %H:%M:%S'
def make_soup(s):
   match=re.compile('https://|http://|www.|.com|.in|.org|gov.in')
   if re.search(match,s):
    while(True):
     try:
      http = httplib2.Http()
      break
     except:
         continue
    while(True):
     try:
      status, response = http.request(s)
      break
     except:
         continue
    while(True):
     try:
      page = BeautifulSoup(response,"html.parser",parse_only=SoupStrainer('div'))
      break
     except:
         continue
    return page
   else:
     return None
def test_internet():
   while(True):
      try:
         http = httplib2.Http()
         status, response = http.request("https://www.google.com")
         break
      except:
            continue
def parse1(s):
   global c
   temp_set=set()
   soup=make_soup(s)
   if(soup!=None):
      for div in soup.find_all('div',class_=[ "thing" , "id-t3_3ua12m" ,"linkflair" , "linkflair-normal" , "odd" ,  "link"]):
       try:
         if(div.p!=None and div.p.next_sibling!=None and div.p.next_sibling.next_sibling!=None):
          x=div.p.next_sibling.next_sibling.next_sibling['class']
          if(x[0]=='entry'):
            element='\nPROMPT '+str(c+1)+'\n'
            if(div.p.next_sibling.next_sibling.next_sibling!=None and div.p.next_sibling.next_sibling.next_sibling.p!=None and div.p.next_sibling.next_sibling.next_sibling.p.a!=None):
               element=element+div.p.next_sibling.next_sibling.next_sibling.p.a.string+'\n'
               element=element+div.p.next_sibling.next_sibling.next_sibling.p.a['href']+'\n'
            if(div.p.next_sibling.next_sibling.next_sibling.find('p',{'class':'tagline'})!=None and div.p.next_sibling.next_sibling.next_sibling.find('p',{'class':'tagline'}).time!=None):
                  element=element+div.p.next_sibling.next_sibling.next_sibling.find('p',{'class':'tagline'}).time['datetime']+'\t'
                  element=element+div.p.next_sibling.next_sibling.next_sibling.find('p',{'class':'tagline'}).time['title']+'\t'
                  element=element+div.p.next_sibling.next_sibling.next_sibling.find('p',{'class':'tagline'}).time.string+'\n'
            if(div.p.next_sibling.next_sibling.next_sibling.find('p',{'class':'tagline'})!=None and div.p.next_sibling.next_sibling.next_sibling.find('p',{'class':'tagline'}).a!=None):
               element=element+div.p.next_sibling.next_sibling.next_sibling.find('p',{'class':'tagline'}).a.string+'\n'
               element=element+div.p.next_sibling.next_sibling.next_sibling.find('p',{'class':'tagline'}).text+'\n'
            if(div.div.find('div',{'class':'score likes'})!=None):
               element=element+'score likes '+div.div.find('div',{'class':'score likes'}).string+'\t'
               element=element+'score dislikes '+div.div.find('div',{'class':'score dislikes'}).string+'\t'
               element=element+'score unvoted '+div.div.find('div',{'class':'score unvoted'}).string+'\n\n'
            f.write(element)
            c=c+1
          elif(x[0]=='thumbnail'):
            element='\nPROMPT '+str(c+1)+'\n'
            if(div.find('div',{'class':'entry unvoted'})!=None and div.find('div',{'class':'entry unvoted'}).p!=None and div.find('div',{'class':'entry unvoted'}).p.a!=None and div.find('div',{'class':'entry unvoted'}).p.a.string!=None):
               element=element+div.find('div',{'class':'entry unvoted'}).p.a.string+'\n'
               element=element+div.find('div',{'class':'entry unvoted'}).p.a['href']+'\n'
               if(div.find('div',{'class':'entry unvoted'}).find('p',{'class':'tagline'})!=None and div.find('div',{'class':'entry unvoted'}).find('p',{'class':'tagline'}).time != None):
                  element=element+div.find('div',{'class':'entry unvoted'}).find('p',{'class':'tagline'}).time['datetime']+'\t'
                  element=element+div.find('div',{'class':'entry unvoted'}).find('p',{'class':'tagline'}).time['title']+'\t'
                  element=element+div.find('div',{'class':'entry unvoted'}).find('p',{'class':'tagline'}).time.string+'\n'
               if(div.find('div',{'class':'entry unvoted'}).find('p',{'class':'tagline'}).a!=None):
                  element=element+div.find('div',{'class':'entry unvoted'}).find('p',{'class':'tagline'}).a.string+'\n'
                  element=element+div.find('div',{'class':'entry unvoted'}).find('p',{'class':'tagline'}).text+'\n'
               if(div.p.next_sibling.next_sibling.find('div',{'class':'score likes'})!=None and div.p.next_sibling.next_sibling.find('div',{'class':'score dislikes'})!=None and div.p.next_sibling.next_sibling.find('div',{'class':'score unvoted'})!=None):
                  element=element+'score likes '+div.p.next_sibling.next_sibling.find('div',{'class':'score likes'}).string+'\t\t'
                  element=element+'score dislikes '+div.p.next_sibling.next_sibling.find('div',{'class':'score dislikes'}).string+'\t\t'
                  element=element+'score unvoted '+div.p.next_sibling.next_sibling.find('div',{'class':'score unvoted'}).string+'\n'
            f.write(element)
            c=c+1
       except:
            continue
def count_next_of_current(s,m):
    soup=make_soup(s)
    y='https://www.reddit.com/r/'+m+'/'+select_tab+'/?count='
    match=re.compile(y)
    for link in soup.find_all('a',{'rel':['next']}):
        href=link['href']
        return href

def read_reddit_images(change_file_number,m,x):
    global f
    global select_tab
    select_tab=x
    x=m+'_'+select_tab+'.txt'
    #test_internet()
    s='https://www.reddit.com/r/'+m+'/'+select_tab
    soup=make_soup(s)
    f=open(x,'a',encoding='utf-8')
    f.write('\n\n\n\niteration number '+str(change_file_number)+' '+datetime.now().strftime(FORMAT)+'\n\n')
    maximum_number_of_next_pages=7
    parse1(s)
    count=0
    print('for '+m+' '+select_tab+' current page number is'+'\n'+str(count))
    while(count<maximum_number_of_next_pages):
        s=count_next_of_current(s,m)
        if(s!=None):
            parse1(s)
            count=count+1
            print(count)
        else:
            break
    f.write('\n\niteration number '+str(change_file_number)+' '+datetime.now().strftime(FORMAT)+'\n\n')
    f.close()
def main(m,i):
   read_reddit_images(i,m,'new')
   read_reddit_images(i,m,'hot')
   read_reddit_images(i,m,'top')
   read_reddit_images(i,m,'rising')
   read_reddit_images(i,m,'controversial')
   read_reddit_images(i,m,'gilded')
   
   
if __name__ == "__main__":
    processes = []
    arguments = sys.argv[2:]#it was b
    for x in arguments:
        print(x)
        p = multiprocessing.Process(target=main, args=(str(x),int(sys.argv[1]), ))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    my.close()
