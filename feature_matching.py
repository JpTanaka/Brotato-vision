import cv2
import argparse
from pathlib import Path
import os

""" 
Draw matching for a single template images and a background image using SIFT algorithm

"""
def bf_matching(template_path : str, bkg_path : str, ratio_test : bool = True) -> None:
    # use colored images for printing
    colored_template_img = cv2.imread(template_path) 
    colored_bkg_img = cv2.imread(bkg_path)

    # use gray images for analysis
    template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE) 
    bkg_img = cv2.imread(bkg_path, cv2.IMREAD_GRAYSCALE)    
    
    sift = cv2.SIFT_create()

    kp_template, des_template = sift.detectAndCompute(template_img, None)
    kp_bkg, des_bkg = sift.detectAndCompute(bkg_img, None)
    
    bf = cv2.BFMatcher() 
    if ratio_test:  # Lowe's ratio test --> (short explanation: https://stackoverflow.com/questions/51197091/how-does-the-lowes-ratio-test-work)
        matches = bf.knnMatch(des_template, des_bkg, k = 2) # find two best matches for each keypoint
        good = []
        ctx = 0.8
        for m,n in matches:
            if m.distance < ctx * n.distance:
                good.append([m])
        res_img = cv2.drawMatchesKnn(colored_template_img, kp_template, colored_bkg_img, kp_bkg, good, None, flags = cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    else: 
        matches = bf.match(des_template, des_bkg) # find best match for each keypoint
        matches = sorted(matches, key=lambda x : x.distance) # sort by distance
        good = matches[:10] # get 10 closest kp
        res_img = cv2.drawMatches(colored_template_img, kp_template, colored_bkg_img, kp_bkg, good, None, flags = cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

    cv2.imshow("Feature Matching (SIFT)", res_img)

if __name__ == "__main__":
    # project_dir = Path(__file__).resolve().parent.parent
    project_dir = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(description="Feature Matching using SIFT for a single template and background image")

    parser.add_argument("--template", type=str, default=os.path.join(str(project_dir), "sprites", "baby_alien_1.png"), help="Path to template image")
    parser.add_argument("--background", type=str, default=os.path.join(str(project_dir), "samples", "sample_image.png"), help="Path to background image")
    parser.add_argument("--ignore_ratio_test", action="store_true", help="Do not use ratio test")
    args = parser.parse_args()
    
    template_path = args.template
    bkg_path = args.background
    ratio_test = False if args.ignore_ratio_test else True

    if not Path(template_path).is_file():
        raise FileNotFoundError(f"'{template_path}' not found")
    if not Path(bkg_path).is_file():
        raise FileNotFoundError(f"'{bkg_path}' not found")
    
    bf_matching(template_path, bkg_path, ratio_test)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
