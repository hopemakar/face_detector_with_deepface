from time import sleep, time
import numpy as np
import cv2
from threading import Thread


class CamAsyncer:
    def __init__(self, video):

        self.for_detect = []
        self.camera = cv2.VideoCapture(video)
        self.started = False
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def start(self):
        self.started = True
        t = Thread(target=self.create_buffer, args=())
        t.daemon = True
        t.start()
        return self


    def create_buffer(self):

        kcf_tracker_1 = None
        kcf_tracker_2 = None

        while self.started:

            ret, frame = self.camera.read()
            # if frame.shape[0] >= 720:
            #     frame = cv2.resize(frame, (0,0), fx=0.8, fy=0.8)

            kcf_tracker_box_1 = None
            kcf_tracker_box_2 = None

            if kcf_tracker_1 is not None:
                ok, box = kcf_tracker_1.update(frame)
                if ok:
                    kcf_tracker_box_1 = box

            if kcf_tracker_2 is not None:
                ok, box = kcf_tracker_2.update(frame)
                if ok:
                    kcf_tracker_box_2 = box

            ###############################################################################################################
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(gray, 1.9, 2)

            ###############################################################################################################
            if len(faces) == 1 and kcf_tracker_1 is None:
                kcf_tracker_1 = cv2.TrackerKCF_create()
                (x, y, w, h) = faces[0]
                kcf_tracker_1.init(frame, (x, y, w, h))

            if len(faces) > 1 and (kcf_tracker_1 is None or kcf_tracker_2 is None):
                kcf_tracker_1 = cv2.TrackerKCF_create()
                kcf_tracker_2 = cv2.TrackerKCF_create()
                (x1, y1, w1, h1) = faces[0]
                kcf_tracker_1.init(frame, (x1, y1, w1, h1))
                (x2, y2, w2, h2) = faces[1]
                kcf_tracker_2.init(frame, (x2, y2, w2, h2))

            #############################################################################################################

            if kcf_tracker_box_1 is not None and kcf_tracker_box_2 is None:

                (x, y, w, h) = map(int, kcf_tracker_box_1)
                self.for_detect.append(frame[y-50:y+h+50, x-50:x+w+50])   #для модели

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) #тут отрисовка боксов, т.к. на фронте они сами рисуются
                cv2.putText(frame, '1', (x, y - 10),                         #то я их тут закоментила
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2, cv2.LINE_AA)

            ###############################################################################################################
            if kcf_tracker_box_1 is not None and kcf_tracker_box_2 is not None:

                (x1, y1, w1, h1) = map(int, kcf_tracker_box_1)
                (x2, y2, w2, h2) = map(int, kcf_tracker_box_2)

                self.for_detect.append(frame[y1-50:y1+h1+50, x1-50:x1+w1+50])
                self.for_detect.append(frame[y2-50:y2+h2+50, x2-50:x2+w2+50])

                cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)
                cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
                cv2.putText(frame, '1', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, '2', (x2, y2 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2, cv2.LINE_AA)


            cv2.imshow('Tracking example', frame)

            interrupt = cv2.waitKey(10)

            if interrupt & 0xFF == ord('q'):
                break
            self.for_detect = []



        self.camera.release()
        cv2.destroyAllWindows()



