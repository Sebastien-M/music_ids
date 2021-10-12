from enum import Enum

from django.db import models

VALID_AUDIO_FILE_TYPES = {
    "flac": "audio/flac",
    "m3u": "audio/mpegurl",
    "m3u8": "audio/mpegurl",
    "m4a": "audio/mp4",
    "m4b": "audio/mp4",
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg",
    "opus": "audio/ogg",
    "pls": "audio/x-scpls",
    "wav": "audio/wav",
    "aac": "audio/aac",
}


class ProjectFileTypeChoices(models.TextChoices):
    ABLETON_PROJECT_FILE = "ABLETON_PROJECT_FILE", "Ableton project file"
    AUDIO_FILE = "AUDIO_FILE", "Audio file"
    MUSIC_SHEET = "MUSIC_SHEET", "Music sheet"
