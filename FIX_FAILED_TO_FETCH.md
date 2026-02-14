# Fix "Failed to fetch" Error

## 🔴 Problem

You're seeing `❌ Error: Failed to fetch` when trying to use the API from your deployed Vercel site.

## 🔍 Root Causes

This error typically occurs due to **three main issues**:

1. **Missing Environment Variable**: `VITE_API_BASE_URL` not set in Vercel
2. **CORS Configuration**: Backend doesn't allow requests from your Vercel domain
3. **Backend Not Accessible**: Backend not deployed or URL is incorrect

---

## ✅ Solution 1: Set Environment Variable in Vercel

### Step 1: Get Your Backend URL

First, you need to know where your backend is deployed. Options:

**Option A: Backend deployed on Railway/Render/etc.**
- Your backend URL: `https://your-backend.railway.app` or similar

**Option B: Backend deployed on Vercel (separate project)**
- Your backend URL: `https://your-backend.vercel.app`

**Option C: Backend running locally (development only)**
- Use a tunneling service like ngrok: `https://your-app.ngrok.io`

### Step 2: Add Environment Variable in Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project: **Medicinal-plant-leaf-disease-detection**
3. Go to **Settings** → **Environment Variables**
4. Click **Add New**
5. Enter:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: Your backend URL (e.g., `https://your-backend.railway.app`)
   - **Environments**: Select all (Production, Preview, Development)
6. Click **Save**
7. **Redeploy** your application:
   - Go to **Deployments** tab
   - Click the three dots (⋯) on the latest deployment
   - Click **Redeploy**

### Step 3: Verify

After redeploy, check the browser console:
- Open your Vercel site
- Open Developer Tools (F12)
- Check the Network tab
- API calls should now go to your backend URL, not `localhost:8000`

---

## ✅ Solution 2: Fix CORS Configuration

Your backend needs to allow requests from your Vercel domain.

### Updated Backend Code

I've already updated `backend/main.py` to:
- Read allowed origins from environment variable
- Automatically add Vercel domain if `VERCEL_URL` is set
- Support both development and production

### If Backend is Deployed Separately

**For Railway/Render/Other Platforms:**

1. Set environment variable in your backend deployment:
   - **Key**: `ALLOWED_ORIGINS`
   - **Value**: `https://medicinal-plant-leaf-disease-detect.vercel.app,http://localhost:5173`
   - (Add your Vercel domain + localhost for local dev)

2. **Redeploy your backend** after setting the variable

**For Vercel Backend Deployment:**

If you deploy backend on Vercel, set:
- `ALLOWED_ORIGINS`: `https://medicinal-plant-leaf-disease-detect.vercel.app,http://localhost:5173`
- `VERCEL_URL`: Will be auto-set by Vercel

### Manual CORS Update (Alternative)

If you can't use environment variables, update `backend/main.py` directly:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174", 
        "http://localhost:5175",
        "https://medicinal-plant-leaf-disease-detect.vercel.app",  # Add your Vercel domain
        "https://*.vercel.app",  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**⚠️ Security Note**: For production, it's better to specify exact domains rather than using wildcards.

---

## ✅ Solution 3: Deploy Your Backend

If your backend isn't deployed yet, you need to deploy it first.

### Option A: Deploy to Railway (Recommended for Python)

1. Go to [Railway](https://railway.app)
2. Create new project → Deploy from GitHub
3. Select your repository
4. Railway will auto-detect Python
5. Set start command: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `ALLOWED_ORIGINS`: `https://medicinal-plant-leaf-disease-detect.vercel.app,http://localhost:5173`
7. Get your Railway URL (e.g., `https://your-app.railway.app`)
8. Use this URL as `VITE_API_BASE_URL` in Vercel

### Option B: Deploy to Render

1. Go to [Render](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Settings:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as Railway)
6. Get your Render URL

### Option C: Deploy Backend to Vercel (Advanced)

Vercel supports Python, but it's more complex. See [Vercel Python documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python).

---

## 🧪 Testing the Fix

### 1. Check Environment Variable

After setting `VITE_API_BASE_URL` in Vercel and redeploying:

1. Open your Vercel site
2. Open Browser DevTools (F12)
3. Go to Console tab
4. Type: `console.log(import.meta.env.VITE_API_BASE_URL)`
5. Should show your backend URL (not `localhost:8000`)

### 2. Test API Connection

1. Open Network tab in DevTools
2. Try to use a feature that calls the API
3. Check the Network requests:
   - Should see requests to your backend URL
   - Should NOT see `localhost:8000`
   - Status should be 200 (not CORS errors)

### 3. Check CORS Headers

In Network tab, click on an API request:
- Look at Response Headers
- Should see: `Access-Control-Allow-Origin: https://medicinal-plant-leaf-disease-detect.vercel.app`
- If you see CORS error, backend CORS is not configured correctly

---

## 📋 Quick Checklist

- [ ] Backend is deployed and accessible
- [ ] `VITE_API_BASE_URL` is set in Vercel (Settings → Environment Variables)
- [ ] `ALLOWED_ORIGINS` is set in backend deployment (includes your Vercel domain)
- [ ] Frontend is redeployed after setting environment variable
- [ ] Backend is redeployed after setting CORS
- [ ] Test in browser - API calls should work

---

## 🐛 Still Not Working?

### Check Browser Console

1. Open DevTools (F12) → Console tab
2. Look for specific error messages:
   - `CORS policy`: Backend CORS issue
   - `Failed to fetch`: Network/connection issue
   - `404 Not Found`: Wrong API URL
   - `NetworkError`: Backend not accessible

### Check Network Tab

1. DevTools → Network tab
2. Try using the app
3. Look for failed requests (red)
4. Click on failed request → Check:
   - **Request URL**: Is it correct?
   - **Status Code**: What error?
   - **Response**: Any error message?

### Common Issues

**Issue**: Still seeing `localhost:8000` in requests
- **Fix**: Environment variable not set or frontend not redeployed
- **Action**: Set `VITE_API_BASE_URL` in Vercel and redeploy

**Issue**: CORS error in console
- **Fix**: Backend doesn't allow your Vercel domain
- **Action**: Update backend CORS configuration

**Issue**: 404 or connection refused
- **Fix**: Backend URL is wrong or backend is down
- **Action**: Verify backend is deployed and URL is correct

**Issue**: Works locally but not in production
- **Fix**: Environment variable only set locally
- **Action**: Set `VITE_API_BASE_URL` in Vercel dashboard

---

## 📚 Additional Resources

- [Vercel Environment Variables](https://vercel.com/docs/environment-variables)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)

---

## 🎯 Summary

The "Failed to fetch" error is almost always caused by:

1. **Missing `VITE_API_BASE_URL`** → Set in Vercel dashboard
2. **CORS blocking requests** → Update backend CORS configuration
3. **Backend not deployed** → Deploy backend first

Fix all three, and your API calls should work! 🚀

