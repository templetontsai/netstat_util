import pandas as pd
import json
from urllib.request import urlopen
import urllib.request
import urllib.parse
import ssl


def dotCom(domain):
    return domain + '.com'


def digCMD(label):
    sslContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    response = urlopen('https://122.148.156.195:8080/dig/' +
                       label, context=sslContext)
    return json.load(response)

df = pd.read_csv('../notebook/playground/INVESTMENTS.csv')
df = df[:5]


df['domainName'] = df['domain'].apply(dotCom)

df['ip'] = df['domainName'].apply(digCMD)
print(df.head(5))
