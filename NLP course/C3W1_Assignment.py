#!/usr/bin/env python
# coding: utf-8

# # Week 1: Explore the BBC News archive
# 
# Welcome! In this assignment you will be working with a variation of the [BBC News Classification Dataset](https://www.kaggle.com/c/learn-ai-bbc/overview), which contains 2225 examples of news articles with their respective categories (labels).
# 
# Let's get started!

# In[1]:


import csv
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# Begin by looking at the structure of the csv that contains the data:

# In[2]:


with open("./bbc-text.csv", 'r') as csvfile:
    print(f"First line (header) looks like this:\n\n{csvfile.readline()}")
    print(f"Each data point looks like this:\n\n{csvfile.readline()}")     


# As you can see, each data point is composed of the category of the news article followed by a comma and then the actual text of the article.

# ## Removing Stopwords
# 
# One important step when working with text data is to remove the **stopwords** from it. These are the most common words in the language and they rarely provide useful information for the classification process.
# 
# Complete the `remove_stopwords` below. This function should receive a string and return another string that excludes all of the stopwords provided.

# In[3]:


# GRADED FUNCTION: remove_stopwords
def remove_stopwords(sentence):
    """
    Removes a list of stopwords
    
    Args:
        sentence (string): sentence to remove the stopwords from
    
    Returns:
        sentence (string): lowercase sentence without the stopwords
    """
    # List of stopwords
    stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]
    
    # Sentence converted to lowercase-only
    sentence = sentence.lower()
    tokenizer = Tokenizer(oov_token = "<oov>")
    tokenizer.fit_on_texts(sentence)
    word_index = tokenizer.word_index
    sequence = tokenizer.texts_to_sequences(sentence)
    print(word_index)
    #print(sequence)
    print(len(word_index))
    print(word_index)
    for word in stopwords:
        token = " "+ word + " "
        sentence = sentence.replace(token , " ")
    ### END CODE HERE
    return sentence


# In[4]:


# Test your function
remove_stopwords(" I am about to go to the store and get any snack")


# ***Expected Output:***
# ```
# 'go store get snack'
# 
# ```

# ## Reading the raw data
# 
# Now you need to read the data from the csv file. To do so, complete the `parse_data_from_file` function.
# 
# A couple of things to note:
# - You should omit the first line as it contains the headers and not data points.
# - There is no need to save the data points as numpy arrays, regular lists is fine.
# - To read from csv files use [`csv.reader`](https://docs.python.org/3/library/csv.html#csv.reader) by passing the appropriate arguments.
# - `csv.reader` returns an iterable that returns each row in every iteration. So the label can be accessed via row[0] and the text via row[1].
# - Use the `remove_stopwords` function in each sentence.

# In[33]:


# GRADED FUNCTION: parse_data_from_file
import json
def parse_data_from_file(filename):
    """
    Extracts sentences and labels from a CSV file
    
    Args:
        filename (string): path to the CSV file
    
    Returns:
        sentences, labels (list of string, list of string): tuple containing lists of sentences and labels
    """
    sentences = []
    labels = []
    with open(filename, 'r') as csvfile:
        ### START CODE HERE
        reader = csv.reader(csvfile, delimiter=',')
        
        next(reader, None)
        
        for item in reader:
            sentences.append(item[1])
            labels.append(item[0])

        ### END CODE HERE

    return sentences, labels


# In[34]:


# Test your function
sentences, labels = parse_data_from_file("./bbc-text.csv")

print(f"There are {len(sentences)} sentences in the dataset.\n")
print(f"First sentence has {len(sentences[0].split())} words (after removing stopwords).\n")
print(f"There are {len(labels)} labels in the dataset.\n")
print(f"The first 5 labels are {labels[:5]}")


# ***Expected Output:***
# ```
# There are 2225 sentences in the dataset.
# 
# First sentence has 436 words (after removing stopwords).
# 
# There are 2225 labels in the dataset.
# 
# The first 5 labels are ['tech', 'business', 'sport', 'sport', 'entertainment']
# 
# ```

# ## Using the Tokenizer
# 
# Now it is time to tokenize the sentences of the dataset. 
# 
# Complete the `fit_tokenizer` below. 
# 
# This function should receive the list of sentences as input and return a [Tokenizer](https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/text/Tokenizer) that has been fitted to those sentences. You should also define the "Out of Vocabulary" token as `<OOV>`.

# In[35]:


# GRADED FUNCTION: fit_tokenizer
def fit_tokenizer(sentences):
    """
    Instantiates the Tokenizer class
    
    Args:
        sentences (list): lower-cased sentences without stopwords
    
    Returns:
        tokenizer (object): an instance of the Tokenizer class containing the word-index dictionary
    """
    ### START CODE HERE
    # Instantiate the Tokenizer class by passing in the oov_token argument
    tokenizer = Tokenizer(oov_token='<OOV>')
    tokenizer.fit_on_texts(sentences)
    word_index = tokenizer.word_index
    # Fit on the sentences
    ### END CODE HERE
    return tokenizer


# In[36]:


tokenizer = fit_tokenizer(sentences)
word_index = tokenizer.word_index

print(f"Vocabulary contains {len(word_index)} words\n")
print("<OOV> token included in vocabulary" if "<OOV>" in word_index else "<OOV> token NOT included in vocabulary")


# ***Expected Output:***
# ```
# Vocabulary contains 29714 words
# 
# <OOV> token included in vocabulary
# 
# ```

# In[37]:


# GRADED FUNCTION: get_padded_sequences
def get_padded_sequences(tokenizer, sentences):
    """
    Generates an array of token sequences and pads them to the same length
    
    Args:
        tokenizer (object): Tokenizer instance containing the word-index dictionary
        sentences (list of string): list of sentences to tokenize and pad
    
    Returns:
        padded_sequences (array of int): tokenized sentences padded to the same length
    """
    
    ### START CODE HERE
    # Convert sentences to sequences
    sequences = tokenizer.texts_to_sequences(sentences)
    
    # Pad the sequences using the post padding strategy
    padded = pad_sequences(sequences, padding='post')
    
    ### END CODE HERE
    
    return padded


# In[38]:


padded_sequences = get_padded_sequences(tokenizer, sentences)
print(f"First padded sequence looks like this: \n\n{padded_sequences[0]}\n")
print(f"Numpy array of all sequences has shape: {padded_sequences.shape}\n")
print(f"This means there are {padded_sequences.shape[0]} sequences in total and each one has a size of {padded_sequences.shape[1]}")


# ***Expected Output:***
# ```
# First padded sequence looks like this: 
# 
# [  96  176 1157 ...    0    0    0]
# 
# Numpy array of all sequences has shape: (2225, 2438)
# 
# This means there are 2225 sequences in total and each one has a size of 2438
# 
# ```

# In[39]:


# GRADED FUNCTION: tokenize_labels
def tokenize_labels(labels):
    """
    Tokenizes the labels
    
    Args:
        labels (list of string): labels to tokenize
    
    Returns:
        label_sequences, label_word_index (list of string, dictionary): tokenized labels and the word-index
    """
    ### START CODE HERE
    
    # Instantiate the Tokenizer class
    # No need to pass additional arguments since you will be tokenizing the labels
    
    label_tokenizer = Tokenizer()

    # Fit the tokenizer to the labels
    label_tokenizer.fit_on_texts(labels)
    label_word_index = label_tokenizer.word_index
    label_seq = label_tokenizer.texts_to_sequences(labels)
    
    ### END CODE HERE
    
    return label_seq, label_word_index


# In[32]:


label_sequences, label_word_index = tokenize_labels(labels)
print(f"Vocabulary of labels looks like this {label_word_index}\n")
print(f"First ten sequences {label_sequences[:10]}\n")


# ***Expected Output:***
# ```
# Vocabulary of labels looks like this {'sport': 1, 'business': 2, 'politics': 3, 'tech': 4, 'entertainment': 5}
# 
# First ten sequences [[4], [2], [1], [1], [5], [3], [3], [1], [1], [5]]
# 
# ```

# **Congratulations on finishing this week's assignment!**
# 
# You have successfully implemented functions to process various text data processing ranging from pre-processing, reading from raw files and tokenizing text.
# 
# **Keep it up!**
