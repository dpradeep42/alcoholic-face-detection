"""Crop a license-plate region from a still vehicle photo.

The steps match ``VehicleDetection/NumberDetection.ipynb``: bilateral filter,
Canny edges, and the largest four-sided contour. OCR and the Google Sheet
append live in that notebook and need Tesseract plus a service-account key.
"""

import argparse
import os
import sys

import cv2


def find_plate(image):
    """Return the plate crop, or None when no four-sided region is found."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 90, 90)
    edges = cv2.Canny(blur, 30, 200)
    found = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = found[0] if len(found) == 2 else found[1]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            if w == 0 or h == 0:
                continue
            return image[y : y + h, x : x + w]
    return None


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(
        description="Crop a license plate from a vehicle photo."
    )
    parser.add_argument(
        "image",
        nargs="?",
        default=os.path.join(here, "data", "images", "car_3.jpg"),
        help="Path to a vehicle image (default: data/images/car_3.jpg)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Where to write the crop. Omit to only print the result.",
    )
    args = parser.parse_args(argv)

    image = cv2.imread(args.image)
    if image is None:
        print(f"Could not read image: {args.image}", file=sys.stderr)
        return 1

    plate = find_plate(image)
    if plate is None:
        print(f"No plate region found in {args.image}", file=sys.stderr)
        return 1

    print(f"{args.image}: plate crop shape={tuple(plate.shape)}")
    if args.output:
        if not cv2.imwrite(args.output, plate):
            print(f"Could not write {args.output}", file=sys.stderr)
            return 1
        print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
