# Backend Deployment Guide

This guide will help you deploy your Python FastAPI backend with ML model to production.

## 🎯 Recommended: Railway (Easiest for Python + ML)

Railway is the easiest platform for deploying Python applications with ML models.

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"

### Step 2: Deploy from GitHub

1. Click **"Deploy from GitHub repo"**
2. Select your repository: `saketh10-10/Medicinal-plant-leaf-disease-detection`
3. Railway will auto-detect it's a Python project

### Step 3: Configure Settings

1. **Root Directory**: Set to `backend` (important!)
   - Go to Settings → Source
   - Set Root Directory: `backend`

2. **Start Command**: 
   ```
   python -m uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
   - Go to Settings → Deploy
   - Set Start Command (or Railway will auto-detect)

3. **Environment Variables**:
   - Go to Settings → Variables
   - Add:
     ```
     ALLOWED_ORIGINS=https://medicinal-plant-leaf-disease-detect.vercel.app,http://localhost:5173
     PORT=8000
     ```

### Step 4: Deploy

1. Railway will automatically:
   - Install dependencies from `requirements.txt`
   - Build your application
   - Deploy it

2. Wait for deployment to complete (5-10 minutes first time)

3. Get your backend URL:
   - Go to Settings → Domains
   - Railway provides a URL like: `https://your-app.railway.app`
   - Or add a custom domain

### Step 5: Update Frontend

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Your project → Settings → Environment Variables
3. Add/Update:
   ```
   Key: VITE_API_BASE_URL
   Value: https://your-app.railway.app
   ```
4. Redeploy frontend

---

## 🚀 Alternative: Render

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select: `saketh10-10/Medicinal-plant-leaf-disease-detection`

### Step 3: Configure Settings

**Basic Settings:**
- **Name**: `medicinal-plant-backend` (or any name)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
- Click "Environment" tab
- Add:
  ```
  ALLOWED_ORIGINS=https://medicinal-plant-leaf-disease-detect.vercel.app,http://localhost:5173
  PORT=8000
  ```

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Get your URL: `https://your-app.onrender.com`

### Step 5: Update Frontend

Same as Railway - update `VITE_API_BASE_URL` in Vercel.

---

## ⚙️ Alternative: Vercel (Advanced)

Vercel supports Python but has limitations with large files (ML models).

### Limitations:
- Function size limit (50MB)
- Model file might be too large
- Cold start latency

### If you want to try Vercel:

1. Create `api/index.py` in root:
```python
from backend.main import app
```

2. Create `vercel.json` for backend (separate from frontend):
```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend/main.py"
    }
  ]
}
```

**Note**: This is complex and may not work well with large model files. Railway or Render are recommended.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] ✅ `requirements.txt` includes all dependencies (torch, torchvision, etc.)
- [ ] ✅ `plant_disease_model.pth` is in `backend/` directory
- [ ] ✅ `plant_info.json` is in `backend/` directory
- [ ] ✅ `class_names.json` is in `backend/` directory
- [ ] ✅ Model file is committed to git (check `.gitignore`)
- [ ] ✅ Backend runs locally: `python -m uvicorn main:app`
- [ ] ✅ Model loads successfully
- [ ] ✅ CORS is configured correctly

### ⚠️ Important: Model File Size

If your `plant_disease_model.pth` file is **larger than 100MB**:
1. **Option 1**: Use Git LFS (Large File Storage)
   ```bash
   git lfs install
   git lfs track "*.pth"
   git add .gitattributes
   git add backend/plant_disease_model.pth
   git commit -m "Add model file with Git LFS"
   ```

2. **Option 2**: Host model externally
   - Upload to cloud storage (S3, Google Cloud Storage, etc.)
   - Download model on first request
   - Cache in memory

3. **Option 3**: Use Railway's file system
   - Railway can handle large files
   - Just ensure it's committed to git

---

## 🔧 Troubleshooting

### Issue: Model file too large

**Railway/Render**: Should handle large files fine (up to several GB)

**Vercel**: Has 50MB function limit. Consider:
- Using a model hosting service (Hugging Face, etc.)
- Loading model from external storage

### Issue: Build fails - missing dependencies

**Fix**: Ensure `requirements.txt` includes:
```
torch>=2.5.0
torchvision>=0.20.0
```

### Issue: Model not found error

**Fix**: 
1. Ensure model file is committed to git
2. Check Root Directory is set to `backend`
3. Verify file paths in `predict.py` are relative

### Issue: CORS errors

**Fix**: 
1. Set `ALLOWED_ORIGINS` environment variable
2. Include your Vercel frontend domain
3. Redeploy backend

### Issue: Port binding error

**Fix**: Use `$PORT` environment variable:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 🧪 Testing Deployment

After deployment:

1. **Health Check**:
   ```
   GET https://your-backend.railway.app/health
   ```
   Should return: `{"status": "healthy"}`

2. **Root Endpoint**:
   ```
   GET https://your-backend.railway.app/
   ```
   Should return API info

3. **Model Status**:
   ```
   GET https://your-backend.railway.app/model-status
   ```
   Should show model is loaded

4. **Test Upload**:
   - Use Postman or curl to test `/test-upload` endpoint
   - Or test from your frontend

---

## 📊 Cost Comparison

**Railway**:
- Free tier: $5 credit/month
- Paid: $0.000463/GB-hour + $0.01/GB transfer
- Good for: Development and small projects

**Render**:
- Free tier: Spins down after 15 min inactivity
- Paid: $7/month for always-on
- Good for: Production apps

**Vercel**:
- Free tier: Limited for Python
- Paid: $20/month
- Good for: Frontend (not recommended for Python ML)

---

## ✅ Recommended Setup

**Best for your project**:
1. **Frontend**: Vercel (already deployed ✅)
2. **Backend**: Railway (recommended) or Render

**Why Railway?**
- ✅ Easy Python deployment
- ✅ Handles large files (ML models)
- ✅ Good free tier
- ✅ Simple configuration
- ✅ Auto-deploys from GitHub

---

## 🎯 Quick Start (Railway)

1. Go to [railway.app](https://railway.app) → Sign up
2. New Project → Deploy from GitHub
3. Select your repo
4. Settings → Root Directory: `backend`
5. Settings → Variables → Add `ALLOWED_ORIGINS`
6. Wait for deploy
7. Copy URL → Update Vercel `VITE_API_BASE_URL`
8. Done! 🎉

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vercel Python Functions](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

---

## 🆘 Need Help?

If you encounter issues:
1. Check deployment logs
2. Verify environment variables
3. Test endpoints with Postman/curl
4. Check backend logs for errors
5. Ensure model file is committed to git

