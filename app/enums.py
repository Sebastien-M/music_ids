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


class ProjectKeyChoices(models.TextChoices):
    NONE = "", "Non spécifié"
    C = "C", "C"
    C_MINOR = "Cm", "Cm"
    C_SHARP = "C#", "C#"
    C_SHARP_MINOR = "C#m", "C#m"
    D = "D", "D"
    D_MINOR = "Dm", "Dm"
    D_SHARP = "D#", "D#"
    D_SHARP_MINOR = "D#m", "D#m"
    E = "E", "E"
    E_MINOR = "Em", "Em"
    F = "F", "F"
    F_MINOR = "Fm", "Fm"
    F_SHARP = "F#", "F#"
    F_SHARP_MINOR = "F#m", "F#m"
    G = "G", "G"
    G_MINOR = "Gm", "Gm"
    G_SHARP = "G#", "G#"
    G_SHARP_MINOR = "G#m", "G#m"
    A = "A", "A"
    A_MINOR = "Am", "Am"
    A_SHARP = "A#", "A#"
    A_SHARP_MINOR = "A#m", "A#m"
    B = "B", "B"
    B_MINOR = "Bm", "Bm"
