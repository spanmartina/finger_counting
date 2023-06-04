import cv2
import time
import hand_tracking as htm

# wCam, hCam = 640, 480

# open video capturing
cap = cv2.VideoCapture(0)
# give a size to the cam
# cap.set(3, wCam)
# cap.set(4, hCam)

previous_time = 0
detector = htm.handDetector(detectionCon=0.75)

#based on the tip of the fingers we can decide if they are open or close
tipids = [4, 8, 12, 16, 20]
#ex: number 8 below nr 6 -> closed


while True:
    success, img = cap.read() #reads our frame
    img = cv2.flip(img, 1)
    img = detector.findHands(img)

# create a list of the hand marks that we detect
    lmList = detector.findPosition(img, draw= False)

# if we find landmarks we do something
    if len(lmList) != 0 and len(lmList) == 21:
        fingerlist = []

        # thumb and dealing with flipping of hands
        if lmList[12][1] > lmList[20][1]:
            if lmList[tipids[0]][1] > lmList[tipids[0] - 1][1]:
                fingerlist.append(1)
            else:
                fingerlist.append(0)
        else:
            if lmList[tipids[0]][1] < lmList[tipids[0] - 1][1]:
                fingerlist.append(1)
            else:
                fingerlist.append(0)

        # others
        for id in range(1, 5):
            if lmList[tipids[id]][2] < lmList[tipids[id] - 2][2]:
                fingerlist.append(1)
            else:
                fingerlist.append(0)

        if len(fingerlist) != 0:
            fingercount = fingerlist.count(1)


        cv2.putText(img, f'Total fingers: {str(fingercount)}', (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (19, 19, 127), 3)

    #write the fps
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f'FPS: {int(fps)}', (0, 70), cv2.FONT_HERSHEY_PLAIN,
                2, (19, 19, 127), 3)
    # cv2.putText(img, (fps), (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)





    cv2.imshow("Finger Counting", img)
    #waitKey(1) - 1 milisecond delay to see our images
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break