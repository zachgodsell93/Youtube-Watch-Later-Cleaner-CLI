# Detailed Setup Instructions

This guide will walk you through setting up the YouTube Watch Later Cleaner from scratch.

## Prerequisites

- Python 3.7 or higher installed on your system
- A Google account
- Basic familiarity with command line/terminal

## Step 1: Set Up Google Cloud Project

### 1.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click on the project dropdown at the top of the page
4. Click "New Project"
5. Enter a project name (e.g., "YouTube Watch Later Cleaner")
6. Click "Create"
7. Wait for the project to be created (you'll see a notification)

### 1.2 Enable YouTube Data API v3

1. Make sure your new project is selected in the project dropdown
2. In the left sidebar, go to "APIs & Services" > "Library"
3. In the search bar, type "YouTube Data API v3"
4. Click on "YouTube Data API v3" in the results
5. Click the "Enable" button
6. Wait for the API to be enabled

### 1.3 Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Select "External" as the user type
3. Click "Create"
4. Fill in the required fields:
   - **App name**: YouTube Watch Later Cleaner
   - **User support email**: Your email address
   - **Developer contact information**: Your email address
5. Click "Save and Continue"
6. On the "Scopes" page, click "Add or Remove Scopes"
7. Filter for YouTube and add the scope: `https://www.googleapis.com/auth/youtube`
8. Click "Update" then "Save and Continue"
9. On "Test users" page, click "Add Users"
10. Add your Google email address
11. Click "Save and Continue"
12. Review and click "Back to Dashboard"

### 1.4 Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" at the top
3. Select "OAuth client ID"
4. For "Application type", select "Desktop app"
5. Enter a name (e.g., "YouTube Cleaner Desktop Client")
6. Click "Create"
7. You'll see a dialog with your client ID and secret
8. Click "Download JSON"
9. Save the downloaded file

## Step 2: Set Up the Python Project

### 2.1 Install Python Dependencies

```bash
# Navigate to the project directory
cd Youtube-Watch-Later-Cleaner

# Create a virtual environment (recommended)
python3 -m venv env

# Activate the virtual environment
# On macOS/Linux:
source env/bin/activate
# On Windows:
env\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2.2 Add Your Credentials

1. Locate the JSON file you downloaded in step 1.4
2. Rename it to `client_secrets.json`
3. Move it to the project directory (same folder as `youtube_cleaner.py`)

Your directory should now look like this:
```
Youtube-Watch-Later-Cleaner/
├── client_secrets.json         (your credentials - do not commit!)
├── client_secrets.json.example (example format)
├── config.py                   (configuration settings)
├── youtube_cleaner.py          (main script)
├── requirements.txt
├── README.md
├── SETUP.md
└── env/                        (virtual environment)
```

## Step 3: First Run and Authentication

### 3.1 Run the Script in Dry-Run Mode

```bash
python youtube_cleaner.py --threshold 50 --dry-run
```

### 3.2 Complete OAuth Authentication

1. The script will automatically open your web browser
2. If it doesn't open automatically, copy the URL from the terminal and paste it in your browser
3. Sign in to your Google account (if not already signed in)
4. You'll see a warning "Google hasn't verified this app"
   - Click "Advanced"
   - Click "Go to YouTube Watch Later Cleaner (unsafe)"
   - This is safe - it's your own app!
5. Review the permissions requested
6. Click "Allow"
7. You should see "The authentication flow has completed"
8. Return to your terminal

### 3.3 Verify Authentication

The script will:
- Save your authentication token to `token.pickle`
- Connect to the YouTube API
- List videos in your Watch Later playlist
- Show what would be removed (in dry-run mode)

## Step 4: Using the Script

### Test with Dry Run First

Always test with dry-run mode first:

```bash
# Preview what would be removed with 50% threshold
python youtube_cleaner.py --threshold 50 --dry-run

# Preview with 75% threshold
python youtube_cleaner.py --threshold 75 --dry-run
```

### Execute the Cleaning

Once you're satisfied with the preview:

```bash
# Actually remove videos
python youtube_cleaner.py --threshold 50 --execute
```

## Troubleshooting

### "Credentials file not found" Error

- Make sure `client_secrets.json` is in the project directory
- Check that the filename is exactly `client_secrets.json`
- Verify the file contains valid JSON

### "Access Not Configured" Error

- Make sure you enabled the YouTube Data API v3 in Google Cloud Console
- Wait a few minutes and try again (changes can take time to propagate)

### "Invalid Grant" Error

- Delete `token.pickle` file
- Run the script again to re-authenticate

### Browser Doesn't Open for Authentication

- Copy the URL from the terminal
- Paste it into your web browser manually
- Complete the authentication flow

### "Insufficient Permission" Error

- Make sure you added the YouTube scope in the OAuth consent screen
- Delete `token.pickle` and re-authenticate

## Important Notes

### API Quota Limits

YouTube Data API v3 has quota limits:
- 10,000 units per day by default
- Reading playlist items costs 1 unit per request
- Deleting items costs 50 units per deletion

For a large Watch Later playlist, you may need to:
- Request a quota increase from Google
- Or run the script over multiple days

### Watch History Limitation

The current implementation has a known limitation: the YouTube Data API v3 doesn't easily provide watch percentage data.

To implement full watch percentage tracking, you'll need to:

1. **Use YouTube Analytics API** (more complex setup)
2. **Export your watch history** from Google Takeout and parse it
3. **Build custom tracking** using browser extensions or other methods

The script structure is ready - you just need to implement one of these data sources.

## Security Best Practices

1. **Never share your `client_secrets.json` file**
2. **Never commit `client_secrets.json` or `token.pickle` to version control**
3. **Keep your OAuth credentials private**
4. **Regularly review authorized applications** in your Google Account settings

## Getting Help

If you encounter issues:

1. Check the error message carefully
2. Review this setup guide
3. Check the main README.md
4. Verify your Google Cloud Console settings
5. Try deleting `token.pickle` and re-authenticating

## Next Steps

Once everything is working:

1. Consider scheduling the script to run automatically (e.g., using cron on Linux/macOS)
2. Implement actual watch percentage tracking (see README.md)
3. Customize thresholds and settings in `config.py`
4. Add additional features as needed

Enjoy your cleaner Watch Later playlist!
