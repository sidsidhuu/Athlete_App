
import cv2
import os

# -------------------------
# CONFIGURATION
# -------------------------
# Path to folder containing videos organized by activity
video_source_dir = "video_source"  # e.g., video_source/running/*.mp4
# Destination dataset folder
dataset_dir = "dataset"  # dataset/train or dataset/test
# Number of frames to extract per video (optional: set 0 for all frames)
frames_per_video = 50

# -------------------------
# HELPER FUNCTION
# -------------------------
def extract_frames_from_video(video_path, output_folder, max_frames=0):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, total_frames // max_frames) if max_frames > 0 else 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % step == 0:
            cv2.imwrite(os.path.join(output_folder, f"frame_{count}.jpg"), frame)
        count += 1

    cap.release()
    print(f"[INFO] Extracted {count//step if max_frames>0 else count} frames from {video_path}")


# -------------------------
# MAIN SCRIPT
# -------------------------
for activity in os.listdir(video_source_dir):
    activity_folder = os.path.join(video_source_dir, activity)
    if not os.path.isdir(activity_folder):
        continue

    # Choose train or test automatically (e.g., 80% train, 20% test)
    video_files = [f for f in os.listdir(activity_folder) if f.endswith((".mp4",".avi"))]
    split_index = int(0.8 * len(video_files))
    train_videos = video_files[:split_index]
    test_videos = video_files[split_index:]

    # Extract frames for training videos
    for vid in train_videos:
        vid_path = os.path.join(activity_folder, vid)
        output_folder = os.path.join(dataset_dir, "train", activity)
        extract_frames_from_video(vid_path, output_folder, frames_per_video)

    # Extract frames for testing videos
    for vid in test_videos:
        vid_path = os.path.join(activity_folder, vid)
        output_folder = os.path.join(dataset_dir, "test", activity)
        extract_frames_from_video(vid_path, output_folder, frames_per_video)
