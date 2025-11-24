# TODO - Setup and Implementation Checklist

## Initial Setup

### 1. Set Up Google Cloud Project

- [ ] Go to [Google Cloud Console](https://console.cloud.google.com/)
- [ ] Create a new project (e.g., "YouTube Watch Later Cleaner")
- [ ] Enable YouTube Data API v3
  - [ ] Navigate to "APIs & Services" > "Library"
  - [ ] Search for "YouTube Data API v3"
  - [ ] Click "Enable"

### 2. Configure OAuth Consent Screen

- [ ] Go to "APIs & Services" > "OAuth consent screen"
- [ ] Select "External" user type
- [ ] Fill in required fields (app name, email, etc.)
- [ ] Add scope: `https://www.googleapis.com/auth/youtube`
- [ ] Add yourself as a test user

### 3. Create OAuth 2.0 Credentials

- [ ] Go to "APIs & Services" > "Credentials"
- [ ] Click "Create Credentials" > "OAuth client ID"
- [ ] Select "Desktop app" as application type
- [ ] Download the credentials JSON file
- [ ] Rename the file to `client_secrets.json`
- [ ] Move `client_secrets.json` to the project directory

### 4. Install Python Dependencies

- [ ] Create virtual environment: `python3 -m venv env`
- [ ] Activate virtual environment:
  - macOS/Linux: `source env/bin/activate`
  - Windows: `env\Scripts\activate`
- [ ] Install dependencies: `pip install -r requirements.txt`

### 5. First Run and Authentication

- [ ] Run the script in dry-run mode: `python youtube_cleaner.py --threshold 50 --dry-run`
- [ ] Complete OAuth authentication in your browser
- [ ] Verify that the script can access your Watch Later playlist

### 6. Test the Script

- [ ] Test with different thresholds in dry-run mode:
  - [ ] `python youtube_cleaner.py --threshold any --dry-run`
  - [ ] `python youtube_cleaner.py --threshold 25 --dry-run`
  - [ ] `python youtube_cleaner.py --threshold 50 --dry-run`
  - [ ] `python youtube_cleaner.py --threshold 75 --dry-run`
- [ ] Review the output to ensure it's working as expected

### 7. Execute Cleaning (When Ready)

- [ ] Choose your preferred threshold
- [ ] Run with `--execute` flag: `python youtube_cleaner.py --threshold 50 --execute`
- [ ] Verify videos were removed from Watch Later playlist

## Future Enhancements

### Implement Watch Percentage Tracking

Currently, the YouTube Data API v3 doesn't easily provide watch percentage data. Choose one of these approaches:

#### Option A: YouTube Analytics API
- [ ] Research YouTube Analytics API requirements
- [ ] Enable YouTube Analytics API in Google Cloud Console
- [ ] Update script to use Analytics API for watch history
- [ ] Test and validate watch percentage accuracy

#### Option B: Google Takeout Export
- [ ] Export watch history from [Google Takeout](https://takeout.google.com/)
- [ ] Create parser for watch history JSON/CSV files
- [ ] Integrate parser with main script
- [ ] Test with exported data

#### Option C: Custom Tracking
- [ ] Design custom tracking solution (browser extension, etc.)
- [ ] Implement tracking database/storage
- [ ] Integrate with main script
- [ ] Test tracking accuracy

### Additional Features (Optional)

- [ ] Add scheduling/automation (cron job or Task Scheduler)
- [ ] Add email notifications when cleaning is complete
- [ ] Create web interface for easier configuration
- [ ] Add support for other playlists (not just Watch Later)
- [ ] Implement undo functionality (backup removed videos)
- [ ] Add statistics/reporting (how many videos cleaned, storage saved, etc.)
- [ ] Add filters (by channel, duration, upload date, etc.)
- [ ] Create GUI version for non-technical users

## Security Checklist

- [ ] Verify `client_secrets.json` is in `.gitignore`
- [ ] Verify `token.pickle` is in `.gitignore`
- [ ] Never share or commit OAuth credentials
- [ ] Regularly review authorized apps in Google Account settings
- [ ] Keep dependencies up to date for security patches

## Documentation

- [ ] Read through README.md
- [ ] Read through SETUP.md for detailed instructions
- [ ] Customize config.py settings if needed
- [ ] Document any custom modifications you make

## Notes

- See **SETUP.md** for detailed step-by-step instructions
- See **README.md** for usage examples and documentation
- The script is safe - always use `--dry-run` first to preview changes
- YouTube API has daily quota limits - be mindful if cleaning large playlists
