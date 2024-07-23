import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns

# Function to analyze sentiment
def analyze_sentiment(review):
    analysis = TextBlob(review)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Streamlit App
st.title("📊 Review Sentiment Analysis App 📝")
st.subheader("Sentiment Analysis App Develop by Muhammad Aqeel")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your review data", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview")
    st.dataframe(df.head())

    # Display column names and select the 'Review' column
    st.write("Select the column containing reviews")
    review_column = st.selectbox("Review Column", df.columns)

    if review_column:
        # Analyze sentiment
        df['Sentiment'] = df[review_column].apply(analyze_sentiment)

        # Sidebar options
        st.sidebar.header("Options")
        option = st.sidebar.radio("Select an option", ['Review Data', 'Data Visualization'])

        if option == 'Review Data':
            # Display total reviews
            total_reviews = df.shape[0]
            st.write(f"Total Reviews: {total_reviews} 📝")

            # Display positive reviews
            positive_reviews = df[df['Sentiment'] == 'Positive'].shape[0]
            st.write(f"Positive Reviews: {positive_reviews} 😊")

            # Display negative reviews
            negative_reviews = df[df['Sentiment'] == 'Negative'].shape[0]
            st.write(f"Negative Reviews: {negative_reviews} 😞")

        elif option == 'Data Visualization':
            st.subheader("Sentiment Distribution")

            # Pie chart
            st.write("Pie Chart")
            sentiment_counts = df['Sentiment'].value_counts()
            fig, ax = plt.subplots()
            ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

            # Area graph
            st.write("Area Graph")
            df['Sentiment'] = pd.Categorical(df['Sentiment'], categories=['Positive', 'Neutral', 'Negative'])
            sentiment_over_time = df.groupby(['Sentiment']).size().cumsum()
            fig, ax = plt.subplots()
            sentiment_over_time.plot(kind='area', ax=ax)
            ax.set_title("Cumulative Sentiment Over Time")
            st.pyplot(fig)

            # Scatter plot
            st.write("Scatter Plot")
            df['Polarity'] = df[review_column].apply(lambda x: TextBlob(x).sentiment.polarity)
            fig, ax = plt.subplots()
            sns.scatterplot(x=df.index, y='Polarity', hue='Sentiment', data=df, ax=ax)
            ax.set_title("Sentiment Polarity")
            st.pyplot(fig)

            # Bar plot
            st.write("Bar Plot")
            fig, ax = plt.subplots()
            sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)
            ax.set_title("Sentiment Count")
            st.pyplot(fig)
 