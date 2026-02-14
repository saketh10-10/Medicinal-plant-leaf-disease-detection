# Vercel NOT_FOUND Error - Active Troubleshooting

## ✅ Issue Found and Fixed

**Root Cause**: TypeScript build was failing due to missing path alias configuration.

**Fix Applied**: Added path aliases to `tsconfig.app.json`:
```json
"baseUrl": ".",
"paths": {
  "@/*": ["./src/*"]
}
```

## 🔍 Verification Steps

### 1. Test Build Locally
```bash
cd frontend
npm run build
```

**Expected**: Build should complete successfully with output in `frontend/dist/`

### 2. Verify Build Output
```bash
# Check if index.html exists
Test-Path frontend\dist\index.html
```

**Expected**: Should return `True`

### 3. Check Vercel Configuration

Your `vercel.json` should be:
```json
{
  "version": 2,
  "buildCommand": "cd frontend && npm ci && npm run build",
  "outputDirectory": "frontend/dist",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## 🚨 Common Issues and Solutions

### Issue 1: Build Fails on Vercel
**Symptoms**: 
- Deployment shows "Build Failed" in Vercel dashboard
- Build logs show TypeScript errors

**Solution**:
1. Fix all TypeScript errors locally first
2. Ensure `tsconfig.app.json` has correct path aliases
3. Run `npm run build` locally to verify

### Issue 2: Build Succeeds but Still NOT_FOUND
**Symptoms**:
- Build completes successfully
- But site shows 404

**Possible Causes**:
1. **Wrong Root Directory in Vercel Settings**
   - Go to Vercel Dashboard → Project Settings → General
   - Check "Root Directory" - should be empty (root of repo) or set to project root
   - If set to `frontend/`, change it to empty or remove it

2. **Output Directory Mismatch**
   - Verify `outputDirectory` in `vercel.json` matches actual build output
   - For Vite: should be `frontend/dist`
   - Check build logs to see where files are actually created

3. **Missing Rewrites**
   - Ensure `rewrites` section exists in `vercel.json`
   - Should redirect all routes to `/index.html` for SPAs

### Issue 3: Environment Variables Not Set
**Symptoms**:
- Site loads but API calls fail
- Console shows CORS or connection errors

**Solution**:
1. Go to Vercel Dashboard → Settings → Environment Variables
2. Add `VITE_API_BASE_URL` with your backend URL
3. Redeploy after adding variables

## 📋 Pre-Deployment Checklist

Before deploying, verify:

- [ ] ✅ Build succeeds locally (`npm run build` in frontend/)
- [ ] ✅ `frontend/dist/index.html` exists after build
- [ ] ✅ `vercel.json` is in root directory
- [ ] ✅ `outputDirectory` in vercel.json matches actual output (`frontend/dist`)
- [ ] ✅ `buildCommand` is correct
- [ ] ✅ `rewrites` are configured for SPA routing
- [ ] ✅ No TypeScript errors (`tsc` or `npm run build`)
- [ ] ✅ `package-lock.json` is committed
- [ ] ✅ Root Directory in Vercel settings is correct (empty or root)

## 🔧 Vercel Dashboard Settings to Check

1. **Project Settings → General**
   - Root Directory: Should be empty (or `/` if you have monorepo)
   - Framework Preset: Can be "Other" or "Vite"

2. **Project Settings → Build & Development Settings**
   - Build Command: Should match `vercel.json` or be auto-detected
   - Output Directory: Should match `vercel.json` or be auto-detected
   - Install Command: Can be auto or `npm ci`

3. **Project Settings → Environment Variables**
   - `VITE_API_BASE_URL`: Your backend API URL

## 🐛 Debugging Steps

### Step 1: Check Build Logs
1. Go to Vercel Dashboard → Your Project → Deployments
2. Click on the failed deployment
3. Check "Build Logs" tab
4. Look for errors (TypeScript, npm, build failures)

### Step 2: Check Deployment Logs
1. Same deployment page
2. Check "Function Logs" or "Runtime Logs"
3. Look for runtime errors

### Step 3: Test Locally
```bash
# Build
cd frontend
npm ci
npm run build

# Preview build
npm run preview
# Visit http://localhost:4173
```

### Step 4: Verify File Structure
After local build, verify:
```
frontend/
  dist/
    index.html          ← Must exist
    assets/
      index-[hash].js
      index-[hash].css
```

## 🔄 Alternative Vercel Configuration

If the current config doesn't work, try this alternative:

```json
{
  "version": 2,
  "buildCommand": "cd frontend && npm ci && npm run build",
  "outputDirectory": "frontend/dist",
  "installCommand": "cd frontend && npm ci",
  "framework": null,
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

## 📞 Next Steps

1. **Commit and push the TypeScript fix**:
   ```bash
   git add frontend/tsconfig.app.json
   git commit -m "Fix TypeScript path alias configuration"
   git push
   ```

2. **Redeploy on Vercel**:
   - Vercel will automatically redeploy on push
   - Or manually trigger redeploy from dashboard

3. **Monitor the deployment**:
   - Watch build logs in real-time
   - Check if build succeeds
   - Verify site loads correctly

4. **If still failing**:
   - Share the build logs from Vercel
   - Check Vercel dashboard settings (Root Directory)
   - Verify all files are committed and pushed

## 🎯 Expected Result

After fixing the TypeScript issue and redeploying:
- ✅ Build should complete successfully
- ✅ Site should load at your Vercel URL
- ✅ All routes should work (thanks to rewrites)
- ✅ No more NOT_FOUND errors

