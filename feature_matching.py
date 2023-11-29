import cv2
import numpy as np
import matplotlib.pyplot as plt

def bf_matching(template_path, bkg_path, ratio_test = True):
    template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE) 
    bkg_img = cv2.imread(bkg_path, cv2.IMREAD_GRAYSCALE)

    sift = cv2.SIFT_create()

    kp_template, des_template = sift.detectAndCompute(template_img, None)
    kp_bkg, des_bkg = sift.detectAndCompute(bkg_img, None)
    
    bf = cv2.BFMatcher() 
    if ratio_test:  # Lowe's ratio test --> (short explanation: https://stackoverflow.com/questions/51197091/how-does-the-lowes-ratio-test-work)
        matches = bf.knnMatch(des_template, des_bkg, k = 2) # find two best matches (closest) for each keypoint
        good = []
        ctx = 0.8 # adjust this value
        for m,n in matches:
            if m.distance < ctx * n.distance:
                good.append([m])
        res_img = cv2.drawMatchesKnn(template_img, kp_template, bkg_img, kp_bkg, good, None, flags = cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    else: 
        matches = bf.match(des_template, des_bkg) # find two best matches (closest) for each keypoint
        matches = sorted(matches, key=lambda x : x.distance) # sort by distance
        good = matches[:50] # get 50 closest kp
        res_img = cv2.drawMatches(template_img, kp_template, bkg_img, kp_bkg, good, None, flags = cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

    plt.imshow(res_img)
    plt.show()

if __name__ == "__main__":
    template_path = "sprites/baby_alien_img.png"
    bkg_path = "test.png"
    bf_matching(template_path, bkg_path, ratio_test = True)
