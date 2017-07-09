Dataset used: http://mklab.iti.gr/project/web-news-article-dataset

Order of execution:

1) Pass dataset to function document_word_frequency which will create a csv file with all the words and their respective inverse document frequency.

2) Now that you have the file, it should be just either calling it through the console, since it has argparse ready, or just shooting up summarize with the respective arguments(don't forget article_obj needs to be called with article_object function), so it would typically be called as such: summarize(article_object(url), ....
