from face_detector import FaceInfo
import argparse
import cv2

def main(args):

    streamer = FaceInfo(args.url_cam)
    streamer.face_analyze()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url_cam', help='url camera', default=0)
    args = parser.parse_args()
    main(args)


