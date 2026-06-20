"""Hằng số toàn cục dùng chung cho toàn bộ ứng dụng."""

from __future__ import annotations

# URL mặc định của YouTube TV.
YOUTUBE_TV_URL = "https://www.youtube.com/tv"
YOUTUBE_ACTIVATE_URL = "https://www.youtube.com/activate"

# User-Agent mặc định mô phỏng Smart TV Samsung Tizen.
DEFAULT_TV_USER_AGENT = (
 "Mozilla/5.0 (SMART-TV; Linux; Tizen 6.5) AppleWebKit/537.36 "
 "(KHTML, like Gecko) 85.0.4183.93/6.5 TV Safari/537.36"
)

# Các độ phân giải TV được hỗ trợ (label -> (width, height)).
TV_RESOLUTIONS: dict[str, tuple[int, int]] = {
 "1080p": (1920, 1080),
 "2k": (2560, 1440),
 "4k": (3840, 2160),
 "8k": (7680, 4320),
}

# SponsorBlock API endpoint công khai.
SPONSORBLOCK_API = "https://sponsor.ajay.app/api/skipSegments"

# Các loại segment SponsorBlock được hỗ trợ.
SPONSORBLOCK_CATEGORIES = [
 "sponsor",
 "intro",
 "outro",
 "selfpromo",
 "interaction",
]

# Các endpoint YouTube InnerTube cần được log lại để debug.
YOUTUBE_API_ENDPOINTS = [
 "youtubei/v1/player",
 "youtubei/v1/browse",
 "youtubei/v1/next",
 "youtubei/v1/search",
]

# Danh sách domain quảng cáo bị chặn mặc định.
DEFAULT_AD_BLOCK_DOMAINS = [
 "doubleclick.net",
 "googleads.g.doubleclick.net",
 "pagead2.googlesyndication.com",
 "googlesyndication.com",
 "adservice.google.com",
 "adservice.google.com.vn",
 "ads.youtube.com",
 "static.doubleclick.net",
 "youtube.com/pagead",
 "youtube.com/api/stats/ads",
 "youtube.com/get_midroll_info",
]
