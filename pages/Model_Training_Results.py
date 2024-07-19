import streamlit as st

def main():
    st.title("Model Training Results")

    st.header("Data Distribution")
    image_paths1 = [
        "Exploratory_Data_Analysis/pie_chart.png",
        "Exploratory_Data_Analysis/words_histogram.png",
        "Exploratory_Data_Analysis/characters_histogram.png"
    ]

    for image_path in image_paths1:
        st.image(image_path, caption=image_path.split('/')[-1], use_column_width=True)

    st.header("Correlation")
    image_paths2 = [
        "Exploratory_Data_Analysis/pairplots.png",
        "Exploratory_Data_Analysis/correlation_heatmap.png"
    ]

    for image_path in image_paths2:
        st.image(image_path, caption=image_path.split('/')[-1], use_column_width=True)
    
    st.header("Most Common Words")
    image_paths3 = [
        "Exploratory_Data_Analysis/most_common_NON_spam_words.png",
        "Exploratory_Data_Analysis/most_common_spam_words.png"
    ]

    for image_path in image_paths3:
        st.image(image_path, caption=image_path.split('/')[-1], use_column_width=True)

if __name__ == "__main__":
    main()
