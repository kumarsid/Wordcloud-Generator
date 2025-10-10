import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import string
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import time
import io
import pandas as pd

# Set page configuration with a wide layout
st.set_page_config(layout="wide", page_title="Wordcloud Generator", page_icon="🌀")

# Custom CSS for styling
st.markdown("""
<style>
    /* Override Streamlit's default styles */
    .stApp {
        max-width: 100%;
        padding: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }

    /* Header/Title styling */
    .css-1v0mbdj.e115fcil1 {
        width: 100%;
        text-align: center;
        margin-bottom: 2rem;
    }

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    /* Title text */
    .title-text {
        font-size: 36px;
        font-weight: bold;
        color: #4B0082;
        text-align: center;
        padding: 1rem 0;
    }

    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }

    /* Input area styling */
    .stTextArea textarea {
        background-color: white;
        border-radius: 10px;
        border: 1px solid #ddd;
        padding: 10px;
    }

    /* Button styling */
    .stButton > button {
        background-color: #6A5ACD !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        width: auto !important;
        margin: 1rem 0 !important;
    }

    .stButton > button:hover {
        background-color: #483D8B !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
    }

    /* Radio button group styling */
    .stRadio > label {
        color: #4B0082;
        font-weight: 500;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        padding: 2rem 1rem;
    }

    /* Footer styling */
    footer {
        text-align: center;
        padding: 1rem;
        font-size: 14px;
        color: #6A5ACD;
    }

    /* Make sure elements don't overflow */
    .element-container {
        width: 100% !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem;
        }
        
        .title-text {
            font-size: 28px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Apply the title using the custom class
st.markdown('<h1 class="title-text">Wordcloud Generator</h1>', unsafe_allow_html=True)

# About section moved to the main area
def about_section():
    st.markdown('<div class="about"><h2>About</h2><p>'
                'This Wordcloud Generator allows you to create visually appealing word clouds '
                'from your text files or directly entered text. It provides options to customize '
                'the appearance of the word cloud using different colors and shapes.<br><br>'
                '<strong>GDPR Compliance:</strong> '
                'Please ensure that any text file uploaded does not contain personal data '
                'that could identify individuals, in compliance with GDPR. '
                'The generated word clouds do not store any personal data.</p></div>',
                unsafe_allow_html=True)

# Colormap options
cmap_options = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'coolwarm', 'bone', 'copper', 'gray']

# Sidebar upload for text file
def upload_file():
    uploaded_file = st.sidebar.file_uploader("Upload text file", type=['txt'])
    return uploaded_file

# Sidebar upload for masking image
def upload_mask_image():
    masking_image = st.sidebar.file_uploader("Upload masking image (optional)", type=['jpg', 'png'])
    if masking_image is not None:
        return Image.open(masking_image)
    return None

# Predefined mask options
def get_predefined_mask():
    predefined_masks = {
        "Cloud": "Cloud.jpg",
        "Heart": "heart.jpg"
    }
    mask_choice = st.sidebar.selectbox("Or select a predefined mask", options=["None"] + list(predefined_masks.keys()))
    if mask_choice != "None":
        return Image.open(predefined_masks[mask_choice])
    return None

# Wordcloud generator function
def make_wordcloud(text_input, cmap='viridis', mask_image=None, min_font_size=10, max_font_size=100, max_words=200):
    stopwords = set(STOPWORDS)
    tokens = text_input.split()
    punctuation_mapping_table = str.maketrans('', '', string.punctuation)
    tokens_stripped_of_punctuation = [token.translate(punctuation_mapping_table) for token in tokens]
    lower_tokens = [token.lower() for token in tokens_stripped_of_punctuation]

    joined_string = (" ").join(lower_tokens)

    # Check if the mask image is provided
    if mask_image is not None:
        mask_image_array = np.array(mask_image)
    else:
        mask_image_array = None

    # Create and save the wordcloud
    wordcloud = WordCloud(width=800,  # Adjust width for better display
                          height=600,  # Adjust height for better display
                          stopwords=stopwords,
                          min_font_size=min_font_size,
                          max_font_size=max_font_size,
                          max_words=max_words,
                          colormap=cmap,
                          mask=mask_image_array,
                          background_color="white").generate(joined_string)

    plt.figure(figsize=(12, 8))  # Adjust figure size for better laptop view
    plt.axis("off")
    plt.imshow(wordcloud)
    
    # Save to a BytesIO object instead of a file
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=300, bbox_inches='tight')
    img_buf.seek(0)
    
    return img_buf, wordcloud, joined_string  # Return joined_string here

# Display the generated wordcloud and provide download option
def run_app(img_buf, wordcloud, joined_string):  # Accept joined_string as a parameter
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.image(img_buf)
        
        btn = st.download_button(
            label="Download image",
            data=img_buf,
            file_name="wordcloud.png",
            mime="image/png",
            key="download_button"
        )
    
    with col2:
        st.subheader("Word Frequencies")
        word_freq = wordcloud.words_
        sorted_word_freq = dict(sorted(word_freq.items(), key=lambda item: item[1], reverse=True)[:20])
        
        # Create a DataFrame for better visualization
        word_freq_df = pd.DataFrame(sorted_word_freq.items(), columns=['Word', 'Frequency'])
        word_freq_df['Frequency'] = (word_freq_df['Frequency'] * len(joined_string.split())).astype(int)  # Show counts
        
        # Display a bar chart
        st.bar_chart(word_freq_df.set_index('Word'))

# Main app logic
def main():
    

    st.sidebar.title("Settings")
    st.sidebar.header("This is testing the changes")
    st.header("This is testing the changes in the main section")
    # Input method selection
    input_method = st.sidebar.radio("Choose input method", ["Upload File", "Enter Text"])
    
    if input_method == "Upload File":
        text_file = upload_file()
        if text_file is not None:
            read_file = text_file.read().decode('utf-8')
        else:
            read_file = None
    else:
        read_file = st.text_area("Enter your text here", height=200, key="text_input", help="Type or paste your text here")
    
    if read_file:
        masking_image = upload_mask_image()
        if masking_image is None:
            masking_image = get_predefined_mask()

        cmap = st.sidebar.selectbox("Select a colormap", options=cmap_options, index=0)
        
        # Advanced options
        with st.sidebar.expander("Advanced Options"):
            min_font_size = st.slider("Minimum Font Size", 4, 20, 10)
            max_font_size = st.slider("Maximum Font Size", 50, 200, 100)
            max_words = st.slider("Maximum Words", 50, 500, 200)

        if st.sidebar.button("Generate Wordcloud", key="run_button"):
            with st.spinner('🌪️ Generating WordCloud...'):
                start_time = time.time()
                img_buf, wordcloud, joined_string = make_wordcloud(read_file, cmap=cmap, mask_image=masking_image, 
                                                                   min_font_size=min_font_size, max_font_size=max_font_size, 
                                                                   max_words=max_words)
                end_time = time.time()
                execution_time = end_time - start_time
                st.success(f"Wordcloud generated in {execution_time:.2f} seconds!")
                run_app(img_buf, wordcloud, joined_string)  # Pass joined_string to run_app
    else:
        st.info("👈 Please upload a text file or enter text to get started.")

    # Footer
    st.markdown(
        '<div class="footer">Created with 💜 by Sid | '
        '<a href="https://github.com/kumarsid" target="_blank">GitHub</a></div>',
        unsafe_allow_html=True
    )

    about_section()  

if __name__ == "__main__":
    main()
