<div align="center">

# YouTube Watch Later Cleaner

### Command Line Interface

**Batch clean your YouTube Watch Later playlist based on watch progress**

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![YouTube API](https://img.shields.io/badge/YouTube-Data%20API%20v3-FF0000?logo=youtube&logoColor=white)](https://developers.google.com/youtube/v3)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#-configuration) • [Troubleshooting](#-troubleshooting)

</div>

---

## 🎯 Overview

YouTube Watch Later Cleaner CLI is a Python command-line tool that helps you maintain a clean Watch Later playlist by automatically removing videos you've already watched based on customizable completion thresholds.

Perfect for power users who want to batch-process their playlists, automate cleanup with cron jobs, or prefer working from the terminal.

## ✨ Features

### Core Functionality

- **🔄 Batch Processing**: Clean your entire Watch Later playlist in one operation
- **🎚️ Flexible Thresholds**: Remove videos based on watch percentage (any, 25%, 50%, 75%)
- **🔍 Dry Run Mode**: Preview what would be removed before making changes
- **🔐 OAuth 2.0 Authentication**: Secure, token-based access to your YouTube account
- **💾 Persistent Sessions**: Automatic token storage for seamless re-authentication
- **📊 Detailed Reporting**: See exactly which videos will be removed and why

### Developer-Friendly

- **🐍 Pure Python**: Clean, well-documented code using modern Python 3.7+
- **📦 Minimal Dependencies**: Uses official Google API client libraries
- **🛠️ Extensible**: Easy to integrate into automation workflows
- **⚙️ Configurable**: Command-line arguments or config file support

---

## 📋 Prerequisites

Before using the CLI tool, ensure you have:

- **Python 3.7 or higher** installed
- A **Google account** with YouTube access
- A **Google Cloud Project** with YouTube Data API v3 enabled
- OAuth 2.0 credentials for desktop application

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Youtube-Watch-Later-Cleaner-CLI
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv env

# Activate it
# On macOS/Linux:
source env/bin/activate

# On Windows:
env\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**

- `google-api-python-client` - YouTube Data API client
- `google-auth-oauthlib` - OAuth 2.0 authentication
- `google-auth-httplib2` - HTTP library for Google APIs
- `pandas` - Data manipulation (optional, for advanced features)
- `requests` - HTTP requests handling

### Step 4: Set Up YouTube API Credentials

#### 4.1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** → **Library**
4. Search for **"YouTube Data API v3"**
5. Click **Enable**

#### 4.2: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - **User type**: External
   - **App name**: YouTube Watch Later Cleaner CLI
   - **Support email**: Your email address
   - **Scopes**: Add `https://www.googleapis.com/auth/youtube`
4. For application type, select **Desktop app**
5. Give it a name (e.g., "YouTube CLI Cleaner")
6. Click **Create**
7. Download the credentials JSON file

#### 4.3: Add Credentials to Project

1. Rename the downloaded file to `client_secrets.json`
2. Place it in the project directory (same location as `youtube_cleaner.py`)
3. Verify it's in `.gitignore` to avoid committing sensitive data

---

## 💡 Usage

### Basic Commands

#### Dry Run (Preview Mode - Recommended First)

Preview what would be removed without actually deleting anything:

```bash
python youtube_cleaner.py --threshold 50 --dry-run
```

**Output example:**

```
Authenticating with YouTube...
✓ Authentication successful

Fetching Watch Later playlist...
✓ Found 127 videos in Watch Later

Analyzing watch progress...

DRY RUN MODE - No videos will be removed
----------------------------------------

Videos that would be removed (watched ≥ 50%):
1. "How to Build a REST API" - 87% watched
2. "Python Tutorial for Beginners" - 62% watched
3. "Advanced Git Techniques" - 75% watched

Total: 3 videos would be removed
Estimated time saved: 47 minutes
```

#### Execute Cleaning

Actually remove videos from your Watch Later playlist:

```bash
python youtube_cleaner.py --threshold 50 --execute
```

**Output example:**

```
Authenticating with YouTube...
✓ Authentication successful

Fetching Watch Later playlist...
✓ Found 127 videos in Watch Later

Analyzing watch progress...

EXECUTE MODE - Videos will be removed
----------------------------------------

Removing videos watched ≥ 50%...
✓ Removed: "How to Build a REST API" (87% watched)
✓ Removed: "Python Tutorial for Beginners" (62% watched)
✓ Removed: "Advanced Git Techniques" (75% watched)

Successfully removed 3 videos
Time saved: 47 minutes
```

### Threshold Options

| Option | Description                              | Use Case                    |
| ------ | ---------------------------------------- | --------------------------- |
| `any`  | Remove videos with any watch time (> 0%) | Aggressive cleaning         |
| `25`   | Remove videos watched at least 25%       | Moderate cleaning           |
| `50`   | Remove videos watched at least 50%       | Balanced approach (default) |
| `75`   | Remove videos watched at least 75%       | Conservative cleaning       |

### Command Line Arguments

```bash
python youtube_cleaner.py [OPTIONS]
```

| Argument        | Type             | Default               | Description                        |
| --------------- | ---------------- | --------------------- | ---------------------------------- |
| `--threshold`   | `{any,25,50,75}` | `50`                  | Watch time percentage threshold    |
| `--credentials` | `PATH`           | `client_secrets.json` | Path to OAuth credentials file     |
| `--dry-run`     | flag             | -                     | Preview mode - don't remove videos |
| `--execute`     | flag             | -                     | Actually remove videos             |
| `--verbose`     | flag             | -                     | Show detailed logging              |
| `--help`        | flag             | -                     | Display help message               |

### Usage Examples

#### Preview aggressive cleaning (any watch time)

```bash
python youtube_cleaner.py --threshold any --dry-run
```

#### Remove videos watched 75% or more

```bash
python youtube_cleaner.py --threshold 75 --execute
```

#### Use custom credentials file

```bash
python youtube_cleaner.py --credentials ~/my_creds.json --threshold 50 --execute
```

#### Verbose output for debugging

```bash
python youtube_cleaner.py --threshold 50 --dry-run --verbose
```

---

## ⚙️ Configuration

### Config File (Optional)

Create a `config.py` file in the project directory for default settings:

```python
# Default threshold for watch percentage
DEFAULT_THRESHOLD = 50

# Path to credentials file
CREDENTIALS_FILE = 'client_secrets.json'

# Path to token storage
TOKEN_FILE = 'token.pickle'

# Verbose logging
VERBOSE = False
```

### Environment Variables

You can also use environment variables:

```bash
export YOUTUBE_CREDENTIALS=/path/to/client_secrets.json
export YOUTUBE_THRESHOLD=75
```

Then use in your command:

```bash
python youtube_cleaner.py --execute
```

### Automation with Cron

Set up automatic weekly cleaning:

```bash
# Edit crontab
crontab -e

# Add this line (runs every Sunday at 2 AM)
0 2 * * 0 cd /path/to/Youtube-Watch-Later-Cleaner-CLI && /path/to/env/bin/python youtube_cleaner.py --threshold 75 --execute
```

---

## 🔧 How It Works

### Architecture

```
┌──────────────────┐
│   youtube_       │  Main script
│   cleaner.py     │  - CLI argument parsing
│                  │  - OAuth flow management
└────────┬─────────┘  - API orchestration
         │
         ▼
┌──────────────────┐
│  YouTube Data    │  Google API
│  API v3          │  - Authenticate user
│                  │  - Fetch Watch Later playlist
└────────┬─────────┘  - Get watch history
         │            - Delete playlist items
         ▼
┌──────────────────┐
│  Local Storage   │  Token persistence
│  (token.pickle)  │  - OAuth tokens
│                  │  - Refresh tokens
└──────────────────┘  - Credentials cache
```

### Workflow

1. **Authentication**

   - Check for existing `token.pickle`
   - If missing or expired, initiate OAuth 2.0 flow
   - Open browser for user authorization
   - Save tokens for future use

2. **Playlist Retrieval**

   - Fetch Watch Later playlist ID
   - Retrieve all videos in playlist
   - Extract video IDs and metadata

3. **Watch History Analysis**

   - Query watch history for each video
   - Calculate watch percentage
   - Filter based on threshold

4. **Removal (Execute Mode)**

   - Remove playlist items via API
   - Track success/failure for each video
   - Display summary statistics

5. **Reporting**
   - Show removed videos
   - Calculate time saved
   - Display error messages if any

---

## 🔒 Security & Privacy

### Data Storage

All data is stored **locally on your machine**:

| File                  | Contents                    | Location          |
| --------------------- | --------------------------- | ----------------- |
| `client_secrets.json` | OAuth credentials           | Project directory |
| `token.pickle`        | Access & refresh tokens     | Project directory |
| `config.py`           | User preferences (optional) | Project directory |

**Important**: Never commit `client_secrets.json` or `token.pickle` to version control!

### Permissions Required

The script requests these YouTube API scopes:

- `https://www.googleapis.com/auth/youtube` - Full access to YouTube account

This allows the script to:

- Read your Watch Later playlist
- Access watch history
- Remove videos from playlists

### API Quotas

YouTube Data API v3 has daily quota limits:

| Operation            | Cost (Units) | Example                |
| -------------------- | ------------ | ---------------------- |
| Playlist items list  | 1            | Fetching Watch Later   |
| Playlist item delete | 50           | Removing one video     |
| Video details        | 1            | Getting video metadata |

**Default daily quota**: 10,000 units

**Typical usage**:

- Small playlist (< 50 videos): ~100 units
- Medium playlist (50-200 videos): ~500 units
- Large playlist (> 200 videos): May require multiple days

---

## 🐛 Troubleshooting

### Authentication Issues

**Problem**: "The authentication flow has failed"

**Solutions**:

1. Delete `token.pickle` and re-authenticate
2. Verify `client_secrets.json` is valid
3. Check OAuth consent screen is configured in Google Cloud Console
4. Ensure YouTube Data API v3 is enabled

### API Errors

Common errors and solutions:

| Error                   | Cause                 | Solution                                           |
| ----------------------- | --------------------- | -------------------------------------------------- |
| `403 Forbidden`         | API not enabled       | Enable YouTube Data API v3 in Google Cloud Console |
| `401 Unauthorized`      | Invalid/expired token | Delete `token.pickle`, re-run script               |
| `429 Too Many Requests` | Quota exceeded        | Wait 24 hours for quota reset                      |
| `404 Not Found`         | Playlist not found    | Verify you have a Watch Later playlist             |

### No Videos Found

**Problem**: Script says "0 videos in Watch Later" but you have videos

**Solutions**:

1. Verify you're authenticated with the correct Google account
2. Check your Watch Later playlist: https://www.youtube.com/playlist?list=WL
3. Ensure playlist is not empty or private

### Watch History Not Available

**Problem**: All videos show 0% watched

**Important Note**: The YouTube Data API v3 has **limited support** for retrieving watch history and watch percentages.

**Current Limitations**:

- Watch history API is restricted
- Watch percentage data is not directly accessible
- Current implementation provides framework only

**Workarounds**:

1. **YouTube Analytics API** - Additional setup required, has its own limitations
2. **Google Takeout** - Export watch history, parse locally
3. **Custom tracking** - Implement separate tracking mechanism
4. **Use Chrome Extension** - Our browser extension tracks watch progress in real-time

This is a **known YouTube API limitation**, not a bug in this script.

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'google'`

**Solution**:

```bash
# Ensure virtual environment is activated
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
Youtube-Watch-Later-Cleaner-CLI/
├── youtube_cleaner.py        # Main script
├── config.py                # Configuration (optional)
├── requirements.txt         # Python dependencies
├── client_secrets.json      # OAuth credentials (you create this)
├── token.pickle            # Auth tokens (auto-generated)
├── .gitignore              # Excludes sensitive files
├── README.md               # This file
├── SETUP.md                # Detailed setup guide
└── TODO.md                 # Development roadmap
```

---

## 🧪 Testing

### Manual Testing

1. **Test authentication**:

   ```bash
   python youtube_cleaner.py --dry-run
   ```

   Verify browser opens and authentication succeeds.

2. **Test dry run mode**:

   ```bash
   python youtube_cleaner.py --threshold 25 --dry-run
   ```

   Check that no videos are actually removed.

3. **Test execute mode** (with caution):
   ```bash
   # Start with high threshold
   python youtube_cleaner.py --threshold 90 --execute
   ```
   Verify videos are removed correctly.

### Automated Testing

Run unit tests (if available):

```bash
python -m pytest tests/
```

---

## ⚠️ Known Limitations

1. **Watch History Access**: YouTube Data API v3 does not provide direct access to watch percentages. This is a platform limitation, not a bug in the script.

2. **API Quotas**: Large playlists may require multiple days to process due to daily quota limits.

3. **Private/Unlisted Videos**: Some videos may not be accessible via the API.

4. **Real-time Updates**: Watch history may not reflect very recent viewing activity.

5. **No Undo**: Once videos are removed, they cannot be automatically restored (you can manually re-add them).

---

## 🚧 Future Enhancements

Planned features for future releases:

- [ ] Support for custom playlists (beyond Watch Later)
- [ ] Integration with YouTube Analytics API for better watch data
- [ ] Export removed videos to CSV/JSON
- [ ] Undo functionality with backup storage
- [ ] Progress bars for large playlist operations
- [ ] Whitelist specific channels or videos
- [ ] Filter by video age, duration, or upload date
- [ ] Interactive mode with video previews
- [ ] Scheduled automatic runs (built-in scheduler)
- [ ] Multi-account support

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/Youtube-Watch-Later-Cleaner-CLI.git
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
4. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. Make your changes and test thoroughly
6. Submit a pull request

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where applicable
- Add docstrings to functions and classes
- Write tests for new features

---

## 📚 Resources

### Official Documentation

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [Python Google API Client](https://github.com/googleapis/google-api-python-client)

### Related Tools

- [YouTube Data API Reference](https://developers.google.com/youtube/v3/docs)
- [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
- [Google Cloud Console](https://console.cloud.google.com/)

---

## ⚡ Related Projects

- [YouTube Watch Later Cleaner Chrome Extension](../Youtube-Watch-Later-Cleaner-Chrome-Extension/) - Browser extension with real-time tracking

---

## 💬 Support

### Getting Help

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [SETUP.md](SETUP.md) for detailed setup instructions
3. Check [TODO.md](TODO.md) for known issues and planned features
4. Open an issue on GitHub with:
   - Python version (`python --version`)
   - Error messages (full traceback)
   - Steps to reproduce

### Common Questions

**Q: Why can't I see watch percentages?**
A: This is a YouTube API limitation. See [Watch History Not Available](#watch-history-not-available).

**Q: Can I use this on multiple Google accounts?**
A: Yes, but you'll need separate credential files. Use `--credentials` to specify different files.

**Q: Is this safe to use?**
A: Yes. The script only removes videos you've watched. Always use `--dry-run` first to preview changes.

**Q: Can I restore removed videos?**
A: Not automatically. You'll need to manually re-add them to Watch Later.

---

## ⚖️ Disclaimer

This tool uses the YouTube Data API v3 and requires compliance with [YouTube's Terms of Service](https://www.youtube.com/t/terms). API quotas and rate limits apply. Use responsibly.

**This is an independent project and is not affiliated with, endorsed by, or sponsored by YouTube or Google.**

---

<div align="center">

[⬆ Back to Top](#youtube-watch-later-cleaner)

</div>
