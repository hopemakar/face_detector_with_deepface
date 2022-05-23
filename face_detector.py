import cv2
from deepface import DeepFace
from time import sleep, time


class FaceInfo:

	def __init__(self, video):

		self.video = video


	def face_analyze(self):

		from cam_buffer import CamAsyncer
		frame = CamAsyncer(self.video)

		frame.start()
		while (1):

			if len(frame.for_detect) != 0:

				for i, face in enumerate(frame.for_detect):

					face_info = DeepFace.analyze(
						face,
						actions = ['age', 'gender', 'race', 'emotion'],
						enforce_detection=False)

					if 'instance_1' in face_info.keys(): 
						person = f"{i+1} face"
						sex = face_info['instance_1']['gender']
						age = face_info['instance_1']['age']
						race = face_info['instance_1']['dominant_race']
						emotion = face_info['instance_1']['dominant_emotion']
					else:
						person = f"{i+1} face"
						sex = face_info['gender']
						age = face_info['age']
						race = face_info['dominant_race']
						emotion = face_info['dominant_emotion']

					print(f"{person}\n{sex} {age} y.o.\n{race}\n{emotion}")




