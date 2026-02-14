# Quick Backend Deployment Guide

## 🚀 Deploy to Railway (Recommended - 5 minutes)

### Step 1: Sign Up
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign in with GitHub

### Step 2: Deploy
1. Click **"Deploy from GitHub repo"**
2. Select: `saketh10-10/Medicinal-plant-leaf-disease-detection`
3. Railway will auto-detect Python

### Step 3: Configure
1. Go to **Settings** → **Source**
2. Set **Root Directory**: `backend`
3. Go to **Settings** → **Variables**
4. Add environment variable:
   ```
   Key: ALLOWED_ORIGINS
   Value: https://medicinal-plant-leaf-disease-detect.vercel.app,http://localhost:5173
   ```

### Step 4: Get Your URL
1. Wait for deployment (5-10 minutes)
2. Go to **Settings** → **Domains**
3. Copy your Railway URL (e.g., `https://your-app.railway.app`)

### Step 5: Update Frontend
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Your project → **Settings** → **Environment Variables**
3. Add/Update:
   ```
   Key: VITE_API_BASE_URL
   Value: https://your-app.railway.app
   ```
4. **Redeploy** frontend

### ✅ Done!
Your backend is now deployed and connected to your frontend!

---

## 🆘 Troubleshooting

**Build fails?**
- Check Root Directory is set to `backend`
- Verify `requirements.txt` includes torch/torchvision

**CORS errors?**
- Ensure `ALLOWED_ORIGINS` includes your Vercel domain
- Redeploy backend after adding variable

**Model not found?**
- Ensure `plant_disease_model.pth` is committed to git
- Check it's in `backend/` directory

---

## 📖 Full Guide
See `BACKEND_DEPLOYMENT_GUIDE.md` for detailed instructions and alternatives.

