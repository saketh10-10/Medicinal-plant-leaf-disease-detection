# Quick Fix: "Failed to fetch" Error

## 🚨 Immediate Actions Required

### Step 1: Set Environment Variable in Vercel (5 minutes)

1. Go to: https://vercel.com/dashboard
2. Click on your project: **Medicinal-plant-leaf-disease-detection**
3. Go to **Settings** → **Environment Variables**
4. Click **Add New**
5. Fill in:
   ```
   Key: VITE_API_BASE_URL
   Value: [YOUR_BACKEND_URL_HERE]
   Environments: ✅ Production ✅ Preview ✅ Development
   ```
6. Click **Save**
7. Go to **Deployments** → Click **⋯** on latest → **Redeploy**

### Step 2: Update Backend CORS (If Backend is Deployed)

**If your backend is already deployed:**

1. Go to your backend hosting platform (Railway/Render/etc.)
2. Add environment variable:
   ```
   Key: ALLOWED_ORIGINS
   Value: https://medicinal-plant-leaf-disease-detect.vercel.app,http://localhost:5173
   ```
3. Redeploy backend

**If backend is NOT deployed yet:**
- See `FIX_FAILED_TO_FETCH.md` for deployment instructions

### Step 3: Verify Fix

1. Wait for Vercel redeploy to complete
2. Visit your site: https://medicinal-plant-leaf-disease-detect.vercel.app
3. Open DevTools (F12) → Console
4. Try using the app
5. Should see API calls working (no "Failed to fetch" errors)

---

## ❓ What's Your Backend URL?

**Option 1: Backend on Railway**
- URL format: `https://your-app.railway.app`
- Find it in Railway dashboard

**Option 2: Backend on Render**
- URL format: `https://your-app.onrender.com`
- Find it in Render dashboard

**Option 3: Backend on Vercel**
- URL format: `https://your-backend.vercel.app`
- Find it in Vercel dashboard

**Option 4: Backend Not Deployed Yet**
- You need to deploy it first
- See `FIX_FAILED_TO_FETCH.md` for instructions

---

## ✅ After Fixing

Once you've:
1. ✅ Set `VITE_API_BASE_URL` in Vercel
2. ✅ Updated backend CORS (if deployed)
3. ✅ Redeployed both frontend and backend

Your API calls should work! 🎉

---

## 📖 Detailed Guide

For more detailed instructions, troubleshooting, and deployment guides, see:
- **`FIX_FAILED_TO_FETCH.md`** - Complete guide with all solutions

