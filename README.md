# 📚 Basecamp Handbook RAG Web Application

A beautiful, interactive web application for querying the Basecamp Employee Handbook using Retrieval-Augmented Generation (RAG). Built with Flask, LangChain, and OpenAI.

## 🎯 Features

✨ **Beautiful Chat Interface** - Modern, responsive UI for asking questions
🔍 **RAG-Powered Answers** - Retrieves relevant information from the Basecamp handbook
📖 **Source Attribution** - Shows which handbook sections were used to answer your question
⚡ **Real-time Processing** - Fast, interactive responses
🔒 **Secure** - API keys stored in environment variables, never committed to GitHub

## 🛠️ Tech Stack

- **Backend**: Flask (Python web framework)
- **RAG System**: LangChain + ChromaDB + OpenAI API
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI text-embedding-ada-002
- **LLM**: GPT-3.5-turbo

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (get it at https://platform.openai.com/api-keys)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/saad-jabara/rag-web-app.git
cd rag-web-app
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**⚠️ IMPORTANT**: Never commit the `.env` file to GitHub! The `.gitignore` is configured to prevent this.

### 5. Run the Application

```bash
python app.py
```

The application will:
1. Load documents from Basecamp handbook URLs
2. Create embeddings and build the vector database
3. Start the Flask server on `http://localhost:5000`

Open your browser and navigate to `http://localhost:5000`

## 💬 Usage

1. Type a question about Basecamp's employee handbook
2. Click "Send" or press Enter
3. The system will retrieve relevant sections and generate an answer
4. View the sources that were used to answer your question

### Example Questions

- "What benefits does Basecamp offer employees?"
- "How does Basecamp support work-life balance?"
- "What is Basecamp's approach to internal communication?"
- "How are work hours structured at Basecamp?"
- "What diversity and inclusion initiatives does Basecamp have?"

## 🏗️ How It Works

### Architecture

```
User Question
      ↓
[Embed Question with OpenAI]
      ↓
[Search Vector Database]
      ↓
[Retrieve Top 3 Relevant Chunks]
      ↓
[Send to GPT-3.5-turbo with Context]
      ↓
[Return Answer + Sources]
```

### Key Components

1. **Document Loader** - Fetches content from Basecamp handbook URLs
2. **Text Splitter** - Chunks documents (500 chars, 100 char overlap)
3. **Embeddings** - Converts text to vector embeddings
4. **Vector Store** - Stores and searches embeddings with ChromaDB
5. **Retriever** - Finds top 3 most relevant chunks for each query
6. **LLM Chain** - Uses GPT-3.5-turbo to generate answers with context

## 📁 Project Structure

```
rag-web-app/
├── app.py                  # Flask application and RAG logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── templates/
│   └── index.html         # Frontend UI
└── chroma_db/             # Vector database (auto-created)
```

## 🔒 Security Best Practices

✅ **Environment Variables** - API keys stored in `.env`, not in code
✅ `.gitignore` - Prevents `.env` from being committed
✅ **CORS Enabled** - Safe cross-origin requests
✅ **Input Validation** - Questions validated before processing
✅ **Error Handling** - Graceful error messages

### Never Do This ❌

```bash
# DON'T hardcode API keys in code
OPENAI_API_KEY = "sk-xxxxxxxxxxxx"

# DON'T commit .env to GitHub
git add .env

# DON'T push to public repo with credentials
git push origin main
```

## 🚢 Deployment

### Deploy to Render (Free Tier Available)

1. Push code to GitHub
2. Go to https://render.com
3. Create new Web Service
4. Connect GitHub repository
5. Set environment variables in Render dashboard
6. Deploy!

### Deploy to Vercel (Frontend) + Backend

1. Split into separate frontend (Vercel) and backend (Render/Railway)
2. Update frontend API calls to backend URL

### Deploy to Railway

1. Connect GitHub repository
2. Set `OPENAI_API_KEY` in Railway dashboard
3. Railway auto-detects Flask and deploys

## 🛠️ Troubleshooting

### "Please set OPENAI_API_KEY in your .env file"

- Check that `.env` file exists in project root
- Verify `OPENAI_API_KEY` is set correctly
- Make sure you copied `.env.example` to `.env`

### "Connection timeout loading documents"

- Check your internet connection
- Verify Basecamp handbook URLs are accessible
- May take a few minutes on first run

### "ModuleNotFoundError: No module named 'flask'"

- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### "Address already in use"

- Another process is using port 5000
- Change port: `app.run(port=5001)`
- Or kill the process: `lsof -i :5000` then `kill -9 <PID>`

## 📚 Knowledge Base

This RAG system is trained on the Basecamp Employee Handbook covering:

- How We Work
- Benefits and Perks
- Work-Life Balance
- Internal Communication
- Getting Started Guide
- Diversity, Equity, and Inclusion (DEI)
- Pricing and Profit
- Support Titles
- Internal Systems

## 📊 API Endpoints

### GET `/`
Returns the main HTML page with chat interface

### POST `/api/query`
Process a question through the RAG system

**Request:**
```json
{
  "question": "What benefits does Basecamp offer?"
}
```

**Response:**
```json
{
  "answer": "Basecamp offers comprehensive benefits...",
  "sources": [
    {
      "source": "https://basecamp.com/handbook/benefits-and-perks",
      "content": "..."
    }
  ],
  "status": "success"
}
```

### GET `/api/health`
Health check endpoint

## 🧠 Advanced Customization

### Use Different LLM Model

Edit `app.py`, change the model:
```python
llm = ChatOpenAI(model="gpt-4", temperature=0)  # Use GPT-4 instead
```

### Adjust Chunk Size

Edit `app.py`, modify RecursiveCharacterTextSplitter:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Increase for longer context
    chunk_overlap=200
)
```

### Add More Sources

Edit `app.py`, add URLs to `basecamp_urls`:
```python
basecamp_urls = [
    # ... existing URLs ...
    "https://your-custom-handbook.com/page"
]
```

### Change Temperature

Lower temperature = more deterministic answers
Higher temperature = more creative answers

```python
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
```

## 🤝 Contributing

Feel free to fork and customize this project for your own needs!

### Ideas for Enhancement

- Add user authentication
- Store conversation history in database
- Implement chat sessions
- Add document upload feature
- Support multiple knowledge bases
- Implement user feedback/ratings
- Add analytics dashboard

## 📝 License

MIT License - Use freely for personal and commercial projects

## 👨‍💻 Author

**Saad Jabara**
- AI Engineer | Python Developer | LangChain Practitioner
- GitHub: https://github.com/saad-jabara

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

---

⭐ If you found this helpful, please star the repository!

Built with ❤️ using Flask, LangChain, and OpenAI
