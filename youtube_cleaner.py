#!/usr/bin/env python3
"""
YouTube Watch Later Cleaner
Cleans up your Watch Later playlist based on watch time percentage.
"""

import os
import json
import argparse
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle

# YouTube API scopes needed
SCOPES = ['https://www.googleapis.com/auth/youtube']

# Watch time threshold options
THRESHOLD_OPTIONS = {
    'any': 0,      # Any watch time > 0%
    '25': 25,      # 25% watched
    '50': 50,      # 50% watched
    '75': 75       # 75% watched
}


class YouTubeWatchLaterCleaner:
    """Manages cleaning of YouTube Watch Later playlist based on watch progress."""

    def __init__(self, credentials_file: str = 'client_secrets.json'):
        """
        Initialize the cleaner.

        Args:
            credentials_file: Path to OAuth 2.0 client secrets JSON file
        """
        self.credentials_file = credentials_file
        self.youtube = None
        self.watch_later_playlist_id = None

    def authenticate(self) -> None:
        """Authenticate with YouTube API using OAuth 2.0."""
        creds = None
        token_file = 'token.pickle'

        # Load existing credentials if available
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)

        # If credentials don't exist or are invalid, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file '{self.credentials_file}' not found. "
                        "Please download it from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for future use
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

        # Build YouTube API client
        self.youtube = build('youtube', 'v3', credentials=creds)
        print("✓ Successfully authenticated with YouTube API")

    def get_watch_later_playlist_id(self) -> str:
        """
        Get the Watch Later playlist ID for the authenticated user.

        Returns:
            The Watch Later playlist ID
        """
        try:
            # Get the user's channels to find Watch Later playlist
            request = self.youtube.channels().list(
                part='contentDetails',
                mine=True
            )
            response = request.execute()

            if not response.get('items'):
                raise Exception("No channel found for authenticated user")

            # Watch Later playlist is in the user's content details
            # We need to use a different approach - get playlists and find Watch Later
            playlists_request = self.youtube.playlists().list(
                part='snippet,contentDetails',
                mine=True,
                maxResults=50
            )
            playlists_response = playlists_request.execute()

            # Watch Later is a special playlist, we can access it via playlistItems
            # with a special playlist ID 'WL'
            self.watch_later_playlist_id = 'WL'
            print(f"✓ Found Watch Later playlist (ID: WL)")
            return self.watch_later_playlist_id

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            raise

    def get_watch_later_videos(self) -> List[Dict]:
        """
        Get all videos from the Watch Later playlist.

        Returns:
            List of video items from the playlist
        """
        videos = []
        next_page_token = None

        try:
            while True:
                request = self.youtube.playlistItems().list(
                    part='snippet,contentDetails',
                    playlistId=self.watch_later_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()

                videos.extend(response.get('items', []))

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break

            print(f"✓ Found {len(videos)} videos in Watch Later playlist")
            return videos

        except HttpError as e:
            print(f"An HTTP error occurred while fetching videos: {e}")
            raise

    def get_video_watch_progress(self, video_id: str) -> Optional[Dict]:
        """
        Get watch progress for a specific video.

        Args:
            video_id: The YouTube video ID

        Returns:
            Dictionary with watch progress information or None if not available
        """
        try:
            # Get video details including duration
            video_request = self.youtube.videos().list(
                part='contentDetails,statistics',
                id=video_id
            )
            video_response = video_request.execute()

            if not video_response.get('items'):
                return None

            video_info = video_response['items'][0]
            duration_str = video_info['contentDetails']['duration']

            # Get viewing history / watch progress
            # Note: The YouTube API doesn't directly provide watch percentage
            # We need to use the reportHistory API which requires additional scope
            # For now, we'll use the videos.rate endpoint to check if watched

            # Try to get the video from the user's history
            history_request = self.youtube.videos().list(
                part='contentDetails',
                myRating='like',
                id=video_id
            )

            # Alternative: Use the reportHistory API (requires youtube.readonly scope)
            # This is a limitation - YouTube API doesn't easily expose watch percentage
            # We'll need to use the YouTube Analytics API or report history

            return {
                'video_id': video_id,
                'duration': duration_str,
                'watch_percentage': None  # Will implement this with Analytics API
            }

        except HttpError as e:
            print(f"Error getting video progress for {video_id}: {e}")
            return None

    def get_videos_watch_history(self, video_ids: List[str]) -> Dict[str, float]:
        """
        Get watch history percentage for multiple videos.

        Note: YouTube API has limited support for watch history/progress.
        This is a simplified version that checks if videos appear in watch history.

        Args:
            video_ids: List of video IDs to check

        Returns:
            Dictionary mapping video_id to watch percentage (0-100)
        """
        watch_progress = {}

        try:
            # Get user's watch history
            # Note: This requires the youtube.force-ssl scope
            # The API doesn't directly provide watch percentage easily
            # This is a known limitation of the YouTube Data API

            # For demonstration, we'll return a placeholder
            # In production, you'd need to use YouTube Analytics API
            # or parse the actual watch history

            for video_id in video_ids:
                # Placeholder - in reality, you'd need to implement
                # proper watch history tracking
                watch_progress[video_id] = 0.0

            return watch_progress

        except HttpError as e:
            print(f"Error getting watch history: {e}")
            return watch_progress

    def remove_video_from_watch_later(self, playlist_item_id: str, video_title: str) -> bool:
        """
        Remove a video from the Watch Later playlist.

        Args:
            playlist_item_id: The playlist item ID (not the video ID)
            video_title: Title of the video (for logging)

        Returns:
            True if successful, False otherwise
        """
        try:
            self.youtube.playlistItems().delete(
                id=playlist_item_id
            ).execute()

            print(f"  ✓ Removed: {video_title}")
            return True

        except HttpError as e:
            print(f"  ✗ Failed to remove {video_title}: {e}")
            return False

    def clean_watch_later(self, threshold: float, dry_run: bool = True) -> None:
        """
        Clean the Watch Later playlist based on watch time threshold.

        Args:
            threshold: Minimum watch percentage (0-100) to remove video
            dry_run: If True, only show what would be removed without actually removing
        """
        print(f"\n{'DRY RUN - ' if dry_run else ''}Cleaning Watch Later playlist...")
        print(f"Threshold: {threshold}% watch time\n")

        # Get Watch Later playlist ID
        self.get_watch_later_playlist_id()

        # Get all videos in Watch Later
        videos = self.get_watch_later_videos()

        if not videos:
            print("No videos found in Watch Later playlist.")
            return

        # Note: Due to YouTube API limitations, we can't easily get exact watch percentages
        # This implementation shows the structure. You would need to:
        # 1. Use YouTube Analytics API for better watch history data
        # 2. Or maintain your own tracking database
        # 3. Or use browser history/YouTube Data Export

        print("\nIMPORTANT NOTE:")
        print("The YouTube Data API v3 has limited support for watch history/progress.")
        print("To fully implement watch percentage tracking, you'll need to either:")
        print("  1. Use YouTube Analytics API (requires additional setup)")
        print("  2. Export and parse your YouTube watch history")
        print("  3. Implement custom tracking\n")

        removed_count = 0
        would_remove_count = 0

        print(f"Checking {len(videos)} videos...\n")

        for video in videos:
            playlist_item_id = video['id']
            video_id = video['snippet']['resourceId']['videoId']
            video_title = video['snippet']['title']

            # For demonstration, we'll show the structure
            # In production, replace this with actual watch percentage retrieval
            watch_percentage = 0.0  # Placeholder

            # Check if video meets threshold for removal
            should_remove = watch_percentage >= threshold or (threshold == 0 and watch_percentage > 0)

            if should_remove:
                if dry_run:
                    print(f"  Would remove: {video_title} ({watch_percentage}% watched)")
                    would_remove_count += 1
                else:
                    if self.remove_video_from_watch_later(playlist_item_id, video_title):
                        removed_count += 1

        print(f"\n{'Would remove' if dry_run else 'Removed'} {would_remove_count if dry_run else removed_count} video(s)")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Clean YouTube Watch Later playlist based on watch time percentage'
    )
    parser.add_argument(
        '--threshold',
        type=str,
        choices=list(THRESHOLD_OPTIONS.keys()),
        default='50',
        help='Watch time threshold: any, 25, 50, or 75 percent'
    )
    parser.add_argument(
        '--credentials',
        type=str,
        default='client_secrets.json',
        help='Path to OAuth 2.0 client secrets JSON file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be removed without actually removing'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually remove videos (opposite of dry-run)'
    )

    args = parser.parse_args()

    # Determine if this is a dry run
    dry_run = not args.execute if args.execute else True

    # Get threshold value
    threshold_value = THRESHOLD_OPTIONS[args.threshold]

    print("=" * 60)
    print("YouTube Watch Later Cleaner")
    print("=" * 60)

    try:
        # Create cleaner instance
        cleaner = YouTubeWatchLaterCleaner(credentials_file=args.credentials)

        # Authenticate
        cleaner.authenticate()

        # Clean the playlist
        cleaner.clean_watch_later(threshold=threshold_value, dry_run=dry_run)

        print("\n" + "=" * 60)
        print("Done!")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nTo use this script, you need to:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select an existing one")
        print("3. Enable the YouTube Data API v3")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download the credentials JSON file as 'client_secrets.json'")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        raise


if __name__ == '__main__':
    main()
