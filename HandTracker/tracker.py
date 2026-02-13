import cv2
import mediapipe as mp
import time
import math
import pyautogui

pyautogui.PAUSE = 0
PRESS_DURATION = 0.1

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=0                
)

cv2.namedWindow("Hold My Line Piece", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hold My Line Piece", 1200, 900)

pTime = cTime = 0

LEFT = DOWN = -1
RIGHT = UP = 1
NONE = 0


class HandMovementTracker:
    def __init__(self, window_size = 3):
        self.previous_x = None
        self.position_history = []
        self.window_size = window_size
        self.threshold = 0.04 # percentage of screen width
    
    def HorizontalMovement(self, current_x):
        self.position_history.append(current_x)
        
        if len(self.position_history) > self.window_size:
            self.position_history.pop(0)
        
        # Calculate smoothed position (average)
        smoothed_x = sum(self.position_history) / len(self.position_history)
        
        if self.previous_x is None:
            self.previous_x = smoothed_x
            return NONE
        
        delta = smoothed_x - self.previous_x
        
        self.previous_x = smoothed_x
        
        # Determine direction
        if delta < -self.threshold:
            return LEFT
        elif delta > self.threshold:
            return RIGHT
        else:
            return NONE

class RotationDetector:
    def __init__(self):
        self.previous_angle = None
        self.rotate_threshold = 30
    
    def detect(self, handlandmarks):

        current_angle = calculate_angle(hand_landmarks)

        if self.previous_angle is None:
            self.previous_angle = current_angle
            return False
        
        delta = abs(self.previous_angle - current_angle)
        self.previous_angle = current_angle
        
        return delta > self.rotate_threshold

def hand_x(x_positions):
    
    if x_positions is None or len(x_positions) == 0:
        return None
    
    return sum(x_positions) / len(x_positions) 

print_list = ["" for i in range(10)]
def print_cv():
    global print_list
    
    for i in range(len(print_list)):
        y = (i) * 30 + 70 
        cv2.putText(
            frame, 
            print_list[i],
            (10, y),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0,255,0),
            1
        )

def squared_dist(landmark1, landmark2):
    x1,y1 = landmark1.x, landmark1.y
    x2,y2 = landmark2.x, landmark2.y
    return (x1 - x2)**2 + (y1 - y2)**2

def is_curled(hand_landmarks):
    
    '''
    Check ratio of tip-knuckle to knucle wrist.
    tip-knucle / knuckle wrist
    > 2/3 -> extended
    < 2/3 -> fist
    '''

    fingers = [
        (8, 5),   # Index
        (12, 9),  # Middle
        (16, 13), # Ring
        (20, 17), # Pinky
    ]

    curled_count = 4

    TIP = 0
    KNUCKLE = 1
    WRIST = 2

    for finger in fingers:

        tip = hand_landmarks.landmark[finger[TIP]]
        knuckle = hand_landmarks.landmark[finger[KNUCKLE]]
        wrist = hand_landmarks.landmark[WRIST]

        knuckle_wrist = squared_dist(knuckle, wrist)
        tip_wrist =  squared_dist(tip,wrist)

        if knuckle_wrist and tip_wrist/knuckle_wrist >= 2/3:
            curled_count -= 1
    
    return curled_count >= 3

def calculate_angle(hand_landmarks):
    
    '''
    Calculate general direction of the hand through the average of the angles from wrist to the 4 main fingers.
    '''

    fingers = [
        (8, 5),   # Index
        (12, 9),  # Middle
        (16, 13), # Ring
        (20, 17), # Pinky
    ]


    TIP = 0
    WRIST = 2

    angle = 0

    for finger in fingers:
        tip = hand_landmarks.landmark[finger[TIP]]
        wrist = hand_landmarks.landmark[WRIST]

        delta_y = tip.y - wrist.y
        delta_x = tip.x - wrist.x
        angle += math.degrees(math.atan2(-delta_y, delta_x))
    return angle / len(fingers)

def press(key):
    pyautogui.keyDown(key)
    time.sleep(PRESS_DURATION) 
    pyautogui.keyUp(key)


# Track each landmark
h_tracker = HandMovementTracker()
h_rotation = RotationDetector()


while True:
    success, frame = cap.read()
    # frame = cv2.resize(frame, (640, 480))
    if success:
        
        frame = cv2.flip(frame, 1)

        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(RGB_frame)
        
        is_fist = False
        gesture = "Not Fist"
        direction_x = 'NONE'
        angle = None
        rotated = False
        hand_x_pos = None

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                
                rotated = h_rotation.detect(hand_landmarks)
                angle = h_rotation.previous_angle

                if is_curled(hand_landmarks):
                    is_fist = True

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            hand_x_pos = hand_landmarks.landmark[0].x
            dir = h_tracker.HorizontalMovement(hand_x_pos) 

            if dir == LEFT:
                direction_x = 'LEFT'
            elif dir == RIGHT:
                direction_x =  'RIGHT'
            else:
                direction_x = 'NONE'

        if is_fist:
            gesture = "Fist"
        
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        print_list = [
            f"FPS = {int(fps)}",
            gesture,
            direction_x,
            f"{hand_x_pos}",
            f"Angle: {angle}",
            f"Rotated? {rotated}"
        ]
        print_cv()

        if is_fist:
            if direction_x == 'LEFT':
                press('left')
            elif direction_x == 'RIGHT':
                press('right')
        elif rotated:
                press('up')

        cv2.imshow("Hold My Line Piece", frame)
        
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()