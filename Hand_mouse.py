import cv2
import mediapipe as mp
import pyautogui
import time
import threading 
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
screen_width,screen_height = pyautogui.size()

lock = True

def delay():
   global lock
   time.sleep(1)
   lock = True


while True:
    success,img=cap.read()
    img = cv2.flip(img,1)
    img_rbg = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result = hands.process(img_rbg)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # thumb_coord = hand_landmarks.landmark[4]
            # thumb_x = int(thumb_coord.x*screen_width)
            # thumb_y = int(thumb_coord.y*screen_height)
            for id,lm in enumerate(hand_landmarks.landmark):
               
                if id == 8:
                    h,w,_ = img.shape
                    Ix, Iy = int(lm.x * w), int(lm.y * h)
                    screen_x,screen_y = int(screen_width*lm.x),int(screen_height*lm.y)
                    # Hx,Hy = int(w*thumb_coord.x),int(h*thumb_coord.y)
                    print(screen_x,screen_y)
                    if screen_y >= 0 and screen_x >= 0:
                        
                        pyautogui.moveTo(screen_x,screen_y)
                        cv2.circle(img, (Ix, Iy), 10, (0, 215, 0), cv2.FILLED)
                        # cv2.circle(img,(Hx,Hy),10,(0,100,0),cv2.FILLED)
                        
                        # if int(screen_x/32) == int(thumb_x/32) and int(thumb_y/32) == int(screen_y/32) and lock:
                        #     thread = threading.Thread(target=delay)
                        #     thread.start()
                        #     pyautogui.rightClick()
                        #     lock = False

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)


    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()    