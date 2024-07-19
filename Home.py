import streamlit as st

st.title("Email/Text Spam Classifier and Model Training Results")

# Remove the sidebar title and selectbox
# st.sidebar.title("Navigation")
# page = st.sidebar.selectbox("Choose a page", ["Spam Classifier", "Model Training Results"])

# Use radio buttons for page selection instead of sidebar selectbox
page = st.selectbox(
    "Choose a page",
    ["Spam Classifier", "Model Training Results","Generate Data"],
    help="Select the page you want to view"
)
if page == "Spam Classifier":
    import pages.Spam_Classifier
    pages.Spam_Classifier.main()
elif page == "Model Training Results":
    import pages.Model_Training_Results
    pages.Model_Training_Results.main()
elif page == "Generate Data":
    import pages.Generate_Data
    pages.Generate_Data.main()
