<h2>Получение атрибутов лица на основе DeepFace</h2>

Чтобы запустить достаточно сделать

`python3 -m venv env`<br>
`source env/bin/activate`<br>
`pip install -r requirements.txt`<br>
Если будет ошибка AttributeError: module 'cv2' has no attribute 'TrackerKCF_create', в консоли выполнить:<br>
`python -m pip install opencv-contrib-python`<br>
`python main.py`<br>
По умолчанию видеопоток будет запущен с фронтальной камеры. При необходимости
можно запустить с указанием характеристик:<br>
`python main.py --url_cam video_2022-04-16_20-27-16.mp4`<br>
для того, чтобы поток видео был из файла.