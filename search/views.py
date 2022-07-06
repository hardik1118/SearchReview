from django.shortcuts import render, HttpResponse
from .models import review, posting_list
import re
import string
# import Stemmer

# Create your views here.
def load():
    with open('C:\\Users\\HP\\Desktop\\New folder\\SearchReview\\search\\static\\test.txt') as f:
        res = f.readlines()
        i = 0
        while i < len(res):
            if res[i].startswith('product/productId: '):
                pId = res[i].split(':')[1].replace('\n', '').strip()
                i += 1
                uId = res[i].split(':')[1].replace('\n', '').strip()
                i += 1
                pName = res[i].split(':')[1].replace('\n', '').strip()
                i += 1
                help = res[i].split(':')[1].replace('\n', '').strip()
                i += 1
                score = res[i].split(':')[1].replace('\n', '').strip()
                i += 1
                time = res[i].split(':')[1].replace('\n', '').strip()
                i += 1
                summary = res[i].split(':')[1].replace('\n', '').strip()
                i += 1
                text = res[i].split(':')[1].replace('\n', '').strip()
                i += 1

                # store review in database
                score = eval(score)
                try:
                    help = eval(help)
                except:
                    help = 0

                obj = review(prodId=pId, userId=uId, profName=pName, help=help, score=score, time=time, summary=summary, text=text)
                obj.save()
            i+=1


STOPWORDS = {'a','about','all','also','and','as','at','be','because','but','by','can','come','could','day','do','even','find','first','for','from','get','give','go','have','he','her','here','him','his','how','i','if','in','into','it','its','just','know','like','look','make','man','many','me','more','my','new','no','not','now','of','on','one','only','or','other','our','out','people','say','see','she','so','some','take','tell','than','that','the','their','them','then','there','these','they','thing','think','this','those','time','to','two','up','use','very','want','way','we','well','what','when','which','who','will','with','would','year','you','your'}

PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

def tokenize(text):
    return text.split()

def lowercase_filter(tokens):
    return [token.lower() for token in tokens]

def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]

def stopword_filter(tokens):
    return [token for token in tokens if token not in STOPWORDS]

# def stem_filter(tokens):
#     return STEMMER.stemWords(tokens)

def analyze(text):
    tokens = tokenize(text)
    tokens = lowercase_filter(tokens)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    # tokens = stem_filter(tokens)

    return [token for token in tokens if token]


def index_words():
    obj = review.objects.all()
    for rv in obj:
        text = rv.summary + rv.text
        text = analyze(text)
        for i in text:
            pl = posting_list.objects.filter(token=i)
            if pl:
                pl = pl[0]
                pl.docs = pl.docs + f'{rv.id},'
            else:
                pl = posting_list(token=i, docs=f'{rv.id},')
            pl.save()


def index(request):
    # below two functions are to be run only first time
    # load()
    # index_words()
    context = {'result':[]}
    if request.method == 'POST':
        try:
            text = request.POST.get('search')
            text = analyze(text)

            # intersection
            res = []
            l = ''
            for i in text:
                pl = posting_list.objects.filter(token=i)
                if pl:
                    pl = pl[0]
                    l += pl.docs
                    res.append((pl.docs).split(','))
                    res[-1].pop()
            res = [set(map(int,i)) for i in res]
            res = set.intersection(*res)

            # union
            l = l.split(',')
            l.pop()
            l = set(map(int,l))
            l.difference_update(res)

            result_set = []
            for i in res:
                result_set.append(review.objects.get(id=i))
            temp = []
            for i in l:
                temp.append(review.objects.get(id=i))
            temp.sort(key=lambda x:x.score, reverse=True)
            result_set.extend(temp)
            context = {'result':result_set, 'tokens':text}
        except:
            pass

    return render(request, 'index.html', context)