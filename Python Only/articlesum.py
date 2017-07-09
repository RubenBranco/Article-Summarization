#!/usr/bin/env python
# -*-coding:utf-8-*-

import newspaper
import nltk
import math
import re
import operator


def article_object(url):
    article = newspaper.Article(url)
    try:
        article.download()
        article.parse()
    except newspaper.ArticleException:
        return None
    return article


def document_word_frequency(dataset):
    """
    http://mklab.iti.gr/project/web-news-article-dataset
    N=2382
    """
    document_frequency = {}
    document_count = 0
    with open(dataset) as data_file:
        for line in data_file:
            split_line = line.split(';')
            if split_line[0] == 'URL':
                continue
            else:
                art_obj = article_object(split_line[0])
                if art_obj is None:
                    continue
                text = re.sub('[^A-Za-z -.]+', '', art_obj.text)
                text = text.replace('...', '').replace('Mr.', 'Mr').replace('Mrs.', 'Mrs').replace('.',' ')
                tokens = nltk.tokenize.word_tokenize(text)
                for word in tokens:
                    if word not in document_frequency:
                        document_frequency[word] = 1
                    else:
                        document_frequency[word] += 1
                document_count += 1
                print(document_count)
    with open('documentfrequency.csv','w') as file_writer:
        for word in document_frequency:
            file_writer.write(word + ',' + str(math.log(document_count/document_frequency[word])) + '\n')



def summarize(article_obj, size, document_frequency_file, n):
    """
    size = Number of lines to display
    """
    text = article_obj.text
    tokens = nltk.tokenize.word_tokenize(re.sub('[^A-Za-z -.]+', '', text).replace('Mr.', 'Mr').replace('Mrs.', 'Mrs').replace('.', ' '))
    term_frequency = {}
    for word in tokens:
        if word.lower() not in term_frequency:
            term_frequency[word.lower()] = 1
        else:
            term_frequency[word.lower()] += 1
    with open(document_frequency_file) as file:
        words = []
        for line in file:
            if line.split(',')[0].lower() in term_frequency:
                words.append(line.split(',')[0].lower())
                term_frequency[line.split(',')[0].lower()] = term_frequency[line.split(',')[0].lower()] * float(line.split(',')[1].strip('\n'))
        for word in term_frequency:
            if word not in words:
                term_frequency[word] = term_frequency[word] * float(math.log(n))

    sentences = re.sub('[^A-Za-z -.]+', '', text).replace('Mr.', 'Mr').replace('Mrs.', 'Mrs').strip('\n').split('.')
    sentences_dict = {i:sentences[i] for i in range(len(sentences))}
    scored_sentences = []
    for i in sentences_dict:
        token = nltk.tokenize.word_tokenize(sentences_dict[i].strip('.'))
        score = 0
        pos_tag = nltk.pos_tag(token)
        title_words = 0
        for word, pos in pos_tag:
            if pos == 'NN':
                score += term_frequency[word.lower()]
            if word in article_obj.title or word.lower() in article_obj.text:
                title_words += 1
        score /= sum(term_frequency.values())
        score += title_words / len(nltk.tokenize.word_tokenize(article_obj.text))
        score *= (i+1)/len(sentences_dict)
        scored_sentences.append((i, score))
    scored_sentences = sorted(scored_sentences, key=operator.itemgetter(1), reverse=True)
    sentences = text.replace('Mr.', 'Mr').replace('Mrs.', 'Mrs').strip('\n').split('.')
    return [sentences[scored_sentences[i][0]]+'.' for i in range(size)]

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Summarize a news article")
    parser.add_argument('url', metavar='article_obj', help='URL of the article you want to summarize')
    parser.add_argument('frequency_path', metavar='document_frequency_file', help='The path for the document frequency file')
    parser.add_argument('-s,--size', metavar='size', dest='size', nargs=1, default=4, type=int, help='Number of lines to display the summary')
    parser.add_argument('-n,--number', metavar='n', dest='number', nargs=1, default=2113, type=int, help="Size of the dataset")
    arguments = parser.parse_args()
    sentences = summarize(article_object(arguments['url']), arguments['size'], arguments['frequency_path'], arguments['number'])
    for sentence in sentences:
        print(sentence)
