# organize imports
import numpy as np
import cv2

cam0 = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(1)
#cam2 = cv2.VideoCapture(2)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out0 = cv2.VideoWriter('output.avi', fourcc, 40.0, (640, 480))
out1 = cv2.VideoWriter('output.avi', fourcc, 40.0, (640, 480))
#out2 = cv2.VideoWriter('output.avi', fourcc, 40.0, (640, 480))


# loop runs if capturing has been initialized. 
while(True):
    # reads frames from a camera 
    # ret checks return at each frame
    ret, frame = cam0.read()

    # output the frame
    out.write(frame)

    # The original input frame is shown in the window 
    cv2.imshow('Original', frame)

    # Wait for 'q' key to stop the program 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the window / Release webcam
cap.release()

# After we release our webcam, we also release the output
out.release()

# De-allocate any associated memory usage 
cv2.destroyAllWindows()
