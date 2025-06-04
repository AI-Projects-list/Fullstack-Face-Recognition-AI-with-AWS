import face_recognition, cv2, os

def load_known_faces(path='models/known_faces'):
    known_faces = []
    names = []
    for file in os.listdir(path):
        img = face_recognition.load_image_file(f"{path}/{file}")
        encoding = face_recognition.face_encodings(img)[0]
        known_faces.append(encoding)
        names.append(os.path.splitext(file)[0])
    return known_faces, names

def recognize_faces(frame, known_faces, names):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)
    results = []

    for encoding, loc in zip(encodings, locations):
        matches = face_recognition.compare_faces(known_faces, encoding)
        name = "Unknown"
        if True in matches:
            index = matches.index(True)
            name = names[index]
        results.append((name, loc))
    return results