import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face = mp.solutions.face_detection.FaceDetection(model_selection=0,min_detection_confidence=0.5)
cap=cv2.VideoCapture(0)
width=640
height=480
Known_distance = 70.0
Known_width = 15.0
counter = 0
window_open = False

def obj_data(img):
    obj_width=0
    image_input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = mp_face.process(image_input)
    if not results.detections:
       print("NO FACE")
    else: 
       for detection in results.detections:
           bbox = detection.location_data.relative_bounding_box
           x, y, w, h = int(bbox.xmin*width), int(bbox.ymin * height), int(bbox.width*width),int(bbox.height*height)
        #    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

           obj_width=w
       return obj_width
    
def Distance_finder(Focal_Length, Known_width, obj_width_in_frame):
    distance = (Known_width * Focal_Length)/obj_width_in_frame
    return distance   

while True:
    ret,frame=cap.read()
    frame=cv2.resize(frame,(640,480))

    obj_width_in_frame=obj_data(frame)
    if not obj_width_in_frame:
        print("NO FACE")
    else:
        Distance = Distance_finder(600, Known_width, obj_width_in_frame)


    if int(Distance) <= 90 and int(Distance) >= 50:
        # check if the window is closed
        if not window_open:
            # create a window to display the frame
            cv2.namedWindow("FRAME", cv2.WINDOW_NORMAL)
            window_open = True

        # display the distance in the frame
        # cv2.putText(frame, f"In Range: {int(Distance)} CM", (5, 25),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
        # show the frame
        cv2.imshow("FRAME",frame)

    else:
        # check if the window is open
        if window_open:
            # close the window
            cv2.destroyWindow("FRAME")
            window_open = False

        # display the distance in the console
       # print(f"Out of Range: {int(Distance)} CM")

    key = cv2.waitKey(1) & 0xFF # wait for key event (1 millisecond delay)
    if key == ord('s'): # if the 's' key is pressed
            cv2.imwrite(f'frame_{counter}.png', frame) # save current frame as 'frame.png' image file
            counter+=1
    elif key == 27: # if the 'Esc' key is pressed
        break

cap.release()
cv2.destroyAllWindows()