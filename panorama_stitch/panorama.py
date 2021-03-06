import numpy as np 
import imutils
import cv2

class Stitcher:
    def __init__(self):
        # check openCV version
        self.isv3 = imutils.is_cv3(or_better=True)

    def stitch(self, images, ratio=0.75, reprojThresh=4.0,
        showMatches=False):
        # unpack the images then detect keypoints and
        # extract local invariant descripttors from them
        (imageA, imageB) = images
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)
        
        # match features between the two images
        M = self.matchKeypoints(kpsA, kpsB,
            featuresA, featuresB, ratio, reprojThresh)
        
        # if the match is None then there aren't enough 
        # matched keypoints to create panorama
        if M is None:
            return None

        # otherwise, apply perspective warp to stitch 
        # the images together
        (matches, H, status) = M
        result = cv2.warpPerspective(imageA, H, 
            (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        # check if keypoint match needs to be visualized
        if showMatches:
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches,
                status)

            # return a tuple of the stitched image and the vis
            return (result, vis)

        
        # return the stitched image
        return result

    def detectAndDescribe(self, image):
        # conver the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # check if we're using OpenCV 3.X
        if self.isv3:
            # detect and extract features from image
            descriptor = cv2.xfeatures2d.SIFT_create()
            (kps, features) = descriptor.detectAndCompute(image, None)

            # otherwise of OpenCV 2.4.X
        else:
            # detect keypoints in image
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(gray)

            # extract the features from the image
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)

        # convert the keypoints from Object to Numpy array
        kps = np.float32([kp.pt for kp in kps])

        # return a tuple of keypoitns and features
        return (kps, features)

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,
        ratio, reprojThresh):
        # compute the raw matches and initialize the list of
        # actualmatches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = mathcer.knnMatch(featuresA, featuresB, 2)
        matches = [] 

        # loop over the matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of
            # each other (Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        
        # computing homography requires atleast 4 matches
        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (_, i) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
                reprojThresh)
            
            # return the matches along with homography matrix
            # and the status of each mathced point
            return (matches, H, status)

        # otherwise, no homography could be computed
        else:
            return None


    def drawMatches(seld, imageA, imageB, kpsA, kpsB, matches, status):
        # initialize the output visualization image
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, w), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, 0:wB] = imageB
        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # only process the match if the keypoint was matched
            # successfully
            if s == 1:
                # draw the match
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1])) 
                cv2.line(vis, ptsA, ptsB, (0, 255, 0), 1)
            
        # return the visualization
        return vis
