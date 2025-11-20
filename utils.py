import time

def countdown(frame, seconds, cv2):
    for i in range(seconds, 0, -1):
        temp = frame.copy()
        cv2.putText(temp, f"{i}",
                    (280, 250), cv2.FONT_HERSHEY_DUPLEX,
                    3, (255,255,255), 5)
        cv2.imshow("Guess The Hero!", temp)
        cv2.waitKey(700)
