from flask import Flask, render_template, Response, request
from face_recog import load_known_faces, recognize_faces
import cv2, time, psycopg2, boto3, os

app = Flask(__name__)
known_faces, names = load_known_faces()
camera = cv2.VideoCapture(0)

# PostgreSQL connection
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    dbname=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS']
)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS faces (name TEXT, time TEXT, image_url TEXT);")
conn.commit()

# S3 client
s3 = boto3.client('s3')

def save_to_s3(image_bytes, filename):
    bucket = os.environ['S3_BUCKET']
    s3.put_object(Bucket=bucket, Key=filename, Body=image_bytes, ContentType='image/jpeg')
    return f"https://{bucket}.s3.amazonaws.com/{filename}"

def save_result(name, image_bytes):
    filename = f"{name}_{int(time.time())}.jpg"
    url = save_to_s3(image_bytes, filename)
    cur.execute("INSERT INTO faces VALUES (%s, %s, %s)", (name, time.ctime(), url))
    conn.commit()

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        results = recognize_faces(frame, known_faces, names)
        for name, (top, right, bottom, left) in results:
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)
            _, jpeg = cv2.imencode('.jpg', frame)
            save_result(name, jpeg.tobytes())
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "Face Recognition Backend Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)