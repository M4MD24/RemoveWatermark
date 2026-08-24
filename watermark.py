from pathlib import Path

import cv2
import numpy as np

from config import (
    ROI_X1,
    ROI_X2,
    ROI_Y1,
    ROI_Y2,
    MIN_SATURATION,
    MIN_VALUE,
    TEXT_THRESHOLD,
    TEXT_PROTECTION_KERNEL_SIZE,
    MASK_KERNEL_SIZE,
    INPAINT_RADIUS,
)
from utils import get_output_parameters


def remove_watermark(
        input_path: Path,
        output_path: Path,
) -> bool:
    original = cv2.imread(
        str(input_path),
        cv2.IMREAD_COLOR,
    )

    if original is None:
        print(f"[ERROR] Cannot read: {input_path}")
        return False

    height, width = original.shape[:2]

    x1 = int(width * ROI_X1)
    x2 = int(width * ROI_X2)

    y1 = int(height * ROI_Y1)
    y2 = int(height * ROI_Y2)

    if x1 >= x2 or y1 >= y2:
        print(f"[ERROR] Invalid image dimensions: {input_path}")
        return False

    roi = original[y1:y2, x1:x2]

    hsv = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2HSV,
    )

    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    watermark_mask = (
            (saturation >= MIN_SATURATION)
            & (value >= MIN_VALUE)
    )

    mask = (
            watermark_mask.astype(np.uint8)
            * 255
    )

    gray = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2GRAY,
    )

    text_mask = (
            (gray < TEXT_THRESHOLD).astype(np.uint8)
            * 255
    )

    protect_kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (
            TEXT_PROTECTION_KERNEL_SIZE,
            TEXT_PROTECTION_KERNEL_SIZE,
        ),
    )

    protected_text = cv2.dilate(
        text_mask,
        protect_kernel,
        iterations=1,
    )

    mask[protected_text > 0] = 0

    mask_kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (
            MASK_KERNEL_SIZE,
            MASK_KERNEL_SIZE,
        ),
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        mask_kernel,
        iterations=1,
    )

    mask = cv2.dilate(
        mask,
        mask_kernel,
        iterations=1,
    )

    mask[protected_text > 0] = 0

    full_mask = np.zeros(
        (height, width),
        dtype=np.uint8,
    )

    full_mask[y1:y2, x1:x2] = mask

    result = cv2.inpaint(
        original,
        full_mask,
        INPAINT_RADIUS,
        cv2.INPAINT_TELEA,
    )

    full_text_mask = np.zeros(
        (height, width),
        dtype=np.uint8,
    )

    full_text_mask[y1:y2, x1:x2] = protected_text

    text_pixels = full_text_mask > 0

    result[text_pixels] = original[text_pixels]

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    parameters = get_output_parameters(
        output_path.suffix,
    )

    success = cv2.imwrite(
        str(output_path),
        result,
        parameters,
    )

    if not success:
        print(
            f"[ERROR] Cannot save: "
            f"{output_path}"
        )
        return False

    return True
