# WhatsApp Chat Analyzer

## Project Overview
The **WhatsApp Chat Analyzer** is a Streamlit-based web application that allows users to analyze WhatsApp chat data. It provides insights such as message statistics, word frequency, emoji usage, active users, and activity trends over time.

## Technologies Used
- **Programming Language**: Python
- **Framework**: Streamlit
- **Data Analysis & Visualization**: Pandas, Matplotlib, Seaborn
- **Natural Language Processing**: WordCloud, Collections, Regex
- **File Handling**: File Uploader in Streamlit
- **Dependency Management**: pip

## Features
- Upload and process a WhatsApp chat file (.txt)
- Extract message count, word count, media messages, and links
- Generate monthly and daily message trends
- Identify most active users in group chats
- Create a WordCloud visualization of frequently used words
- Find most common words (excluding stop words)
- Analyze emoji usage
- Display weekly and monthly activity maps
- Generate a heatmap for user activity by time of day

## Installation and Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
   cd whatsapp-chat-analyzer
   ```

2. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```sh
   streamlit run app.py
   ```

## File Structure
```
whatsapp-chat-analyzer/
│── preprocessor.py    # Data preprocessing functions
│── helper.py          # Functions for statistical analysis
│── app.py             # Main Streamlit app
│── requirements.txt   # List of dependencies
│── README.md          # Project documentation
```

## How to Use
1. Open the application in your browser.
2. Upload a WhatsApp chat file (.txt) using the file uploader.
3. Select a user or analyze the chat overall.
4. Click "Show Analysis" to generate insights.

## Possible Interview Questions
1. What is the purpose of this project?
2. How does the WhatsApp Chat Analyzer process chat data?
3. What libraries and frameworks have you used?
4. How does Streamlit help in building this application?
5. How do you extract and preprocess data from WhatsApp chats?
6. What visualization techniques have you used?
7. How do you identify the most active users?
8. How does the word cloud work?
9. What challenges did you face while developing this project?
10. How can this project be improved in the future?

## Future Enhancements
- Support for multiple file formats (CSV, JSON)
- Sentiment analysis for messages
- Advanced filtering and search options
- Dashboard with more interactive visualizations
- Mobile-friendly UI improvements

## Contributing
Feel free to fork the repository, raise issues, and submit pull requests!

## License
This project is licensed under the MIT License.

