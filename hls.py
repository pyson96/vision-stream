import cv2
import subprocess
import sys

def main(video_source=0, output_path='/var/www/html/hls/stream.m3u8'):
    # OpenCV video capture
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Cannot open video source {video_source}", file=sys.stderr)
        sys.exit(1)

    # Retrieve properties
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS) or 25.0

    # FFmpeg command for HLS output
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f'{width}x{height}',
        '-r', str(fps),
        '-i', 'pipe:0',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-g', '50',
        '-sc_threshold', '0',
        '-f', 'hls',
        '-hls_time', '4',
        '-hls_list_size', '5',
        '-hls_flags', 'delete_segments',
        output_path
    ]

    # Start FFmpeg subprocess
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Write raw frame to FFmpeg stdin
            process.stdin.write(frame.tobytes())
    except BrokenPipeError:
        print("FFmpeg pipe closed", file=sys.stderr)
    finally:
        cap.release()
        process.stdin.close()
        process.wait()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Capture video with OpenCV and generate HLS via FFmpeg')
    parser.add_argument('--source', default=0, help='Video source (device index or file path)')
    parser.add_argument('--output', default='/var/www/html/hls/stream.m3u8',
                        help='HLS output .m3u8 path')
    args = parser.parse_args()
    main(video_source=args.source, output_path=args.output)
