from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Returns a weighted score (0.0–1.0) and matched reasons for a song against a user profile."""
    score = 0.0
    reasons = []

    # Energy (0.30) — distance-based; target_energy is 0.0–1.0
    energy_match = 1.0 - abs(song['energy'] - user_prefs.get('target_energy', 0.5))
    score += 0.30 * energy_match
    if energy_match >= 0.8:
        reasons.append(f"Energy ({song['energy']}) closely matches your target")

    # Mood (0.20) — exact string match
    mood_match = 1.0 if song['mood'] == user_prefs.get('favorite_mood', '') else 0.0
    score += 0.20 * mood_match
    if mood_match:
        reasons.append(f"Mood '{song['mood']}' matches your favorite mood")

    # Tempo (0.15) — distance-based, normalized over a 100 BPM range
    if 'target_tempo_bpm' in user_prefs:
        tempo_match = 1.0 - min(abs(song['tempo_bpm'] - user_prefs['target_tempo_bpm']) / 100.0, 1.0)
        score += 0.15 * tempo_match
        if tempo_match >= 0.8:
            reasons.append(f"Tempo ({song['tempo_bpm']} BPM) is close to your target")

    # Valence (0.12) — distance-based
    if 'target_valence' in user_prefs:
        valence_match = 1.0 - abs(song['valence'] - user_prefs['target_valence'])
        score += 0.12 * valence_match
        if valence_match >= 0.8:
            reasons.append(f"Valence ({song['valence']}) aligns with your preference")

    # Danceability (0.10) — distance-based
    if 'target_danceability' in user_prefs:
        dance_match = 1.0 - abs(song['danceability'] - user_prefs['target_danceability'])
        score += 0.10 * dance_match
        if dance_match >= 0.8:
            reasons.append(f"Danceability ({song['danceability']}) suits your style")

    # Acousticness (0.08) — boolean preference
    if 'likes_acoustic' in user_prefs:
        likes_acoustic = user_prefs['likes_acoustic']
        acoustic_match = song['acousticness'] if likes_acoustic else (1.0 - song['acousticness'])
        score += 0.08 * acoustic_match
        if acoustic_match >= 0.7:
            label = 'acoustic' if likes_acoustic else 'non-acoustic'
            reasons.append(f"Acousticness ({song['acousticness']}) fits your {label} preference")

    # Genre (0.05) — exact string match
    genre_match = 1.0 if song['genre'] == user_prefs.get('favorite_genre', '') else 0.0
    score += 0.05 * genre_match
    if genre_match:
        reasons.append(f"Genre '{song['genre']}' matches your favorite genre")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Scores every song in the catalog and returns the top k matches sorted by score."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
