from pathlib import Path

from config import OUTPUT_SUFFIX
from utils import is_supported_image
from watermark import remove_watermark


def process_file(
        input_file: Path,
        output_root: Path,
        base_root: Path | None = None,
) -> bool:
    if base_root is None:
        relative_path = Path(input_file.name)
    else:
        relative_path = input_file.relative_to(
            base_root,
        )

    output_file = output_root / relative_path

    print(
        f"[PROCESSING] {input_file}"
    )

    success = remove_watermark(
        input_file,
        output_file,
    )

    if success:
        print(
            f"[OK] {output_file}"
        )
    else:
        print(
            f"[FAILED] {input_file}"
        )

    return success


def find_images(
        directory: Path,
        output_directory: Path,
) -> list[Path]:
    images = []

    for path in directory.rglob("*"):
        try:
            path.relative_to(output_directory)
            continue
        except ValueError:
            pass

        if is_supported_image(path):
            images.append(path)

    return sorted(images)


def process_directory(
        input_directory: Path,
) -> None:
    output_directory = (
            input_directory.parent
            / f"{input_directory.name}{OUTPUT_SUFFIX}"
    )

    images = find_images(
        input_directory,
        output_directory,
    )

    if not images:
        print(
            "[INFO] No supported images found."
        )
        return

    total = len(images)
    successful = 0
    failed = 0

    print(
        f"\nFound {total} image(s).\n"
    )

    for index, image in enumerate(
            images,
            start=1,
    ):
        print(
            f"[{index}/{total}] "
            f"Processing: {image}"
        )

        if process_file(
                image,
                output_directory,
                input_directory,
        ):
            successful += 1
        else:
            failed += 1

        print()

    print("=" * 50)
    print("Processing completed")
    print("=" * 50)
    print(f"Total:       {total}")
    print(f"Successful:  {successful}")
    print(f"Failed:      {failed}")
    print(f"Output:      {output_directory}")
    print("=" * 50)


def process_path(
        input_path: str,
) -> None:
    path = Path(input_path).expanduser()

    if not path.exists():
        print(
            f"[ERROR] Path does not exist:\n"
            f"{path}"
        )
        return

    if path.is_file():

        if not is_supported_image(path):
            print(
                f"[ERROR] Unsupported image format: "
                f"{path.suffix}"
            )
            return

        output_directory = (
                path.parent / "output"
        )

        success = process_file(
            path,
            output_directory,
        )

        print()

        if success:
            print(
                f"Done.\n"
                f"Output: {output_directory}"
            )
        else:
            print("Processing failed.")

        return

    if path.is_dir():
        process_directory(path)
        return

    print(
        f"[ERROR] Unsupported path type:\n"
        f"{path}"
    )
