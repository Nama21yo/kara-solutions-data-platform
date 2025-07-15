from ultralytics import YOLO
import os
import psycopg2

IMAGE_DIR = "data/images/new/"
MODEL = YOLO('yolov8n.pt')

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

for img in os.listdir(IMAGE_DIR):
    if not img.lower().endswith((".png", ".jpg", ".jpeg")):
        continue
    image_path = os.path.join(IMAGE_DIR, img)
    # message_id is extracted from filename or a mapping table
    message_id = img.split("_")[0]

    results = MODEL(image_path)
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            cls_name = result.names[class_id]
            score = float(box.conf[0])
            cur.execute("""
                INSERT INTO fct_image_detections (message_id, detected_object_class, confidence_score)
                VALUES (%s, %s, %s)
            """, (message_id, cls_name, score))
    conn.commit()

cur.close()
conn.close()
