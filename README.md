# 프로젝트 개요

이 프로젝트는 OpenCV를 통해 실시간 영상을 캡쳐한 후 YOLO를 통해 각 프레임을 DETECTING 한 후 FFmpeg를 사용해 인코딩하여, Nginx를 통해 HLS 파일을 서빙하여 브라우저에서는 Hls.js 기반 웹 플레이어로 스트림을 재생하는 구조를 갖습니다. 

## 주요 기능

- **hls.py**: OpenCV로 카메라 또는 비디오 파일에서 프레임을 캡처하고, FFmpeg 파이프를 통해 HLS(playlist.m3u8 + .ts 세그먼트) 스트림을 생성
- **index.html**: Hls.js를 활용해 `/hls/stream.m3u8` 스트림을 브라우저에서 재생
- **Nginx 설정**: HLS 파일(.m3u8, .ts)을 `/hls/` 경로로 서빙하도록 구성

## 요구 사항

- Python 3.7 이상
- `opencv-python` 패키지
- FFmpeg (시스템 PATH에 등록)
- Nginx (Windows용 Nginx 또는 Linux에서 사용 가능)
- 브라우저(Hls.js 지원)
- YOLO 


