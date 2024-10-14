# Wordcloud Generator 🌀

## Overview
The Wordcloud Generator is a Streamlit application that allows users to create visually appealing word clouds from text files or directly entered text. Users can customize the appearance of the word clouds with various colors and shapes.

## Features
- Upload text files or enter text directly.
- Generate word clouds with customizable parameters.
- Option to use masking images to shape the word cloud.
- Display word frequencies as a bar chart.

## Requirements
The project requires the following Python packages:
- `streamlit`
- `wordcloud`
- `matplotlib`
- `numpy`
- `Pillow`
- `pandas`

## Installation
**1. Clone the repository:**
   git clone https://github.com/yourusername/wordcloud-generator.git
   cd wordcloud-generator

**2. Install the required packages:**   
   pip install -r requirements.txt

**3. Run the application:**
    streamlit run app.py

## GDPR Compliance
Please ensure that any text file uploaded does not contain personal data that could identify individuals, in compliance with GDPR. The generated word clouds do not store any personal data.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Note on JPG Files
If you want to include specific JPG files for the masks, you can add them directly to the repository. Otherwise, you can ignore them using the .gitignore file and provide instructions in the README on how users can obtain or create those files themselves.