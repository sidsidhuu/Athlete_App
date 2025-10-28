
# Vision-Based Human Activity Recognition for Athlete Fitness

## Overview
This project uses **computer vision (OpenCV)** and **CNN** to recognize athlete activities:
- Running
- Walking
- Fitness Walking
- Squats
- Pushups
- Jumping Jacks
- Stretching
- Volleyball (Gaming Volleyball)

It also calculates a **performance score** based on activity type, duration, and intensity.

## Activity Parameters
Each activity is analyzed with the following parameters:
- **Duration**: Time spent performing the activity.
- **Intensity**: Measured based on movement speed and repetitions (e.g., high for running, moderate for walking).
- **Repetitions**: Applicable for exercises like squats, pushups, jumping jacks.
- **Performance Score**: Calculated as a weighted average of duration, intensity, and form accuracy.

### Specific Activity Details:
- **Running**: High-intensity cardio, focuses on speed and endurance.
- **Walking/Fitness Walking**: Low to moderate intensity, promotes recovery and light cardio.
- **Squats**: Strength training for lower body, repetitions-based.
- **Pushups**: Upper body strength, repetitions-based.
- **Jumping Jacks**: Full-body cardio, high-intensity bursts.
- **Stretching**: Flexibility and recovery, duration-based.
- **Volleyball (Gaming Volleyball)**: Sport-specific activity, involves jumping, spiking, and agility.

## Folder Structure
```
vision_based_human_activity/
├── README.md                 # Project documentation
├── TODO.md                   # Task tracking
├── main.py                   # Main application script
├── train_model.py            # Script for training the CNN model
├── extract_frames.py         # Script for extracting frames from videos
├── requirements.txt          # Python dependencies
├── dataset/                  # Dataset directory
│   ├── train/                # Training data
│   │   ├── jumping_jacks/    # Videos for jumping jacks
│   │   ├── pushups/          # Videos for pushups
│   │   ├── running/          # Videos for running
│   │   ├── squats/           # Videos for squats
│   │   ├── stretching/       # Videos for stretching
│   │   └── walking/          # Videos for walking
│   └── test/                 # Testing data
│       ├── jumping_jacks/    # Test videos for jumping jacks
│       ├── pushups/          # Test videos for pushups
│       ├── running/          # Test videos for running
│       ├── squats/           # Test videos for squats
│       ├── stretching/       # Test videos for stretching
│       └── walking/          # Test videos for walking
├── models/                   # Trained models
│   └── activity_model.h5     # Saved CNN model
├── utils/                    # Utility scripts
│   ├── __init__.py
│   └── performance.py        # Performance scoring logic
└── video_source/             # Source videos for activities
    ├── jumping_jacks/        # Source videos for jumping jacks
    ├── pushups/              # Source videos for pushups
    ├── running/              # Source videos for running
    ├── squats/               # Source videos for squats
    ├── stretching/           # Source videos for stretching
    └── walking/              # Source videos for walking
```
