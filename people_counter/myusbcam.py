import cv2
import numpy
import imutils
from imutils.video import VideoStream
from imutils.video import FPS

# define a video capture object
vid = cv2.VideoCapture(2)

# dimensions
H = None
W = None

while(True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # resize the frame to have a maximum width of 500 pixels (the
    # less data we have, the faster we can process it), then convert
    # the frame from BGR to RGB for dlib
    frame = imutils.resize(frame, width=500)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # if no frame dimensions, set them
    if H is None or W is None:
        (H, W) = frame.shape[:2]

    # start the frames per second throughput estimator
    fps = FPS().start()

    # draw horizontal line
    cv2.line(frame, (0, H // 2), (W, H // 2), (0, 0, 0), 3)

    #
    # Display the resulting frame
    cv2.imshow('frame', frame)

    # frame counter
    fps.update()

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# last post to counter before quiting

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
