import bs4 as bs
import urllib.request
import re
import nltk
import heapq


#https://stackabuse.com/text-summarization-with-nltk-in-python/
'''clean up double spaces and brackets for sentence tokinization'''
def getText(preformatted_text):
    preformatted_text = re.sub(r'\[[0-9]*\]', ' ', preformatted_text)
    return re.sub(r'\s+', ' ', preformatted_text)
'''format further to remove punctuation for word tokinization'''
def RemovePunctuation(prev_formatted_text):
    formarticle = re.sub('[^a-zA-Z]', ' ', prev_formatted_text)
    return re.sub(r'\s+', ' ', formarticle)
'''calculate word frequency'''
def calcWordFreq(formatted_article_text):
    stopwords = nltk.corpus.stopwords.words('english')
    freq = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in freq.keys():
                freq[word] = 1
            else:
                freq[word] += 1
    return freq
'''calculate weighted frequency'''
def calcWeightedFreq(freq):
    maximum_frequncy = max(freq.values())
    for word in freq.keys():
        freq[word] = (freq[word]/maximum_frequncy)
        return freq
def calcSentScores(freq, sentlist):
    sentscores = {}
    for sent in sentlist:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freq.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentscores.keys():
                        sentscores[sent] = freq[word]
                    else:
                        sentscores[sent] += freq[word]
    return sentscores
'''the shared code that prints the summaries using NLTK'''
def printSummary(preformatted_text):
    
    article_text = getText(preformatted_text)
    formatted_article_text = RemovePunctuation(article_text)
    sentence_list = nltk.sent_tokenize(article_text)
    word_frequencies = calcWordFreq(formatted_article_text)
    word_frequencies = calcWeightedFreq(word_frequencies)
    sentence_scores = calcSentScores(word_frequencies, sentence_list)
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    print("Here is your summary:\n" + "_____________________________________________________\n" + summary)
'''summarizer for websites--also extracts the raw text from the line of html where it is located'''
def webSummary():
    print("Enter the desired url of the website you would like to summarize: ")
    website = input()
    scraped_data = urllib.request.urlopen(website)
    article = scraped_data.read()
    soup = bs.BeautifulSoup(article,'lxml')
    paragraphs = soup.find_all('p')
    preformatted_text = ""
    for p in paragraphs:
        preformatted_text += p.text
    printSummary(preformatted_text)
'''summarizer for raw text'''
def rawtextSummary():
    print("Enter the enter the text you would like to summarize: ")
    text = input()
    printSummary(text)

#IO Stream that serves as the runner of the entire program
print("Would you like to summarize text from a website or from your own raw text(Enter Website or Raw Text)")
choice = input()
if choice == "Website":
    webSummary()
elif choice == "Raw Text":
    rawtextSummary()
else:
    print("Option not valid. Have a good day:)")


