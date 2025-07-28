import instaloader
import os
from datetime import datetime;
from dotenv import load_dotenv

load_dotenv()

INSTA_USERNAME = os.getenv("INSTA_USERNAME")
INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")


def get_authenticated_loader():
    """
    Returns an Instaloader object that's logged in using environment variables.
    If session file exists, reuse it.
    """
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
        # Try to load existing session file
        loader.load_session_from_file(INSTA_USERNAME)
    except Exception:
        # Fallback to login if session file doesn't exist
        print("🔐 Logging in fresh with username and password...")
        loader.login(INSTA_USERNAME, INSTA_PASSWORD)
        loader.save_session_to_file()

    return loader

def scrape_full_profile(username, number_of_posts=3):
    """
    Uses authenticated session to fetch full post + profile data.
    """
    username = username.lstrip('@')
    loader = get_authenticated_loader()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        if profile.is_private and not profile.followed_by_viewer:
            return {"error": "Private profile. You must follow the account to access posts."}

        # Profile info
        data = {
            'username': profile.username,
            'full_name': profile.full_name,
            'followers': profile.followers,
            'following': profile.followees,
            'total_posts': profile.mediacount,
            'is_private': profile.is_private,
            'is_verified': profile.is_verified,
            'timestamp': datetime.now().isoformat(),
        }

        # Post analytics
        posts_data = []
        for i, post in enumerate(profile.get_posts()):
            if i >= number_of_posts:
                break
            posts_data.append({
                'shortcode': post.shortcode,
                'url': f"https://www.instagram.com/p/{post.shortcode}/",
                'likes': post.likes,
                'comments': post.comments,
                'caption': post.caption[:100] if post.caption else "",
                'is_video': post.is_video,
                'date': post.date.isoformat()[:10]
            })

        data["posts"] = posts_data
        return data

    except instaloader.exceptions.ProfileNotExistsException:
        return {"error": "Profile does not exist"}
    except instaloader.exceptions.LoginRequiredException:
        return {"error": "Login required. Credentials may be invalid or blocked."}
    except Exception as e:
        return {"error": str(e)}