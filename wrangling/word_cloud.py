import spacy
from spacy.lang.es.stop_words import STOP_WORDS
from spacy.lang.es import Spanish
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

STOP_WORDS |= {'y' , 'rt', 'hola', 'gracia', 'gracias', 'q'}

parser = Spanish()


def spacy_tokenizer(sentence):
    tokens = parser(sentence)

    filtered_tokens = []
    for word in tokens:
        lemma = word.lemma_.lower().strip()

        if lemma not in STOP_WORDS and re.search('^[a-zA-Z]+$' , lemma):
            filtered_tokens.append(lemma)

    return filtered_tokens


def generate_wordcloud(all_words):
    # twitter_mask = np.array(Image.open('/home/carpiero/Google_Drive/IRONHACK/Twitter-Logo.png'))
    wordcloud = WordCloud(random_state=21 , max_font_size=90 , max_words=100 ,height = 300,width = 450, prefer_horizontal=0.99,min_word_length=2,
                          relative_scaling=0.4 , colormap='Spectral',background_color='#192229').generate(all_words)
    #width = 800 , height = 100
    return wordcloud.to_image()





    #     plt.imshow(wordcloud, interpolation='bilinear')
    #     plt.axis("off")
    #     plt.figure()
    #     plt.imshow(twitter_mask, cmap=plt.cm.gray, interpolation='bilinear')
    #     plt.axis("off")
    #     plt.show()

    # plt.figure(figsize=(14 , 10))
    # plt.imshow(wordcloud , interpolation="bilinear")
    # plt.axis('off')
    # plt.savefig(f'../Data/Wordcloud_{star}.pdf' ,
    #             transparent=False ,
    #             dpi=80 ,
    #             bbox_inches="tight")


