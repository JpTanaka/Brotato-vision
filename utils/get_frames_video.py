import cv2
import os


def remove_files_folder(folder_path: str) -> None:
    for file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file)):
            os.remove(os.path.join(folder_path, file))


def extract_frames(video_path: str, output_folder: str, interval_seconds: str) -> None:
    for video_name in os.listdir(video_path):
        video_name_no_extension, extension = video_name.split(".")
        images_folder = os.path.join(output_folder, video_name_no_extension)
        if not os.path.isdir(images_folder):
            os.mkdir(images_folder)
            os.mkdir(os.path.join(images_folder, "canny"))

        remove_files_folder(images_folder)

        cap = cv2.VideoCapture(os.path.join(video_path, video_name))
        if not cap.isOpened():
            print("Error: Could not open video file.")
            return

        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        interval_frames = int(frame_rate * interval_seconds)

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % interval_frames == 0:
                frame_filename = f"{images_folder}/{video_name_no_extension}_frame_{frame_count // interval_frames}.jpg"
                cv2.imwrite(frame_filename, frame)
                print(f"Saved {frame_filename}")
                cv2.imwrite(
                    os.path.join(
                        images_folder,
                        "canny",
                        f"frame_{frame_count//interval_frames}.jpg",
                    ),
                    cv2.Canny(frame, 200, 200),
                )

            frame_count += 1

        cap.release()


if __name__ == "__main__":
    video_path = "videos/"
    output_folder = "images"
    interval_seconds = 5

    extract_frames(video_path, output_folder, interval_seconds)
