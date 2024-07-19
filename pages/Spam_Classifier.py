import streamlit as st
import pickle
from spam_detection import data_preprocessing

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

def main():
    st.title("Email/Text Spam Classifier")
    input_sms = st.text_area("Enter The Email/Text")

    if st.button('Predict'):
        # 1. Preprocess
        transformed_sms = data_preprocessing(input_sms)
        
        # 2. Vectorize
        vector_input = tfidf.transform([transformed_sms])
        
        # 3. Predict
        result = model.predict(vector_input)[0]
        
        # 4. Display
        if result == 1:
            st.header("Spam")
        else:
            st.header("Not Spam")

if __name__ == "__main__":
    main()