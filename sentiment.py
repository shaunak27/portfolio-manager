from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from transformers import logging
from operator import itemgetter
from statistics import mode
import numpy

def get_sentiment(arg):
    d = {0:'Positive', 1: 'Negative', 2: 'Neutral'}
    logging.set_verbosity_error()  
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to('cuda')

    inputs = tokenizer(arg, return_tensors="pt",truncation=True,padding=True)
    inputs = inputs.to('cuda')
    ones = [1]*len(arg)
    labels = torch.tensor(ones).unsqueeze(0).to('cuda')  # Batch size 
    outputs = model(**inputs, labels=labels)
    ret_list = []
    sentiment_list = []
    sentiment = []
    for o in outputs.logits:
        sentiment_list  += [d[max(enumerate(o.tolist()), key=itemgetter(1))[0]]]
    sarr = numpy.array(sentiment_list).reshape(len(sentiment_list)//5,5)
    sarr = sarr.tolist()
    for s in sarr:
        c = 0
        for si in s:
            if si == "Positive":
                c +=1
            elif si == "Negative":
                c -= 1
        if (c > 0):
            sentiment.append("Positive")
        elif (c < 0):
            sentiment.append("Negative")
        else:
            sentiment.append("Neutral")    
    for sent in sentiment:
        if sent == "Positive":
            buy = "Highly Recommended"
        elif sent == "Negative":
            buy = "Not Recommended"
        else :
            buy = "Moderately Recommended"
        ret_list.append([sent,buy])
    return ret_list
