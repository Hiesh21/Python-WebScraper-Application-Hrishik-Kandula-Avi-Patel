import bs4 as bs
import urllib.request
import re
import nltk
import heapq
import smtplib


#Links that we used to help us get an introduction
#https://stackabuse.com/text-summarization-with-nltk-in-python/
#https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
#summary variable
summary = ""

"""clean up double spaces and brackets for sentence tokinization"""
def getText(preformatted_text):
    preformatted_text = re.sub(r'\[[0-9]*\]', ' ', preformatted_text)
    return re.sub(r'\s+', ' ', preformatted_text)
"""format further to remove punctuation for word tokinization"""
def RemovePunctuation(prev_formatted_text):
    formarticle = re.sub('[^a-zA-Z]', ' ', prev_formatted_text)
    return re.sub(r'\s+', ' ', formarticle)
"""calculate word frequency"""
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
"""calculate weighted frequency"""
def calcWeightedFreq(freq):
    maximum_frequncy = max(freq.values())
    for word in freq.keys():
        freq[word] = (freq[word]/maximum_frequncy)
        return freq
"""Calculated the weighed sentence scores"""
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
"""the shared code that prints the summaries using NLTK"""
def printSummary(preformatted_text):
    article_text = getText(preformatted_text)
    formatted_article_text = RemovePunctuation(article_text)
    sentence_list = nltk.sent_tokenize(article_text)
    word_frequencies = calcWordFreq(formatted_article_text)
    word_frequencies = calcWeightedFreq(word_frequencies)
    sentence_scores = calcSentScores(word_frequencies, sentence_list)
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary
    
"""summarizer for websites--also extracts the raw text from the line of html where it is located"""
def webSummary():
    print("Enter the desired url of the website you would like to summarize: ")
    website = input("Website URL: ")
    scraped_data = urllib.request.urlopen(website)
    article = scraped_data.read()
    soup = bs.BeautifulSoup(article,'lxml')
    paragraphs = soup.find_all('p')
    preformatted_text = ""
    for p in paragraphs:
        preformatted_text += p.text
    return printSummary(preformatted_text)
    
"""summarizer for raw text"""
def rawtextSummary():
    print("Enter the enter the text you would like to summarize: ")
    text = input("Text: ")
    printSummary(text)
    return printSummary(text)


"""sends emails"""
def sendEmail(text):
    gmail_user = 'summarizerpatel@gmail.com'
    gmail_password = 'ap57754dp'

    sent_from = gmail_user
    to = ['summarizerpatel@gmail.com']
    subject = 'Summarized Text'
    body = text

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')





#IO Stream that serves as the runner of the entire program

print("Welcome to Text Summarizer. We will output the summarized text in the command line and in email")




print("Would you like to summarize text from a website or from your own raw text(Enter Website or Raw Text)")
choice = input("Enter your choice: ")
if choice == "Website":
    print("Here is your summary:\n" + "_____________________________________________________\n" + webSummary())
    sendEmail(webSummary())
    



elif choice == "Raw Text":
    print("Here is your summary:\n" + "_____________________________________________________\n" + rawtextSummary())
else:
    print("Option not valid. Have a good day:)")



