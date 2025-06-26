# Document Query Engine - Streamlit App

A Streamlit web application for querying documents using a vector search engine powered by GCP Cloud Run.

## Features

- 🔍 Document query interface with vector search
- 🏥 API health monitoring
- 📊 Query statistics and performance metrics
- 🔒 Multi-tenant support with secure tenant isolation
- 💡 Example questions for quick testing
- 📚 Source document display with metadata

## Deployment to Streamlit Cloud

### Prerequisites

1. A GitHub repository with this code
2. A Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
3. GCP project access (if authentication is required)

### Step 1: Prepare GCP Authentication (Optional)

If your API requires authentication, you'll need a GCP service account:

```bash
# Login to GCP
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Create a service account (if you don't have one)
gcloud iam service-accounts create document-query-app \
    --description="Service account for Document Query Streamlit App" \
    --display-name="Document Query App"

# Create and download the service account key
gcloud iam service-accounts keys create ~/document-query-key.json \
    --iam-account=document-query-app@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Grant necessary permissions (adjust as needed)
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:document-query-app@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.invoker"
```

### Step 2: Deploy to Streamlit Cloud

1. **Push to GitHub**: Make sure your code is in a GitHub repository

2. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)

3. **Create New App**:
   - Click "New app"
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `streamlitapp.py`
   - Click "Deploy!"

### Step 3: Configure Environment Variables

In your Streamlit Cloud app settings, add these secrets:

#### Required Environment Variables:
```toml
# API Configuration
API_BASE_URL = "https://document-query-engine-ia2czk4njq-uc.a.run.app"
DEFAULT_TENANT_ID = "d572f04c-0ce5-48c5-a644-b88b8f369936"
```

#### Optional (if authentication required):
```toml
# GCP Project ID
GCP_PROJECT_ID = "your-gcp-project-id"

# Service Account Key (paste the entire JSON content)
GOOGLE_APPLICATION_CREDENTIALS_JSON = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
'''
```

### Step 4: Configure Secrets in Streamlit Cloud

1. Go to your app's settings in Streamlit Cloud
2. Click on "Secrets" tab
3. Paste your configuration in TOML format:

```toml
API_BASE_URL = "https://document-query-engine-ia2czk4njq-uc.a.run.app"
DEFAULT_TENANT_ID = "d572f04c-0ce5-48c5-a644-b88b8f369936"

# Add GCP credentials only if needed
GCP_PROJECT_ID = "your-project-id"
GOOGLE_APPLICATION_CREDENTIALS_JSON = '''
{
  "type": "service_account",
  ...
}
'''
```

4. Click "Save"

### Step 5: Test the Deployment

1. Your app should automatically redeploy after saving secrets
2. Test the API health check to ensure connectivity
3. Try a few example queries to verify everything works

## Local Development

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd pgVectorTest

# Install dependencies
pip install -r requirements.txt

# Copy the secrets template
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit .streamlit/secrets.toml with your actual values
# (DO NOT commit this file to version control)
```

### Run Locally

```bash
streamlit run streamlitapp.py
```

## File Structure

```
pgVectorTest/
├── streamlitapp.py              # Main Streamlit application
├── requirements.txt             # Python dependencies
├── README.md                   # This file
├── .streamlit/
│   └── secrets.toml.example    # Template for secrets configuration
└── .git/                       # Git repository
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**:
   - Check if your API_BASE_URL is correct
   - Verify network connectivity
   - Check if authentication is required

2. **Authentication Errors**:
   - Verify your service account key is valid
   - Check that the service account has necessary permissions
   - Ensure the JSON is properly formatted in secrets

3. **Deployment Errors**:
   - Check that all required dependencies are in requirements.txt
   - Verify your secrets are properly configured in Streamlit Cloud
   - Check the app logs in Streamlit Cloud for detailed error messages

### Getting Help

- Check Streamlit Cloud logs for detailed error messages
- Verify your GCP service account permissions
- Test API endpoints directly using curl or Postman

## Security Notes

- Never commit secrets.toml to version control
- Use environment variables for all sensitive data
- Regularly rotate service account keys
- Monitor API usage and access logs 