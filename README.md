
# 💬 WhatsApp Chat Analyzer

**WhatsApp Chat Analyzer** is a powerful **Streamlit-based web application** built with Python that helps users gain insights from exported WhatsApp chat files. From statistical overviews to emoji analysis and heatmaps, it gives you a detailed breakdown of your communication patterns.

---

## 📌 Features

### 📂 Chat File Upload & Parsing
- Upload `.txt` files exported from WhatsApp
- Automatically detects sender, timestamps, and message types

### 📊 Analytics & Insights
- 📈 Message & word count
- 📎 Media and link message detection
- 🔥 Most active users in group chats
- 📆 Monthly & daily activity trends
- 📅 Weekly & hourly activity heatmaps
- 🧑‍🤝‍🧑 User-wise breakdown of contributions

### 🧠 NLP & Visualizations
- ☁️ WordCloud of frequent terms (excluding stop words)
- 💬 Most common words and phrases
- 😍 Emoji usage analysis and frequency
- 📊 Beautiful visualizations using Matplotlib & Seaborn

---

## 🧰 Tech Stack

| Category              | Tools Used                                  |
|-----------------------|---------------------------------------------|
| 👨‍💻 Programming       | Python                                       |
| 🖼️ UI Framework        | Streamlit                                    |
| 📊 Data Analysis       | Pandas, Collections, Regex                   |
| 📉 Visualization       | Matplotlib, Seaborn, WordCloud               |
| 📦 Package Management  | pip                                          |

---

## 📁 Project Structure

```
whatsapp-analyzer/
├── app.py              # Main Streamlit app logic
├── preprocessor.py     # Data preprocessing (timestamp parsing, etc.)
├── helper.py           # Stats, emoji, and user activity functions
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/vaibhav1445/whatsapp-analyzer.git
cd app
```

### 2️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 🚀 How to Use

1. Export your WhatsApp chat as a `.txt` file.
2. Launch the app in your browser.
3. Upload the chat file via the Streamlit interface.
4. Choose either **Overall** or a specific **User**.
5. Click **Show Analysis** to generate insightful visualizations.

---

## 🧪 Future Enhancements

- 📁 Multi-format support (CSV, JSON)
- 🔍 Advanced filters (by date, user, keywords)
- 📱 Mobile-first responsive design
- 📊 Interactive dashboard with Plotly or Altair
- 📤 Export analysis as PDF or Excel

---

## 🤝 Contributing

Contributions are welcome!  
Fork this repo, raise an issue, and submit a pull request 🙌

---

## 📄 License

Licensed under the **MIT License**. See [`LICENSE`](./LICENSE) for details.

---

## ⭐ Show Your Support

If you found this project helpful, give it a ⭐ on [GitHub](https://github.com/vaibhav1445/whatsapp-analyzer)!

> Made with ❤️ using Python and Streamlit by Vaibhav Srivastava
