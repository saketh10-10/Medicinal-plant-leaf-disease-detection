# Vercel NOT_FOUND Error: Complete Resolution Guide

> **Official Documentation**: [Vercel NOT_FOUND Error Docs](https://vercel.com/docs/errors/NOT_FOUND)  
> **Error Code**: `404` | **Name**: Not Found

## 📋 Official Vercel Troubleshooting Steps

According to [Vercel's official documentation](https://vercel.com/docs/errors/NOT_FOUND), follow these steps first:

1. **Check the deployment URL**: Ensure the deployment URL is correct and doesn't contain typos or incorrect paths
2. **Check deployment existence**: Verify the [deployment exists](https://vercel.com/docs/projects/project-dashboard#deployments) and hasn't been deleted
3. **Review deployment logs**: If the deployment exists, review the [deployment logs](https://vercel.com/docs/deployments/logs) to identify issues
4. **Verify permissions**: Ensure you have the necessary [permissions](https://vercel.com/docs/accounts/team-members-and-roles) to access the deployment
5. **Contact support**: If the above don't resolve it, [contact support](https://vercel.com/help#issues)

---

**This guide focuses on the most common cause**: Configuration issues with build commands, output directories, and SPA routing. If the official troubleshooting steps don't resolve your issue, the fixes below likely will.

---

## 1. 🔧 The Fix

### What I Changed

**Updated `vercel.json`** in the root directory:
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

**Key Change**: Replaced `npm install` with `npm ci` in the build command.

### Why This Fixes the Error

1. **`npm ci` vs `npm install`**:
   - `npm ci` is designed for automated environments (CI/CD, Vercel)
   - It installs dependencies exactly as specified in `package-lock.json`
   - It's faster and more reliable than `npm install`
   - It fails if `package-lock.json` is out of sync (prevents inconsistent builds)
   - **Result**: More reliable, reproducible builds

2. **`buildCommand`**: Tells Vercel exactly how to build your app
   - Without this, Vercel might try to auto-detect and fail
   - The `cd frontend` ensures we're in the right directory

3. **`outputDirectory`**: Points Vercel to where Vite outputs the built files
   - Vite outputs to `dist/` by default
   - Since your frontend is in `frontend/`, the output is `frontend/dist/`
   - Without this, Vercel looks in the wrong place → NOT_FOUND

4. **`rewrites`**: Ensures all routes serve `index.html` (required for React SPAs)
   - When users visit `/about`, Vercel serves `index.html`
   - React Router then handles the routing client-side
   - Without this, direct navigation to routes fails → NOT_FOUND

---

## 2. 🔍 Root Cause Analysis

> **Note**: NOT_FOUND errors can have multiple causes. This guide focuses on **configuration-related issues**, which are the most common for custom project structures. Other causes include: deleted deployments, incorrect URLs, permission issues, or deployment failures. Always check [Vercel's official troubleshooting steps](#-official-vercel-troubleshooting-steps) first.

### What Was Actually Happening

When you deployed to Vercel, here's the sequence of events that led to NOT_FOUND:

#### Scenario 1: Build Command Issues
1. **Vercel's Auto-Detection Failed**
   - Vercel tried to auto-detect your project type
   - It looked for common patterns:
     - `package.json` in root → Found ✅
     - Standard build scripts → Found ✅
     - But your frontend is in `frontend/` subdirectory → Confusion ❌
   - **Result**: Vercel might have tried to build from root, not `frontend/`

2. **Inconsistent Dependency Installation**
   - `npm install` can behave differently in CI vs local
   - If `package-lock.json` was out of sync, dependencies might not install correctly
   - **Result**: Build fails silently or produces incomplete output

3. **Missing Build Output**
   - Even if build ran, Vercel didn't know where to look for output
   - It might have looked in `dist/` (root) instead of `frontend/dist/`
   - **Result**: Vercel finds no files → NOT_FOUND

#### Scenario 2: SPA Routing Issues
1. **Direct Navigation Failure**
   - User visits: `https://yourapp.vercel.app/about`
   - Browser requests: `GET /about` from Vercel's server
   - Without rewrites, Vercel looks for: `/about/index.html` (doesn't exist)
   - **Result**: 404 NOT_FOUND

2. **Why This Happens**
   - SPAs have only ONE HTML file: `index.html`
   - All routing is handled by JavaScript (React Router)
   - The server must serve `index.html` for ALL routes
   - Then React Router takes over and shows the right component

### The Misconception

**You assumed**: "Vercel will automatically figure out my project structure"
**Reality**: 
- Vercel's auto-detection works for **standard** setups (Next.js, Create React App in root)
- Your project has a **custom structure** (Vite + React in `frontend/` subdirectory)
- Custom structures need **explicit configuration** via `vercel.json`

**You assumed**: "`npm install` works the same everywhere"
**Reality**:
- `npm install` can install different versions if `package-lock.json` is outdated
- In CI/CD, `npm ci` is the standard for reproducible builds
- Vercel's build environment is different from your local machine

### What Conditions Triggered This Error

1. **Non-standard project structure**: Frontend in subdirectory
2. **Missing explicit configuration**: No `vercel.json` (or incomplete one)
3. **SPA routing**: Client-side routing without server-side rewrites
4. **Build inconsistency**: Using `npm install` instead of `npm ci` in CI

---

## 3. 📚 Understanding the Concepts

### Why Does This Error Exist?

**Vercel's NOT_FOUND error protects you from**:
- Serving broken or incomplete deployments
- Wasting resources on misconfigured builds
- Confusing users with broken routes
- Security issues (serving wrong files)

It's a **safety mechanism** that says: "I can't find what you're asking for, so I won't serve anything rather than serve the wrong thing."

### The Mental Model

Think of Vercel deployment as a **4-step process**:

```
1. INSTALL: Install dependencies (npm ci)
   ↓
2. BUILD: Run your build command (npm run build)
   ↓
3. LOCATE: Find the output directory (frontend/dist)
   ↓
4. SERVE: Serve files with routing rules (rewrites)
```

**Without proper configuration**, Vercel had to guess steps 1-4, and guessed wrong.

### How This Fits Into the Framework

#### Vite's Build Process
```
npm run build
  ↓
TypeScript compilation (tsc -b)
  ↓
Vite bundling and optimization
  ↓
Output: frontend/dist/
  ├── index.html
  ├── assets/
  │   ├── index-[hash].js
  │   └── index-[hash].css
  └── ...
```

**Key Points**:
- Vite creates **static files** (HTML, CSS, JS)
- No server-side rendering (SSR) by default
- All routes are handled client-side
- Only ONE HTML file exists (`index.html`)

#### Vercel's Role
- **Hosts** these static files
- **Provides CDN** (fast global delivery)
- **Handles routing** (which file to serve for each URL)
- **Applies rewrites** (SPA routing rules)

#### The Connection
```
Your Structure:          Vercel Needs:
frontend/               buildCommand: "cd frontend && npm ci && npm run build"
  ├── src/              outputDirectory: "frontend/dist"
  ├── package.json      rewrites: [all routes → index.html]
  └── dist/ (output)    
```

### SPA Routing Explained

**Single Page Applications (SPAs)** work like this:

```
User visits: https://yourapp.com/about
  ↓
Browser requests: GET /about
  ↓
Server (Vercel) checks: Does /about/index.html exist? NO
  ↓
WITHOUT rewrites: Returns 404 NOT_FOUND ❌
  ↓
WITH rewrites: Returns /index.html ✅
  ↓
Browser loads index.html
  ↓
React Router reads URL (/about)
  ↓
React Router shows <About /> component
  ↓
User sees the About page ✅
```

**Why rewrites are necessary**:
- All routes are handled by JavaScript (React Router)
- There's only ONE HTML file (`index.html`)
- The server must serve `index.html` for ALL routes
- Then React Router takes over and shows the right component

**The `rewrites` rule does exactly this**:
```json
{
  "source": "/(.*)",              // Match any route
  "destination": "/index.html"    // Serve index.html
}
```

### npm ci vs npm install

**`npm install`**:
- Updates `package-lock.json` if needed
- Can install different versions if lock file is outdated
- Slower (checks for updates)
- Good for **local development**

**`npm ci`** (Clean Install):
- Installs **exactly** as specified in `package-lock.json`
- **Fails** if `package-lock.json` is out of sync
- Faster (no version resolution)
- **Designed for CI/CD** (Vercel, GitHub Actions, etc.)
- More reliable for automated builds

**Why use `npm ci` in Vercel**:
- Ensures consistent builds across environments
- Prevents "works on my machine" issues
- Faster build times
- Industry standard for CI/CD

---

## 4. ⚠️ Warning Signs to Watch For

### Red Flags That Indicate This Issue

#### 1. Project Structure
```
✅ SAFE:                    ⚠️ WARNING:
package.json in root        Build tool in subdirectory
build outputs in root       (frontend/, client/, app/)
Standard locations          Custom output directory
(dist/, build/, .next/)     (custom-dist/, output/)
```

**Action**: Always create `vercel.json` for non-standard structures

#### 2. Build Output Location
```
✅ SAFE:                    ⚠️ WARNING:
Standard locations          Custom output directory
(dist/, build/, .next/)     Nested structure
                            (frontend/dist/, app/build/)
```

**Action**: Explicitly set `outputDirectory` in `vercel.json`

#### 3. SPA Routing
```
✅ SAFE:                    ⚠️ WARNING:
Using Next.js              Using React Router
(handles routing            Vue Router
 automatically)             Client-side routing
```

**Action**: Always include `rewrites` for SPAs

#### 4. Environment-Specific URLs
```typescript
✅ SAFE:                    ⚠️ WARNING:
const API_URL =             const API_URL =
  import.meta.env             'http://localhost:8000';
  .VITE_API_BASE_URL ||      const API_URL =
  'http://localhost:8000';     'http://127.0.0.1:8000';
```

**Action**: Use environment variables from the start

### Similar Mistakes You Might Make

#### 1. Forgetting to Build Before Deploy
**Symptom**: Old code appears in production
**Fix**: Ensure `buildCommand` is correct and runs successfully
**Check**: Look at Vercel build logs

#### 2. Wrong Output Directory
**Symptom**: "Build succeeded but site is blank"
**Fix**: Verify `outputDirectory` matches your build tool's output
**Check**: Run `npm run build` locally and see where files are created

#### 3. Missing Environment Variables
**Symptom**: "API calls fail in production"
**Fix**: Set environment variables in Vercel dashboard
**Check**: Vercel project settings → Environment Variables

#### 4. CORS Issues
**Symptom**: "API works locally but fails in production"
**Fix**: Configure backend to allow your Vercel domain
**Check**: Backend CORS configuration

#### 5. TypeScript Errors
**Symptom**: "Build fails with TypeScript errors"
**Fix**: Fix TypeScript errors or adjust `tsconfig.json`
**Check**: Run `tsc` locally before deploying

### Code Smells

```typescript
// ❌ BAD: Hardcoded localhost
const API_URL = 'http://localhost:8000';

// ✅ GOOD: Environment variable
const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

```json
// ❌ BAD: No vercel.json for custom structure
// (Relies on auto-detection)

// ✅ GOOD: Explicit configuration
{
  "buildCommand": "cd frontend && npm ci && npm run build",
  "outputDirectory": "frontend/dist"
}
```

```json
// ❌ BAD: Using npm install in CI
"buildCommand": "cd frontend && npm install && npm run build"

// ✅ GOOD: Using npm ci in CI
"buildCommand": "cd frontend && npm ci && npm run build"
```

### Pre-Deployment Checklist

Before deploying to Vercel, verify:

- [ ] `vercel.json` exists and is correctly configured
- [ ] `buildCommand` matches your local build process
- [ ] `outputDirectory` matches where your build tool outputs files
- [ ] `rewrites` are configured for SPAs (if using client-side routing)
- [ ] Environment variables are set in Vercel dashboard
- [ ] Build succeeds locally (`npm run build`)
- [ ] No TypeScript errors (`tsc` or `npm run build`)
- [ ] `package-lock.json` is committed and up to date
- [ ] API URLs use environment variables (not hardcoded localhost)

---

## 5. 🔄 Alternative Approaches

### Option 1: Monorepo Structure (Current - Recommended)
**What you have**: Frontend and backend in separate directories
```json
{
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

**Pros**:
- ✅ Clear separation of concerns
- ✅ Easy to manage
- ✅ Independent deployment of frontend/backend
- ✅ Scales well for larger projects

**Cons**:
- ⚠️ Requires explicit configuration
- ⚠️ Slightly more complex setup

**Best for**: Projects with separate frontend/backend, team projects

---

### Option 2: Root-Level Frontend
**Move frontend files to root**:
```
PLANT/
├── src/          (frontend code)
├── package.json
├── vite.config.ts
└── dist/         (build output)
```

**Pros**:
- ✅ Vercel auto-detects easier
- ✅ Simpler configuration
- ✅ Standard structure

**Cons**:
- ⚠️ Less organized
- ⚠️ Harder to separate concerns
- ⚠️ Mixes frontend/backend files

**Best for**: Simple projects, solo developers

---

### Option 3: Multiple Vercel Projects
**Deploy frontend and backend separately**:
- Frontend project: Points to `frontend/` directory
- Backend project: Points to `backend/` directory (if using Vercel serverless)

**Pros**:
- ✅ Independent scaling
- ✅ Separate domains
- ✅ Independent deployments
- ✅ Better for microservices

**Cons**:
- ⚠️ More complex setup
- ⚠️ CORS configuration needed
- ⚠️ More projects to manage

**Best for**: Large projects, microservices architecture

---

### Option 4: Vercel with Backend Functions
**Use Vercel Serverless Functions**:
```javascript
// api/analyze.js (in your frontend project)
export default async function handler(req, res) {
  // Your backend logic here
  // Can call Python via subprocess or external API
}
```

**Pros**:
- ✅ Everything in one deployment
- ✅ No CORS issues
- ✅ Unified project

**Cons**:
- ⚠️ Requires rewriting backend code
- ⚠️ Python support is limited (Node.js preferred)
- ⚠️ Cold start latency
- ⚠️ Function size limits

**Best for**: Node.js backends, small APIs

---

### Option 5: Docker + Vercel
**Containerize your app**:
- Use Vercel's Docker support
- Deploy full-stack app as container

**Pros**:
- ✅ Works for complex setups
- ✅ Full control over environment
- ✅ Can run any language/runtime

**Cons**:
- ⚠️ More expensive
- ⚠️ Overkill for simple apps
- ⚠️ Slower deployments
- ⚠️ More complex configuration

**Best for**: Complex applications, specific runtime requirements

---

### Option 6: Separate Backend Deployment
**Current approach** (what you likely have):
- Frontend: Deployed to Vercel
- Backend: Deployed separately (Railway, Render, AWS, etc.)

**Pros**:
- ✅ Use best tool for each part
- ✅ Python backend can use full features
- ✅ Independent scaling
- ✅ No language restrictions

**Cons**:
- ⚠️ CORS configuration needed
- ⚠️ Two deployments to manage
- ⚠️ Environment variable management

**Best for**: Python backends, existing backend infrastructure

---

### Recommended Approach

**For your current setup**: **Option 1** (what we implemented) is best because:

- ✅ Maintains clean separation
- ✅ Works with your existing structure
- ✅ Easy to understand and maintain
- ✅ Allows independent backend deployment
- ✅ Scales well as project grows

**If you want to simplify**: Consider **Option 2** (root-level frontend) if:
- You're a solo developer
- Project is small
- You don't need strict separation

---

## 🎓 Key Takeaways

1. **Always configure explicitly** for non-standard project structures
2. **SPAs need rewrites** to handle client-side routing
3. **Never hardcode localhost** - use environment variables
4. **Use `npm ci` in CI/CD** - more reliable than `npm install`
5. **Test your build locally** before deploying (`npm run build`)
6. **Check Vercel build logs** if something goes wrong
7. **Verify output directory** matches your build tool's output
8. **Set environment variables** in Vercel dashboard before deploying

---

## 🔍 Debugging Steps

If you still encounter NOT_FOUND after applying the fix, follow Vercel's official troubleshooting steps first, then try these:

### Step 0: Follow Official Troubleshooting
1. ✅ Verify deployment URL is correct
2. ✅ Check deployment exists in Vercel dashboard
3. ✅ Review deployment logs for errors
4. ✅ Verify you have access permissions

### Additional Debugging:

### 1. Check Build Logs
- Go to Vercel dashboard → Your project → Deployments
- Click on the failed deployment
- Check "Build Logs" tab
- Look for errors in the build process

### 2. Verify Build Output
```bash
# Locally, run:
cd frontend
npm ci
npm run build

# Check if dist/ directory exists and has files
ls -la dist/
```

### 3. Test Build Command
```bash
# Test the exact command Vercel will run:
cd frontend && npm ci && npm run build
```

### 4. Check Output Directory
- Verify `frontend/dist/` exists after build
- Verify it contains `index.html`
- Check `vercel.json` has correct `outputDirectory`

### 5. Verify Rewrites
- Try accessing a route directly (e.g., `/about`)
- Should serve `index.html`, not 404
- Check `vercel.json` has `rewrites` configured

### 6. Check Environment Variables
- Vercel dashboard → Settings → Environment Variables
- Ensure `VITE_API_BASE_URL` is set (if needed)
- Ensure it's set for correct environments (Production, Preview, Development)

---

## 📖 Further Reading

- **[Vercel NOT_FOUND Error Docs](https://vercel.com/docs/errors/NOT_FOUND)** - Official Vercel documentation
- [Vercel Configuration Reference](https://vercel.com/docs/configuration)
- [Vercel Build Outputs](https://vercel.com/docs/build-outputs)
- [Vercel Deployment Logs](https://vercel.com/docs/deployments/logs)
- [Vercel Project Dashboard](https://vercel.com/docs/projects/project-dashboard)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [SPA Routing on Vercel](https://vercel.com/docs/configuration#routes)
- [npm ci documentation](https://docs.npmjs.com/cli/v8/commands/npm-ci)

---

## ✅ Summary

The NOT_FOUND error was caused by:
1. **Missing/incomplete `vercel.json`** - Vercel couldn't find build output
2. **Using `npm install` instead of `npm ci`** - Inconsistent builds
3. **Missing SPA rewrites** - Direct navigation to routes failed

**The fix**:
- Created/updated `vercel.json` with explicit configuration
- Changed to `npm ci` for reliable builds
- Added rewrites for SPA routing

**Result**: Your app should now deploy successfully to Vercel! 🎉

