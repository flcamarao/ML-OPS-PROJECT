import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import pickle
import base64

def get_img(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

def main():
    # Streamlit app title
    st.title("MOOD Magic")

    # Textbox for user input (URL)
    url = st.text_input("Enter URL:", "")

    # Function to get text from a web page
    def get_text_from_link(url):
        if url:
            if not url.startswith(('http://', 'https://')):
                st.write("Please enter a valid URL with 'http://' or 'https://'.")
                return None

            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = re.sub('[\n\t]+', ' ', soup.get_text().strip())
                return text
            else:
                st.write("Failed to retrieve content from the URL. Please check the URL and try again.")
                return None
        else:
            st.write("Please enter a URL to fetch text from.")
            return None

    # Check if 'fetched_text' is in the session state
    if 'fetched_text' not in st.session_state:
        st.session_state.fetched_text = ""

    user_input = get_text_from_link(url)

    # model_name = "facebook/bart-large-xsum"
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = BartForConditionalGeneration.from_pretrained(model_name)

    # def generate_summaries(model, text, max_length=100):
    #     """
    #     Function to generate text summaries using the summarization model.
    #     """
    #     batch = tokenizer([text], truncation=True, padding="longest", 
    #                     return_tensors="pt")
        
    #     translated = model.generate(**batch, max_length=max_length)
    #     tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    #     return tgt_text[0]


   

    # # Create containers for different sections
    # text_container = st.container()
    # classify_container = st.container()

    # Load the saved model using pickle
    with open('best_model1.pkl', 'rb') as file:
        loaded_model = pickle.load(file)


    # Create two columns for the buttons
    col1, col2 = st.columns(2)

    # Position the "Fetch Text" button in the first column
    with col1:
        if st.button("Fetch Text"):
            user_input = get_text_from_link(url)
            if user_input:
                # Limit the display to a maximum number of characters (e.g., 200 characters)
                max_display_length = 200
                st.session_state.fetched_text = user_input[:max_display_length] + ('...' if len(user_input) > max_display_length else '')
            else:
                st.write("No text fetched. Please check the URL and try again.")

    # Position the "Classify" button in the second column
    result_text = ''
    with col2:
        if st.button("Classify"):
            
            if user_input:
                # Make predictions using the loaded model
                prediction = loaded_model.predict([user_input])[0]
                # Format the prediction result into a single string
                result_text = f"Predicted Mood: {prediction}"
                # Display the formatted result
                
    
    # Display the fetched text, if it exists
    text_container = st.container()
    if st.session_state.fetched_text:
        text_container.write("Fetched Text:")
        text_container.write(st.session_state.fetched_text)
        # text = df['content.clean'].iloc[3] # CHANGE THIS
        # st.warning(generate_summaries(model, st.session_state.fetched_text))
    
    
    classify_container = st.container()
    if result_text != (''):
        classify_container.write(result_text)
    if result_text == 'Predicted Mood: INSPIRED':
        emotions = f"""
            <img src="data:image/png;base64,{get_img("images/inspired.jpg")}" >
        """
        st.markdown(emotions, unsafe_allow_html=True)

    if result_text == 'Predicted Mood: ANGRY':
        emotions = f"""
            <img src="data:image/png;base64,{get_img("images/angry.jpg")}" >
        """
        st.markdown(emotions, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
