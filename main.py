import sys

from processor import process_path


def main() -> None:
    if len(sys.argv) > 1:
        input_path = sys.argv[1]

    else:
        input_path = input(
            "Enter file or folder path: "
        ).strip()

        input_path = input_path.strip('"')

    if not input_path:
        print(
            "[ERROR] No path specified."
        )
        return

    process_path(input_path)


if __name__ == "__main__":
    main()
