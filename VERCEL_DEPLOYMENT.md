# Vercel Deployment Guide

## ✅ Fix Applied

I've resolved the Vercel NOT_FOUND error by creating a proper `vercel.json` configuration file and fixing the API URL configuration.

## 📋 Changes Made

### 1. Created `vercel.json`
- **Location**: Root directory
- **Purpose**: Tells Vercel how to build and serve your application
- **Key configurations**:
  - `buildCommand`: Builds the frontend
  - `outputDirectory`: Points to `frontend/dist` (Vite's default output)
  - `rewrites`: Handles SPA routing (all routes → `index.html`)

### 2. Fixed API Base URL
- **File**: `frontend/src/services/api.ts`
- **Change**: Now uses environment variable `VITE_API_BASE_URL` with fallback to localhost
- **Why**: Hardcoded `localhost` URLs don't work in production

## 🚀 Deployment Steps

### Option 1: Deploy via Vercel Dashboard
1. Push your changes to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Vercel will auto-detect the `vercel.json` configuration
5. Add environment variable:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: Your backend API URL (e.g., `https://your-backend.vercel.app` or your deployed backend)

### Option 2: Deploy via CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variable
vercel env add VITE_API_BASE_URL
```

## 🔧 Environment Variables

You need to set `VITE_API_BASE_URL` in Vercel:

1. Go to your project settings in Vercel
2. Navigate to "Environment Variables"
3. Add:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: Your backend API URL
   - **Environments**: Production, Preview, Development

## 📝 Notes

- **Backend**: Your Python FastAPI backend needs to be deployed separately (Vercel supports Python, or use Railway, Render, etc.)
- **CORS**: Make sure your backend allows requests from your Vercel domain
- **Build**: The frontend will build automatically on each push to your main branch

