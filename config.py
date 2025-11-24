"""
Configuration settings for YouTube Watch Later Cleaner
"""

# Default watch time threshold percentage
# Options: 'any' (any watch time), '25', '50', '75'
DEFAULT_THRESHOLD = '50'

# Path to OAuth 2.0 credentials file
CREDENTIALS_FILE = 'client_secrets.json'

# Path to store authentication token
TOKEN_FILE = 'token.pickle'

# YouTube API settings
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Required OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/youtube']

# Watch Later playlist ID (this is a special YouTube playlist)
WATCH_LATER_PLAYLIST_ID = 'WL'

# Maximum results per API request (YouTube API limit is 50)
MAX_RESULTS_PER_PAGE = 50

# Logging settings
VERBOSE_OUTPUT = True
SHOW_PROGRESS = True

# Threshold mappings (percentage values)
THRESHOLD_PERCENTAGES = {
    'any': 0,      # Any watch time > 0%
    '25': 25,      # 25% watched
    '50': 50,      # 50% watched
    '75': 75       # 75% watched
}
