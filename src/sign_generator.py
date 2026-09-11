import os
from src.sign_library import get_sign, get_absolute_sign_path, PROJECT_ROOT


def retrieve_signs(sign_sequence):
    """
    Retrieves project-relative video paths for a sequence of sign words.
    Returns a list of video paths (or 'SIGN_NOT_FOUND' if missing).
    """
    retrieved_signs = []

    for sign in sign_sequence:
        resource = get_sign(sign)

        if resource:
            retrieved_signs.append(resource)
        else:
            retrieved_signs.append("SIGN_NOT_FOUND")

    return retrieved_signs


def sequence_sign_videos(sign_sequence):
    """
    Resolves full absolute video file paths for valid signs in sequence.
    Returns a list of metadata dicts containing word, relative path, and absolute path.
    """
    sequence_items = []

    for sign in sign_sequence:
        rel_path = get_sign(sign)
        abs_path = get_absolute_sign_path(sign)
        exists = abs_path is not None and os.path.exists(abs_path)

        sequence_items.append({
            "word": str(sign).upper(),
            "relative_path": rel_path if rel_path else "SIGN_NOT_FOUND",
            "absolute_path": abs_path if exists else None,
            "found": exists
        })

    return sequence_items


def play_sign_sequence(sign_sequence, display_window=False):
    """
    Optional playback helper for video sequences using OpenCV if installed.
    """
    items = sequence_sign_videos(sign_sequence)
    valid_paths = [item["absolute_path"] for item in items if item["found"]]

    if display_window:
        try:
            import cv2
            for video_path in valid_paths:
                cap = cv2.VideoCapture(video_path)
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    cv2.imshow("SignBridge - ISL Playback", frame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return valid_paths
                cap.release()
            cv2.destroyAllWindows()
        except ImportError:
            pass

    return valid_paths