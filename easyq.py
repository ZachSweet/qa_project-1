import sys, nltk, operator, csv, numpy as np
from qa_engine.base import QABase
from nltk.stem.wordnet import WordNetLemmatizer


def get_sentence():  #Eventual change: input question_id, if type= sch use scheherezade interp.
    tag_list = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBN', 'VBP', 'VBZ']
    qfile = open('data/hw6-answers.csv')
    readCSV = csv.reader(qfile, delimiter=',')
    qids = []

    for row in readCSV:
        qids.append(row[2])

    del qids[0]


    driver = QABase()
    lemmatizer = WordNetLemmatizer()

    correct = 0
    equal_scores = []

    for question_id in qids:

        q = driver.get_question(question_id)
        story = driver.get_story(q['sid'])
        text = story['text']
        question = q['text']

        text_sentences = nltk.sent_tokenize(text)
        words = [nltk.word_tokenize(x) for x in text_sentences]

        question_words = nltk.word_tokenize(question)
        question_tagged = nltk.pos_tag(question_words)

        scores = [0 for i in range(0,len(text_sentences))]

        i = 0
        for x in words:
            for y in x:
                if y not in ['was']:
                    for z in question_tagged:
                        if lemmatizer.lemmatize(y) in [lemmatizer.lemmatize(z[0])]:
                            if z[1] in tag_list:
                                scores[i] += 5
                            else:
                                scores[i] += 1
            i+=1

        skip = False
        sent_index = np.argmax(scores)
        if sent_index != len(scores) - 1:
            for i in range(sent_index + 1,len(scores)):
                if scores[i] == scores[sent_index]:
                    equal_scores.append(question_id)
                    skip = True

        if not skip:
            print(sent_index)
            print(scores)
            print('question: ' + question)
            print(text_sentences[sent_index])

            is_corr = input('correct? ')
            correct += int(is_corr)

            print('*************')


            print(correct)


if __name__ == '__main__':
