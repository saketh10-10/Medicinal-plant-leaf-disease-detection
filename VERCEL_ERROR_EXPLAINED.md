# Vercel NOT_FOUND Error: Complete Explanation

## 1. 🔧 The Fix

### What I Changed

**Created `vercel.json`** in the root directory:
```json
{
  "version": 2,
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

**Updated `frontend/src/services/api.ts`**:
```typescript
// Before:
const API_BASE_URL = 'http://localhost:8000';

// After:
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

### Why These Changes Fix the Error

1. **`buildCommand`**: Tells Vercel exactly how to build your app (it couldn't guess)
2. **`outputDirectory`**: Points Vercel to where Vite outputs the built files (`frontend/dist`)
3. **`rewrites`**: Ensures all routes serve `index.html` (required for React SPAs)
4. **Environment variable**: Allows different API URLs for dev/prod

---

## 2. 🔍 Root Cause Analysis

### What Was Actually Happening

When you deployed to Vercel without `vercel.json`:

1. **Vercel's Auto-Detection Failed**
   - Vercel tried to auto-detect your project type
   - It looked for common patterns (Next.js, Create React App, etc.)
   - Your project structure (Vite + React in `frontend/` subdirectory) didn't match common patterns
   - **Result**: Vercel didn't know where to find your build output

2. **Missing Build Configuration**
   - Vercel didn't know:
     - What command to run (`npm run build`? `npm run build:prod`?)
     - Where the build output would be (`dist/`? `build/`? `frontend/dist/`?)
   - **Result**: Either no build ran, or Vercel looked in the wrong place

3. **SPA Routing Issue**
   - Even if the build succeeded, direct navigation to routes like `/about` would fail
   - Browsers request `/about` from the server
   - Without rewrites, Vercel looks for a file at `/about/index.html` (doesn't exist)
   - **Result**: 404 NOT_FOUND error

4. **Hardcoded Localhost API**
   - Your frontend tried to call `http://localhost:8000` from the browser
   - In production, `localhost` refers to the user's computer, not your server
   - **Result**: API calls fail (though this doesn't cause NOT_FOUND, it breaks functionality)

### The Misconception

**You assumed**: "Vercel will automatically figure out my project structure"
**Reality**: Vercel's auto-detection works for standard setups, but custom structures (like a `frontend/` subdirectory) need explicit configuration

---

## 3. 📚 Understanding the Concepts

### Why Does This Error Exist?

**Vercel's NOT_FOUND error protects you from**:
- Serving broken or incomplete deployments
- Wasting resources on misconfigured builds
- Confusing users with broken routes

### The Mental Model

Think of Vercel deployment as a **3-step process**:

```
1. BUILD: Run your build command → Creates static files
2. LOCATE: Find the output directory → Where are the files?
3. SERVE: Serve files with routing rules → How to handle requests?
```

**Without `vercel.json`**, Vercel had to guess steps 1-3, and guessed wrong.

### How This Fits Into the Framework

**Vite's Build Process**:
- `npm run build` → Creates optimized files in `dist/`
- These are static HTML/CSS/JS files
- No server-side rendering (SSR) by default

**Vercel's Role**:
- Hosts these static files
- Provides CDN (fast global delivery)
- Handles routing (which file to serve for each URL)

**The Connection**:
- Vite outputs to `frontend/dist/` (because you're in a subdirectory)
- Vercel needs to know this location
- Without configuration, Vercel looks in the root `dist/` → NOT_FOUND

### SPA Routing Explained

**Single Page Applications (SPAs)** work like this:

```
User visits: https://yourapp.com/about
Browser requests: GET /about
Server needs to: Return index.html (not /about/index.html)
React Router then: Handles /about route client-side
```

**Why?** Because:
- All routes are handled by JavaScript (React Router)
- There's only ONE HTML file (`index.html`)
- The server must serve `index.html` for ALL routes
- Then React Router takes over and shows the right component

**The `rewrites` rule does exactly this**:
```json
{
  "source": "/(.*)",        // Match any route
  "destination": "/index.html"  // Serve index.html
}
```

---

## 4. ⚠️ Warning Signs to Watch For

### Red Flags That Indicate This Issue

1. **Project Structure**
   - ✅ **Safe**: `package.json` in root, build outputs in root
   - ⚠️ **Warning**: Build tool in subdirectory (`frontend/`, `client/`, `app/`)
   - **Action**: Always create `vercel.json` for non-standard structures

2. **Build Output Location**
   - ✅ **Safe**: Standard locations (`dist/`, `build/`, `.next/`)
   - ⚠️ **Warning**: Custom output directory or nested structure
   - **Action**: Explicitly set `outputDirectory` in `vercel.json`

3. **SPA Routing**
   - ✅ **Safe**: Using Next.js (handles routing automatically)
   - ⚠️ **Warning**: Using React Router, Vue Router, or client-side routing
   - **Action**: Always include `rewrites` for SPAs

4. **Environment-Specific URLs**
   - ✅ **Safe**: Using environment variables from the start
   - ⚠️ **Warning**: Hardcoded `localhost`, `127.0.0.1`, or absolute URLs
   - **Action**: Use `import.meta.env` (Vite) or `process.env` (others)

### Similar Mistakes You Might Make

1. **Forgetting to Build Before Deploy**
   - Symptom: Old code appears in production
   - Fix: Ensure `buildCommand` is correct

2. **Wrong Output Directory**
   - Symptom: "Build succeeded but site is blank"
   - Fix: Verify `outputDirectory` matches your build tool's output

3. **Missing Environment Variables**
   - Symptom: "API calls fail in production"
   - Fix: Set environment variables in Vercel dashboard

4. **CORS Issues**
   - Symptom: "API works locally but fails in production"
   - Fix: Configure backend to allow your Vercel domain

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
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/dist"
}
```

---

## 5. 🔄 Alternative Approaches

### Option 1: Monorepo Structure (Current)
**What you have**: Frontend and backend in separate directories
```json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/dist"
}
```
**Pros**: Clear separation, easy to manage
**Cons**: Requires explicit configuration

### Option 2: Root-Level Frontend
**Move frontend files to root**:
```
PLANT/
├── src/          (frontend code)
├── package.json
└── vite.config.ts
```
**Pros**: Vercel auto-detects easier
**Cons**: Less organized, harder to separate concerns

### Option 3: Multiple Vercel Projects
**Deploy frontend and backend separately**:
- Frontend project: Points to `frontend/`
- Backend project: Points to `backend/` (if using Vercel serverless)
**Pros**: Independent scaling, separate domains
**Cons**: More complex setup, CORS configuration needed

### Option 4: Vercel with Backend Functions
**Use Vercel Serverless Functions**:
```javascript
// api/analyze.js (in your frontend project)
export default async function handler(req, res) {
  // Your backend logic here
}
```
**Pros**: Everything in one deployment
**Cons**: Requires rewriting backend code, Python support is limited

### Option 5: Docker + Vercel
**Containerize your app**:
- Use Vercel's Docker support
- Deploy full-stack app as container
**Pros**: Works for complex setups
**Cons**: More expensive, overkill for simple apps

### Recommended Approach

**For your current setup**: **Option 1** (what we implemented) is best because:
- ✅ Maintains clean separation
- ✅ Works with your existing structure
- ✅ Easy to understand and maintain
- ✅ Allows independent backend deployment

---

## 🎓 Key Takeaways

1. **Always configure explicitly** for non-standard project structures
2. **SPAs need rewrites** to handle client-side routing
3. **Never hardcode localhost** - use environment variables
4. **Test your build locally** before deploying (`npm run build`)
5. **Check Vercel build logs** if something goes wrong

---

## 📖 Further Reading

- [Vercel Configuration Reference](https://vercel.com/docs/configuration)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [SPA Routing on Vercel](https://vercel.com/docs/configuration#routes)
- [Vercel Build Outputs](https://vercel.com/docs/build-outputs)

