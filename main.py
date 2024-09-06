import requests
from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import openai
import creds
from gtts import gTTS
import os
from datetime import datetime, timedelta
from sendmail import sendmail

current_date = datetime.now()
formatted_date = current_date.strftime('%Y-%m-%d')
previous_day = current_date - timedelta(days=1)
formatted_previous_date = previous_day.strftime('%Y-%m-%d')

open('summaries.txt', 'w').close()

api = NewsApiClient(api_key=creds.news_key)

client = openai.OpenAI(api_key=creds.openai_key, organization=creds.openai_org)

summaries = ''


def extractText(art):
    url = art["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_title = art["title"]
    article_text = soup.get_text()
    article_text = os.linesep.join([s for s in article_text.splitlines() if s])

    return article_title + '\n' + article_text


def summarize(text):
    prompt = [
    {"role": "system", "content": """
        You are an enthusiastic news reporter creating a script for your broadcast. 
        You will be given an article, which you must summarize in an entertaining yet objective manner.
        There will be other information in the block of text given to you, but you must dismiss everything except for what is part of the article.
        This summary should be about 50% of the length of the entire article, although you may deviate from this if you feel certain pieces of information are important or not.
        Additionally, some of the articles will not grant access. If you see an error message in the text, simply return the text "fail" and nothing else.
                                  """},
    {"role": "user", "content": f"Create a summary for this article: {text}. You must include the title, found in the first line of the text."}
  ]
    response = client.chat.completions.create(model='gpt-3.5-turbo-0125', messages=prompt)
    response = response.choices[0].message.content
    return response


def tts(smr):
    with open("summaries.txt") as f:
        lines = [line.rstrip() for line in f]

    result = " ".join(lines)


    os.system(
        f'tts --text "{result}" --model_name tts_models/en/vctk/vits --out_path '{PATH}/NOOZ/{formatted_date}-news.mp3 --speaker_idx "p317"')


articles = api.get_everything(q='artificial intelligence', from_param=formatted_previous_date)
print(articles)

i = 0
while i < 5:
    summary = summarize(extractText(articles["articles"][i]))
    if summary.lower() != 'fail':
        summaries = summaries + summary + '\n\n'
        i += 1

f = open('summaries.txt', 'a')
f.write(summaries.replace('"', ''))
f.close()

tts(summaries)

sendmail("{EMAIL}", formatted_date)
