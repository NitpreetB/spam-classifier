import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
mnb=MultinomialNB()
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score
import pickle
from sklearn.preprocessing import LabelEncoder

ps = PorterStemmer()
tfidf = TfidfVectorizer(max_features=3000)

def main():
    try:
        datafile = pd.read_csv('spam.csv', encoding='latin1', error_bad_lines=False)
        data_cleaning(datafile)
        eda(datafile)
        
        datafile['transformed_text'] = datafile['text'].apply(data_preprocessing) 
        print(datafile.head())
        TextProcessing(datafile)
        modelBuilding(datafile)

        pickle.dump(tfidf, open('vectorizer.pkl', 'wb'))
        pickle.dump(mnb, open('model.pkl', 'wb'))
    
    except pd.errors.ParserError as e:
        print(f"ParserError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def data_cleaning(datafile):
    # Drop unnecessary columns
    datafile.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace=True)
    # Rename columns
    datafile.rename(columns={'v1': 'target', 'v2': 'text'}, inplace=True)
    # Encode target labels
    encoder = LabelEncoder()
    datafile['target'] = encoder.fit_transform(datafile['target'])
    # Check for missing values
    print(datafile.isnull().sum())
    # Check for duplicates and drop them
    print(datafile.duplicated().sum())
    datafile.drop_duplicates(keep='first', inplace=True)

def eda(datafile):
    ## EDA - Exploratory Data Analysis
    print(datafile['target'].value_counts())
    
    # Save pie chart of data distribution
    plt.pie(datafile['target'].value_counts(), labels=['not_spam', 'spam'], autopct="%0.2f")
    plt.title('Distribution of Spam vs. Not Spam')
    plt.savefig('Exploratory_Data_Analysis/pie_chart.png')
    plt.clf()  # Clear the current figure
    
    # Feature engineering: adding new columns
    datafile['num_characters'] = datafile['text'].apply(len)
    datafile['num_words'] = datafile['text'].apply(lambda x: len(nltk.word_tokenize(x)))
    datafile['num_sentences'] = datafile['text'].apply(lambda x: len(nltk.sent_tokenize(x)))
    
    # Display summary statistics
    print(datafile[['num_characters', 'num_words', 'num_sentences']].describe())
    print(datafile[datafile['target'] == 0][['num_characters', 'num_words', 'num_sentences']].describe())
    print(datafile[datafile['target'] == 1][['num_characters', 'num_words', 'num_sentences']].describe())

    # Create and save histogram for both non-spam and spam messages - characters
    plt.hist(datafile[datafile['target'] == 0]['num_characters'], bins=20, edgecolor='black', alpha=1, label='Non-Spam')
    plt.hist(datafile[datafile['target'] == 1]['num_characters'], bins=20, edgecolor='black', alpha=1, label='Spam')
    plt.title('Histogram of Number of Characters in Messages')
    plt.xlabel('Number of Characters')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.savefig('Exploratory_Data_Analysis/characters_histogram.png')
    plt.clf()  # Clear the current figure
    
    # Create and save histogram for both non-spam and spam messages - words 
    plt.hist(datafile[datafile['target'] == 0]['num_words'], bins=20, edgecolor='black', alpha=1, label='Non-Spam')
    plt.hist(datafile[datafile['target'] == 1]['num_words'], bins=20, edgecolor='black', alpha=1, label='Spam')
    plt.title('Histogram of Number of Words in Messages')
    plt.xlabel('Number of words')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.savefig('Exploratory_Data_Analysis/words_histogram.png')
    plt.clf()  # Clear the current figure
    
    sns.pairplot(datafile,hue='target')
    plt.savefig('Exploratory_Data_Analysis/pairplots.png')
    plt.clf()  # Clear the current figure

    # See correlation 
    sns.heatmap(datafile.corr(),annot=True)
    plt.savefig('Exploratory_Data_Analysis/correlation_heatmap.png')
    plt.clf()  # Clear the current figure

def data_preprocessing(text):
    ## Lowercase 
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

def TextProcessing(datafile):
    
    spam_corpus = []
    for msg in datafile[datafile["target"]==1]['transformed_text'].tolist():
        for word in msg.split():
            spam_corpus.append(word)
    
    sns.barplot(pd.DataFrame(Counter(spam_corpus).most_common(30))[0], pd.DataFrame(Counter(spam_corpus).most_common(30))[1])
    plt.xticks(rotation='vertical')
    plt.savefig('Exploratory_Data_Analysis/most_common_spam_words.png')
    plt.clf()  # Clear the current figure

    nspam_corpus = []
    for msg in datafile[datafile["target"]==0]['transformed_text'].tolist():
        for word in msg.split():
            nspam_corpus.append(word)
    
    sns.barplot(pd.DataFrame(Counter(nspam_corpus).most_common(30))[0], pd.DataFrame(Counter(nspam_corpus).most_common(30))[1])
    plt.xticks(rotation='vertical')
    plt.savefig('Exploratory_Data_Analysis/most_common_NON_spam_words.png')
    plt.clf()  # Clear the current figure

def modelBuilding(datafile):
    ## Naive Bayes models
    ## Vectorize the transformed text 
    X = tfidf.fit_transform(datafile['transformed_text']).toarray()

    Y = datafile['target'].values

    ## Split train and test data 
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

    mnb.fit(X_train, Y_train)
    Y_pred2 = mnb.predict(X_test)
    print(accuracy_score(Y_test, Y_pred2))
    print(confusion_matrix(Y_test, Y_pred2))
    print(precision_score(Y_test, Y_pred2))

if __name__ == "__main__":
    main()
