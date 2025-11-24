# Streamlit Cloud Deployment Guide

This guide will help you deploy the frontend application to Streamlit Cloud.

## Prerequisites

1. ✅ Code pushed to GitHub (already done)
2. ✅ GitHub account
3. ✅ Streamlit Cloud account (free)

## Step-by-Step Deployment

### Step 1: Sign Up for Streamlit Cloud

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Click **"Sign up"** or **"Get started"**
3. Sign in with your **GitHub account**
4. Authorize Streamlit Cloud to access your GitHub repositories

### Step 2: Create New App

1. Once logged in, click **"New app"** button (top right)
2. You'll see a form to configure your app

### Step 3: Configure Your App

Fill in the deployment form:

**Repository:**
- Select: `SharmilNK/Data-ML-Engineering` (or your repository name)

**Branch:**
- Select: `main` (or `yifei` if you want to deploy from your branch)
- **Note:** After merging your PR, use `main` branch

**Main file path:**
- Enter: `frontend/app_ui.py`
- This tells Streamlit Cloud which file to run

**Python version:**
- Select: `3.11` (or `3.10` if 3.11 is not available)
- This should match your local Python version

**Advanced settings (optional):**
- You can leave these as default
- Streamlit Cloud will automatically use `requirements.txt` from the project root

### Step 4: Deploy

1. Click **"Deploy"** button
2. Streamlit Cloud will:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start your Streamlit app
   - Provide you with a public URL

### Step 5: Get Your App URL

After deployment (usually takes 1-2 minutes), you'll see:
- **App URL:** `https://your-app-name.streamlit.app`
- Copy this URL

### Step 6: Update README

1. Update the README.md file:
   - Replace the placeholder link with your actual Streamlit Cloud URL
   - Add it to the "Live Frontend Application" section

2. Commit and push:
   ```bash
   git add README.md
   git commit -m "Add Streamlit Cloud deployment link"
   git push origin yifei
   ```

## Troubleshooting

### Issue: App fails to deploy

**Possible causes:**
1. **Wrong file path:** Make sure `frontend/app_ui.py` is correct
2. **Missing dependencies:** Check that `requirements.txt` includes `streamlit` and `requests`
3. **Python version mismatch:** Try a different Python version
4. **Import errors:** Check that all imports in `app_ui.py` are available

**Solution:**
- Check the deployment logs in Streamlit Cloud dashboard
- Look for error messages
- Fix issues and redeploy

### Issue: API connection fails

**Possible causes:**
1. **API URL incorrect:** Check the API URL in the sidebar
2. **API not accessible:** Make sure your Cloud Run API is publicly accessible
3. **CORS issues:** Streamlit Cloud apps can call external APIs without CORS issues

**Solution:**
- Verify API URL: `https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app`
- Test API health: `curl https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app/health`

### Issue: App works locally but not on Streamlit Cloud

**Possible causes:**
1. **File paths:** Streamlit Cloud runs from project root
2. **Environment variables:** Not needed for this app
3. **Dependencies:** Some packages might not be available

**Solution:**
- Make sure all file paths are relative to project root
- Check `requirements.txt` includes all dependencies
- Review Streamlit Cloud logs

## Updating Your App

After making changes:

1. **Commit and push to GitHub:**
   ```bash
   git add frontend/app_ui.py
   git commit -m "Update frontend"
   git push origin yifei
   ```

2. **Streamlit Cloud will automatically redeploy:**
   - Go to your app dashboard
   - Click "⋮" (three dots) → "Redeploy"
   - Or wait for automatic redeployment (usually within minutes)

## Best Practices

1. **Use main branch for production:** Deploy from `main` branch after merging PRs
2. **Test locally first:** Always test changes locally before deploying
3. **Monitor logs:** Check Streamlit Cloud logs if something goes wrong
4. **Keep requirements.txt updated:** Add new dependencies as needed

## Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Cloud Community Forum](https://discuss.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)

