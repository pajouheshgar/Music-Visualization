import os
import cv2
import pyrr
import cairosvg
import numpy as np
from time import time
from functools import wraps
import moviepy.editor as mpe
import scipy.io.wavfile as wavfile

import visualization.parametric.utils.svg3d as svg3d
from visualization.parametric.shapes.doughnut import Doughnut

from preprocessing.bar_extraction import extract_bar_cqt
from visualization.parametric.transformations.deformations import RandomNoise
from visualization.parametric.transformations.rotations import XRotation


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts))
        return result

    return wrap


L = pyrr.vector.normalize(np.float32([0, 0, -1.0]))
H = pyrr.vector.normalize(np.float32([0.0, -1.0, -1.0]))

Shininess = 100.0


def frontface_shader(winding, face):
    if winding < 0:
        return None
    p0, p1, p2 = pyrr.Vector3(face[0]), pyrr.Vector3(face[1]), pyrr.Vector3(face[-1])
    N: np.array = pyrr.vector.normalize(pyrr.vector3.cross(p1 - p0, p2 - p0))
    df = max(0, np.dot(-L, N)) * 0.9
    sf = pow(max(0, np.dot(-H, N)), Shininess)
    color = df * np.float32([1, 1, 0]) + sf * np.float32([1, 1, 1])
    color = np.power(color, 1.0 / 2.2)
    return dict(
        fill=svg3d.rgb(*color), fill_opacity='1.0',
        stroke='black', stroke_width='0.001')


@timing
def main(wav_file, output_file, duration=10, fps=30):
    view = pyrr.matrix44.create_look_at(
        eye=[0, 0, 120], target=[0, 0, 0], up=[0, 1, 0]
    )
    projection = pyrr.matrix44.create_perspective_projection(
        fovy=15, aspect=1, near=10, far=200
    )
    camera = svg3d.Camera(view, projection)

    style = dict(
        fill="white",
        fill_opacity="0.75",
        stroke="black",
        stroke_linejoin="round",
        stroke_width="0.0005",
    )

    video = cv2.VideoWriter("temp.avi", 0, fps, (512, 512))
    sr, wav_data = wavfile.read(wav_file)
    wav_data = np.mean(wav_data, axis=1)
    cqt_split, times = extract_bar_cqt(sr, wav_data)

    t = 0
    pointer = 0
    delta_r = 3.0 / fps
    R = 10
    r = 3
    start_flag = False
    while True:
        cqt = cqt_split[pointer]
        low_freq = np.mean(cqt[17])
        print(low_freq)
        print(t)
        if t >= times[0]:
            start_flag = True
        if t >= times[pointer]:
            delta_r *= -1.0
            pointer += 1

        if start_flag:
            r += delta_r

        shape = Doughnut({"R": R, "r": r})
        shape = shape.add_transformation(RandomNoise({"distortion": 15 / (np.abs(low_freq) ** 2)})).add_transformation(
            XRotation({"angle": t * 20}))
        faces = shape.get_faces(resolution=(50, 20), triangular=True)
        mesh = svg3d.Mesh(faces, shader=frontface_shader)
        view = svg3d.View(camera, svg3d.Scene([mesh]))
        svg3d.Engine([view]).render("temp.svg")
        cairosvg.svg2png(url="temp.svg", write_to="temp.png")
        image = cv2.imread("temp.png")
        video.write(image)
        t += 1 / fps
        if t >= duration:
            break

    cv2.destroyAllWindows()
    video.release()

    video_clip = mpe.VideoFileClip('temp.avi').set_duration(duration)
    audio_clip = mpe.AudioFileClip(wav_file).set_duration(duration)
    final_audio = mpe.CompositeAudioClip([audio_clip])
    final_clip = video_clip.set_audio(final_audio)
    final_clip.write_videofile(output_file, fps=fps)
    os.remove("temp.png")
    os.remove("temp.svg")
    os.remove("temp.avi")


if __name__ == '__main__':
    main("../../dataset/wav/SanTropez.wav", "out.mp4", duration=120, fps=25)
