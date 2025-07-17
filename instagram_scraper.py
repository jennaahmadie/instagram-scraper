import instaloader
from datetime import datetime

def scrape_public_profile(username):
    """
    Scrapes basic public profile data from Instagram without login.

    Args:
        username (str): Instagram username (without @)

    Returns:
        dict: Basic profile information or error message
    """
    username = username.lstrip('@')

    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )

    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        return {
            'username': profile.username,
            'full_name': profile.full_name,
            'followers': profile.followers,
            'following': profile.followees,
            'total_posts': profile.mediacount,
            'is_private': profile.is_private,
            'is_verified': profile.is_verified,
            'timestamp': datetime.now().isoformat(),
            'note': "Post-level data unavailable without login"
        }

    except instaloader.exceptions.ProfileNotExistsException:
        return {"error": f"Profile '{username}' not found"}
    except instaloader.exceptions.QueryReturnedNotFoundException:
        return {"error": f"Instagram blocked unauthenticated access for '{username}'"}
    except Exception as e:
        return {"error": str(e)}
