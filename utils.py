from pathlib import Path

import cv2

from config import SUPPORTED_EXTENSIONS


def is_supported_image(path: Path) -> bool:
    return (
            path.is_file()
            and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def get_output_parameters(extension: str) -> list:
    extension = extension.lower()

    if extension == ".png":
        return [
            cv2.IMWRITE_PNG_COMPRESSION,
            3,
        ]

    if extension in {".jpg", ".jpeg"}:
        return [
            cv2.IMWRITE_JPEG_QUALITY,
            100,
        ]

    if extension == ".webp":
        return [
            cv2.IMWRITE_WEBP_QUALITY,
            100,
        ]

    return []
