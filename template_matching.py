import cv2
import numpy as np
from copy import deepcopy
from typing import Optional
from pathlib import Path
import argparse

""" 
Insert new matching boxes if they do not intersect with current boxes.

"""
def insert_matching(match_locations : np.ndarray, template_shape : tuple[int,int], matched_regions : Optional[set] = None) -> set:
    new_matched_regions = deepcopy(matched_regions) if matched_regions != None else set()

    w, h = template_shape
    for loc in zip(*match_locations[::-1]):
        x, y = loc
        region = ((x, y), (x + w, y + h))

        is_duplicate = any(
            not ((x1 > x + w or x2 < x) or (y1 > y + h or y2 < y))
            for (x1, y1), (x2, y2) in new_matched_regions
        )
        if not is_duplicate:
            new_matched_regions.add(region)
    
    return new_matched_regions

"""
Calculate and draw matching for a list of template images and a background image

"""
def template_matching(background_path : str, template_paths : list[str], threshold : float = 0.8) -> None :
    background = cv2.imread(background_path)
    
    templates = [cv2.imread(template_path, 0) for template_path in template_paths]
    templates += [cv2.flip(template, 1) for template in templates]

    gray_background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    matched_regions = set()

    for template in templates:
        result = cv2.matchTemplate(gray_background, template, cv2.TM_CCOEFF_NORMED)
        match_locations = np.where(result >= threshold)
        matched_regions = insert_matching(match_locations, template.shape[::-1], matched_regions)

    print(matched_regions)

    for upleft, downright in matched_regions:
        cv2.rectangle(background, upleft, downright, (0, 0, 255), 2)
    
    cv2.imshow("Template Matching", background)

"""
Concatenate and print used template images

"""
def show_templates(template_paths : list[str]) -> None:
    colored_templates = [cv2.imread(template_path) for template_path in template_paths]
    max_height = max(template.shape[0] for template in colored_templates)
    resized_templates = [cv2.resize(template, (int(template.shape[1] * max_height / template.shape[0]), max_height)) for template in colored_templates]
    combined_templates = np.concatenate(resized_templates, axis=1)
    cv2.imshow("All templates", combined_templates)

if __name__ == "__main__":
    # project_dir = Path(__file__).resolve().parent.parent
    project_dir = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(description="Performs mulitple template matching for a set of template images and a background image")

    parser.add_argument("--object", type=str, default=None, help="Name of object to be matched. Only image names containing it a substring will be selected")
    parser.add_argument("--templates_dir", type=str, default=str(project_dir) + "/sprites", help="Name of folder containing template images")
    parser.add_argument("--background", type=str, default=str(project_dir) + "/background.png", help="Path to background image")
    parser.add_argument("--threshold", type=float, default = 0.25, help="Threshold value used in the algorithm")

    args = parser.parse_args()

    object_name = args.object
    templates_dir = args.templates_dir
    background_path = args.background
    threshold = args.threshold

    if object_name != None:
        template_paths = [str(item) for item in Path(templates_dir).iterdir() if object_name in item.stem]
    else:
        template_paths = [str(item) for item in Path(templates_dir).iterdir()]

    # template_paths = [
    #     # "sprites/baby_alien1.png",
    #     # "sprites/baby_alien2.png",
    #     "sprites/baby_alien3.png",
    # ]
        
    show_templates(template_paths)
    template_matching(background_path, template_paths, threshold)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
