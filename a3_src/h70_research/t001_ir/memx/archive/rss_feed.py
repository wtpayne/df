import feedparser
import spacy
import praw
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Reddit instance
reddit = praw.Reddit(client_id='d05wJmtbfKgEn4oizn--5g',
                    client_secret='2h_MfiBhPha540TsN7mN6WlenZ8NpQ',
                    user_agent='myapp/1.0')


# Initialize TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

def get_top_stories(new_articles, subreddits, max_number_of_stories=20):

    top_stories = []
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        top_stories += subreddit.top(limit=max_number_of_stories)

    articles = []
    for story in top_stories:
        title = story.title
        url = story.url
        summary = story.selftext
        articles.append({'title': title, 'url': url, 'summary': summary})

    return pd.concat([new_articles, pd.DataFrame(articles)], ignore_index=True)


def get_rss_stories(new_articles, rss_feeds):

    articles = []
    for rss_feed in rss_feeds:
        feed = feedparser.parse(rss_feed)
        for entry in feed.entries:
            title = entry.title
            url = entry.link
            summary = entry.summary
            articles.append({'title': title, 'url': url, 'summary': summary})

    return pd.concat([new_articles, pd.DataFrame(articles)], ignore_index=True)

def recommend_articles(reading_history, new_articles, N=5):

    # Create an empty DataFrame with the desired columns
    recommended_articles_df = pd.DataFrame(columns=['title', 'summary', 'url', 'similarity'])

    if len(reading_history) > 0:
        # Combine the summary, title, and keywords into a single text column for vectorization
        new_articles_text = new_articles['title'] + ' ' + new_articles['summary']
        reading_history_text = reading_history['title'] + ' ' + reading_history['summary']

        # Create a new dataframe with the merged text
        new_articles_merged = pd.DataFrame({'text': new_articles_text})
        reading_history_merged = pd.DataFrame({'text': reading_history_text})

        # Vectorize the text data using TfidfVectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        reading_history_vectors = vectorizer.fit_transform(reading_history_merged['text'])
        new_articles_vectors = vectorizer.transform(new_articles_merged['text'])

        # Calculate the cosine similarity between the reading history and new articles vectors
        similarity_matrix = cosine_similarity(new_articles_vectors, reading_history_vectors)

        # Get the indices of the top N articles for each new article
        top_N_indices = similarity_matrix.argsort()[:, :-N-1:-1]

        # Create a list of recommended articles for each reading history entry
        for i, reading_history_index in enumerate(reading_history.index):
            article_indices = top_N_indices[:, i]
            article_data = []
            for article_index in article_indices:
                title = new_articles.iloc[article_index]['title']
                summary = new_articles.iloc[article_index]['summary']
                url = new_articles.iloc[article_index]['url']
                similarity = similarity_matrix[article_index][i]
                article_data.append([title, summary, url, similarity])
            # Append the recommended articles for this reading history entry to the DataFrame
            recommended_articles_df = recommended_articles_df.append(pd.DataFrame(article_data, columns=['title', 'summary', 'url', 'similarity']), ignore_index=True)

    else:
        print("Random choice!")
        recommended_articles_df = new_articles.sample(n=N)

    return recommended_articles_df

# Get top stories and RSS stories
subreddits = ['worldnews', 'technology', 'science']
rss_feeds = ["https://rss.cnn.com/rss/edition.rss", "https://techcrunch.com/feed/"]

reading_history = pd.DataFrame(columns=['title', 'url', 'summary'])
new_articles = pd.DataFrame(columns=['title', 'url', 'summary'])

new_articles2 = get_top_stories(new_articles, subreddits)
all_articles = get_rss_stories(new_articles2, rss_feeds)

while True:
    # Get the recommended articles
    recommendations = recommend_articles(reading_history, all_articles)
    print(recommendations)
    for index, recommendation in recommendations.iterrows():

        # Display the recommended article
        print("\nRecommended Article:")
        print(recommendation)

        # Ask the user if they liked the article
        response = input("Did you like this article? (y/n) ")
        if response.lower() == 'y':
            # Add the article to the reading history
            reading_history = reading_history.append(recommendation, ignore_index=True)
            print("Article added to reading history.")
        
    # Ask the user if they want to continue
    response = input("Do you want to continue? (y/n) ")
    if response.lower() != 'y':
        break