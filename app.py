from flask import Flask, Response
import cv2

# Create a new Flask web server
app = Flask(__name__)

# Create a VideoCapture object to read from the webcam (0 is for the default cam)
video: cv2.VideoCapture = cv2.VideoCapture(0)


def gen(video: cv2.VideoCapture):
    """
    Generate frame bytes from the video capture.

    """
    while True:
        # Read a new frame from the video capture
        success: bool, image = video.read()
        # Encode the frame as a JPEG image
        ret, jpeg = cv2.imencode('.jpg', image)
        # Convert the image to bytes
        frame = jpeg.tobytes()
        # Yield the frame bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/home')
def index() -> Response:
    """
    Video streaming route. Put this in the src attribute of an img tag.
    """
    global video
    # The response will a HTTP response, containing the video frames.
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, threaded=True)
