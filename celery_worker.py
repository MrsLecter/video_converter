from celery import Celery
import ffmpeg
import sys
import uuid
from src.constants import OUTPUT_FOLDER
app = Celery('celery_worker', backend='rpc://', broker='pyamqp://')

@app.task
def toMP3(filename):

    try:
        (
            ffmpeg.input(filename)
            .audio
            .output(OUTPUT_FOLDER + filename + '_output' + str(uuid.uuid4()) + '.mp3')
            .run()
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), sys.stderr)
        sys.exit(1)


@app.task
def getGIF(in_filename, out_filename,start, duration, width):
    try:
        (
            ffmpeg
            .input(in_filename, ss=start, t=duration)
            .filter('scale', width, -1)
            .output(out_filename)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), sys.stderr)
        sys.exit(1)
