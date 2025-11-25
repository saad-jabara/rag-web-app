# Deploy to Render - Step by Step

## 🚀 Deploy in 5 Minutes

### Step 1: Log In to Render
1. Go to https://render.com/dashboard
2. Sign in with your Render account

### Step 2: Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**

### Step 3: Connect GitHub Repository
1. Select **"GitHub"** as the source
2. Find and click **"rag-web-app"** repository
3. Click **"Connect"**

### Step 4: Configure Service Settings

Fill in the following fields:

| Field | Value |
|-------|-------|
| **Name** | `rag-web-app` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | `Free` (or paid for better performance) |

### Step 5: Add Environment Variables

1. Scroll down to **"Environment"** section
2. Click **"Add Environment Variable"**
3. Add this variable:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | Leave **BLANK FOR NOW** |

4. Click **"Save"** (Render will prompt you if empty)

### Step 6: Deploy

1. Click **"Deploy"** button
2. Wait for deployment to complete (2-5 minutes)
3. You'll see a message: "Your service is live"
4. Render will give you a URL like: `https://rag-web-app.onrender.com`

### Step 7: Add Your API Key (Later)

Once you have your new OpenAI API key:

1. Go back to Render dashboard
2. Click on your `rag-web-app` service
3. Go to **"Environment"** tab
4. Update `OPENAI_API_KEY` with your actual key
5. Click **"Save"** - service will auto-restart

## ✅ Testing Your Deployment

1. Open the Render URL in your browser
2. You should see the RAG chat interface
3. Try asking a question (after you add the API key)

## 🔗 Your Live Application

Once deployed, your app will be at:
```
https://rag-web-app.onrender.com
```

Share this URL with anyone who wants to use it!

## 🐛 Troubleshooting

### Build Failed
- Check the build logs in Render dashboard
- Ensure all files were pushed to GitHub
- Try redeploying

### "OPENAI_API_KEY not set" Error
- Go to Environment settings
- Add your OpenAI API key
- Save and redeploy

### Slow First Response
- First request on free tier can be slow (cold start)
- Subsequent requests will be faster

### Service Crashed
- Check logs in Render dashboard
- Make sure API key is set
- Try redeploying

## 💡 Next Steps

1. ✅ Deploy to Render
2. Get new OpenAI API key from https://platform.openai.com/api-keys
3. Add API key to Render environment variables
4. Test asking questions
5. Share the URL with others!

---

**Your GitHub Repository:** https://github.com/saad-jabara/rag-web-app

**Need Help?** Check the README.md file for more details.
