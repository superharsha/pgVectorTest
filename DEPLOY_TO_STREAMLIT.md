# 🚀 Ready to Deploy to Streamlit Cloud!

Everything is set up! Here's exactly what you need to do:

## ✅ What's Already Done:
- ✅ Service account created: `document-query-app@vpc-host-nonprod-kk186-dr143.iam.gserviceaccount.com`
- ✅ Permissions granted: `roles/run.invoker`
- ✅ Service account key generated and formatted
- ✅ All secrets prepared in `streamlit-cloud-secrets.toml`

## 🎯 Quick Deploy Steps:

### 1. Push to GitHub (if not done yet)
```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### 2. Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"New app"**
3. Connect your GitHub account
4. Select your repository: `pgVectorTest`
5. Set main file: `streamlitapp.py`
6. Click **"Deploy!"**

### 3. Configure Secrets
1. Go to your app's **Settings** → **Secrets** tab
2. **Copy the entire content from `streamlit-cloud-secrets.toml`**
3. **Paste it into the secrets editor**
4. Click **"Save"**

### 4. Test Your App
- Your app will automatically redeploy after saving secrets
- Test the "Check API Health" button
- Try a few example queries

## 📋 Secrets Summary:
Your secrets file contains:
- **API_BASE_URL**: Your Cloud Run endpoint
- **DEFAULT_TENANT_ID**: Your tenant ID
- **GCP_PROJECT_ID**: `vpc-host-nonprod-kk186-dr143`  
- **GOOGLE_APPLICATION_CREDENTIALS_JSON**: Full service account credentials

## 🔒 Security Notes:
- ✅ Service account key file cleaned up from local system
- ✅ Only necessary permissions granted (`run.invoker`)
- ✅ Secrets properly configured for Streamlit Cloud environment

## 🆘 If Something Goes Wrong:
1. Check Streamlit Cloud logs in the app settings
2. Verify all secrets are properly pasted (no extra spaces/characters)
3. Test API endpoints directly if needed:
   ```bash
   curl "https://document-query-engine-ia2czk4njq-uc.a.run.app/health"
   ```

**You're all set! Just copy-paste the secrets and deploy! 🎉** 