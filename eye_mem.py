# organize imports
#import numpy as np
import cv2

cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 40.0, (1920, 1080))

# loop runs if capturing has been initialized. 
while(True):
    # reads frames from a camera 
    # ret checks return at each frame
    ret, frame = cam.read()
    #print(f"{frame.shape[0]} x {frame.shape[1]}")

    # output the frame
    out.write(frame)

    # The original input frame is shown in the window 
    cv2.imshow('Original', frame)

    # Wait for 'q' key to stop the program 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the window / Release webcam
cam.release()

# After we release our webcam, we also release the output
out.release()

# De-allocate any associated memory usage 
cv2.destroyAllWindows()
