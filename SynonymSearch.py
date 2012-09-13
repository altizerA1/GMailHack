from nltk.corpus import wordnet as wn
import imaplib, getpass
import sys
import time

def getSynonyms(word):
  vec = []
  for synset in wn.synsets(word):
    for l in synset.lemmas:
      vec.append(l.name)
  return vec

def Search(mail, word):
  clock_start = time.time()
  vec = getSynonyms(word)
  if word not in vec: vec.append(word)
  
  dict = {}
  numExceptions = 0
  for w in vec:
    s = '(HEADER Subject "' + w + '")'
    data = []
    try:
      result, data = mail.uid('search', None, s)
    except:
      numExceptions += 1
      
    for uidstr in data:
      for uid in uidstr.split():
        if uid not in dict: dict[uid] = 0
        dict[uid] += 1
  #print 'NumExceptions:' + str(numExceptions)
  sortedvec = sorted(dict.items(), key=lambda t: -t[1])

  if len(sortedvec) == 0:
    print 'No Search Results'
    sys.stdout.flush()
    sys.stdout.flush()
  else:
    for uid, count in sortedvec:
      result, data = mail.uid('fetch', uid, '(RFC822)')
      raw_email = data[0][1]
      print 'EmailUID:',uid, 'Count:',count
      print raw_email
      print ''

  print 'Synonym Search:' + word, 'returned', len(sortedvec), 'results and took ', time.time() - clock_start, 'seconds'

def main():
  mail = imaplib.IMAP4_SSL('imap.gmail.com')
  print 'Enter GMail UserName:'
  username = raw_input()
  mail.login(username, getpass.getpass())
  mail.select('inbox')
  
  while(True):
    print 'Enter Search Query:'
    word = raw_input()
    if word == '' or len(word) == 0:
      print 'ERROR: invalid search string'
      sys.stdout.flush()
      continue
    Search(mail, word)  
    
if __name__ == '__main__':
  main()
