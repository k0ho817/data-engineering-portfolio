# 포트폴리오 시각 자료 출처

모든 이미지는 보관 중인 실험 산출물, 발표 자료, 분석 노트북에서 추출하거나 실제 CSV 좌표를 다시 그린 결과입니다. 설명용 SVG와 임의 수치의 차트는 사용하지 않습니다.

| 프로젝트 | 표시 자료 | 원본 출처 | 해석 범위 |
| --- | --- | --- | --- |
| 분산 처리 | distributed-throughput.png | DBLAB/test/final_report_20260521 2/avg_images_per_sec.png | ImageNet1K, ViT-B/16, GPU 3개, 5 epoch 실험. DDP 81.36699, FSDP 78.97620, MWMS 76.8 img/s. 프레임워크 차이가 포함됨 |
| 로그·CSV | trajectory-recorded.png | DBLAB/study/report/trajectory.csv | 첫 10,000행에서 type=bus, objectid=790인 기록만 추출. 좌표 순서 그대로 표시하며 보간·필터링하지 않음. 전체 데이터의 대표성이나 필터 성능을 주장하지 않음 |
| 로그·CSV 보조 자료 | trajectory-7.png | DBLAB/study/report/report2.pptx, 슬라이드 9, ppt/media/image7.png | 버스 1368의 필터 적용 전·후 원본 캡처. 메인 차트의 버스 790과 다른 객체 |
| Aquila | aquila-29.png | Aquila_최종발표_최종.pptx, 슬라이드 6, ppt/media/image29.png | 발표 자료에 수록된 학습·검증 지표. 데이터셋 외부 일반화 성능을 의미하지 않음 |
| Prophet | prophet-components.png | DBLAB/study/prophet/season2.png 및 prophet_season.py | seed=0, 난수로 생성한 720일 합성 데이터의 성분 분해 실습. 실제 관측 데이터 아님 |
| 따릉이 | bike-result-0.png | DBLAB/study/report2/code/1826015문경호.ipynb, 셀 인덱스 32의 첫 PNG 출력 | 저장된 Actual vs Predicted 결과. 급증 구간의 오차와 음수 예측을 포함하며 성능 개선을 주장하지 않음 |
| 벡터 검색 | HTML 실행 기록 | DBLAB/study/vector_db_report/data/vector.ipynb, 셀 인덱스 5·17 | 199,992개 리뷰, 768차원, Flat 검색 첫 결과 유사도 0.8729. 단일 질의 결과이며 정확도 아님 |

`benchmark-summary.csv`는 원본 `final_benchmark_summary.csv`를 그대로 복사한 파일입니다. `trajectory-sample.csv`는 궤적 차트에 사용한 모든 좌표를 담습니다. 다른 PNG는 재생성하거나 수정하지 않고 원본 바이트를 보존했습니다.

로컬 study 폴더 구조에서 `python3 extract_assets.py`를 실행하면 자료 추출과 궤적 차트 생성을 재현할 수 있습니다. Python과 Matplotlib가 필요합니다. 노트북 전체, API 키, 원천 대용량 데이터는 배포 파일에 포함하지 않습니다.
