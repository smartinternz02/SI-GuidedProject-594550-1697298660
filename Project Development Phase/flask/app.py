#importing the necessary libraries
import cv2
import numpy as np
import os
from flask import Flask,render_template,request




app = Flask(__name__)

#index route
@app.route('/')
def index():
    return render_template('index.html')

#process method
@app.route('/process',methods=['POST'])
def process():
    
    video_file = request.files['video']
    image_file = request.files['image']


    video_path = os.path.join('Flask/uploads', video_file.filename)
    image_path = os.path.join('Flask/uploads', image_file.filename)

    posList = np.load('Flask/uploads/parkingSlotPosition.npy')


    cap = cv2.VideoCapture(video_path)
    height = 0 
    width = 0

    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()


        if not ret:
            break

        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        blurred = cv2.GaussianBlur(grey, (3,3), 0)


        threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)


        median = cv2.medianBlur(threshold, 5)


        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(median, kernel,iterations=1)

        imgOverlay = frame.copy()


        freeSlots =[]
        freeSlotPosition = []


        for i, pos in enumerate(posList):
            x, y = pos
            imgCrop = dilated[y:y + height, x:x +width ]
            count= cv2.countNonZero(imgCrop)
            if count < 900:
                color = (0,255, 0)
                thickness = 2
                freeSlots.append(i +1)
                freeSlotPosition.append(pos)
            else:
                color = (0,0, 255)
                thickness = 2
            cv2.rectangle(imgOverlay, pos,(pos[0]+ width,pos[1] + height),color,thickness)
            cv2.putText (imgOverlay, str(i+1),(x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), thickness,cv2.LINE_AA)

        cv2.putText(imgOverlay, f'Free:{len(freeSlots)}/ {len(posList)}',(100,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2, cv2.LINE_AA)

        for slot, pos in zip(freeSlots, freeSlotPosition):
            cv2.putText(imgOverlay, f'Slot{slot}',(pos[0],pos[1]- 10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),thickness,cv2.LINE_AA)

        cv2.imshow("Car Parking Input", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return render_template('result.html', video_path=video_path,image_path=image_path,posList=posList)
#main 
if __name__ == '__main__':
    app.run(debug=True)
  




