import random

def calculate_performance(activity, duration_sec, accuracy=0.9):
    """
    Calculate a performance score based on activity type, duration, and accuracy.
    Accuracy can later be measured via pose/form analysis.
    """

    # Base difficulty score (higher = more intense)
    base_score = {
        'running': 8,
        'walking': 3,
        'squats': 7,
        'pushups': 6,
        'jumping_jacks': 8,
        'stretching': 4
    }.get(activity, 5)

    # Normalize duration (max weight after 30 seconds)
    duration_factor = min(duration_sec / 30, 1.0)

    # Add variation (simulating athlete performance)
    intensity = random.uniform(0.85, 1.15)

    # Final performance score (0–100)
    score = base_score * 10 * duration_factor * accuracy * intensity
    return round(min(score, 100), 2)
