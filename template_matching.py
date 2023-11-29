import cv2
import numpy as np


def template_matching(image_path, template_paths, threshold=0.8):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    matched_regions = set()

    for template_path in template_paths:
        template = cv2.imread(template_path, 0)

        result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)

        for loc in zip(*locations[::-1]):
            x, y = loc
            w, h = template.shape[::-1]
            region = (x, y, x + w, y + h)

            is_duplicate = any(
                not ((x1 > x + w or x2 < x) or (y1 > y + h or y2 < y))
                for x1, y1, x2, y2 in matched_regions
            )
            if not is_duplicate:
                matched_regions.add(region)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    print(matched_regions)
    cv2.imshow("Image with Matches", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    template_paths = [
        "sprites/baby_alien_img.png",
        "sprites/baby_alien_img2.png",
    ]
    image_path = "test.png"
    threshold = 0.2

    template_matching(image_path, template_paths, threshold)
