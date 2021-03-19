# python_project_zikcam

## index
※유튜브 나도코딩 강의 수강(https://www.youtube.com/watch?v=yQ20jZwDjTE)
<br>
※빵형의 개발도상국 참조(https://www.youtube.com/watch?v=cx7VONjFEE0&t=194s)

```sh
├─python_project_zikcam
│  main.py                   # 메인
│  docker-compose.yml
│  README.md                     
├─ videos
├─ video_result
```

# 프로젝트 개요
python 기본 gui 라이브러리인 'tkinter'와 비디오 라이브러리 'opencv'를 사용하여
동영상 직캠 프로그램 제작

# 프로젝트 한계
opencv의 tracker함수가 물체가 겹치는 부분일때 잘 인식하지 못하는 경우가 있다.
<br>
화질이 더 좋거나 하면 얼굴인식까지 해서 해당 인물을 tracking하는 기능으로 수정해야 할 듯
