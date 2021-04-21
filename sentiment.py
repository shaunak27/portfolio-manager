from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from transformers import logging
from operator import itemgetter
from statistics import mode

def get_sentiment(arg):
    d = {0:'Positive', 1: 'Negative', 2: 'Neutral'}
    logging.set_verbosity_error()  
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to('cpu')

    inputs = tokenizer(arg, return_tensors="pt",truncation=True,padding=True)
    inputs = inputs.to('cpu')
    ones = [1]*len(arg)
    labels = torch.tensor(ones).unsqueeze(0).to('cpu')  # Batch size 
    outputs = model(**inputs, labels=labels)
    ret_list = []
    sentiment_list = []
    for o in outputs.logits:
        sentiment_list  += [d[max(enumerate(o.tolist()), key=itemgetter(1))[0]]]
    sentiment = max(set(sentiment_list), key = sentiment_list.count)
    if sentiment == "Positive":
        buy = "Highly Recommended"
    elif sentiment == "Negative":
        buy = "Not Recommended"
    else :
        buy = "Moderately Recommended"
    ret_list = [sentiment,buy]
    return ret_list
