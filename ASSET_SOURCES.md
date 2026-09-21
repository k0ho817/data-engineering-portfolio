# 포트폴리오 시각 자료 출처

## 2026-09 개편에서 추가한 자료

| 표시 자료                         | 출처·처리 방식                                                                                              |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| imagenet-pipeline.png             | gpu08의 ray_imagenet_bench/docs에 보관된 2026-04-28 원본 파이프라인 PNG. 바이트 수정 없이 복사              |
| benchmark-statistics.csv          | storage_cp의 kuberay-benchmark/results/paper-statistics/training_wall_time_statistics.csv 복사              |
| qlora-wall-time.png               | 위 통계 CSV의 E2B text-QLoRA 네 조건으로 재생성. 원본의 평균·CI·n을 사용. pipeline/plot_benchmark.py로 재현 |
| benchmark-run-times.csv           | 성공 RUN_END에서 추출한 네 조건의 외부 실행 시간                                                           |
| bike-hourly-source.csv            | DBLAB/study/report2/code/data.csv의 dateTime, rental_count, temperature 세 열을 추출. 8,758행               |
| bike-daily.csv, bike-quality.json | pipeline/load.py의 SQL 집계 및 검사 결과. 기존 시간별 CSV의 대여량 합계는 119,605건                         |

현재 페이지에는 대표 프로젝트의 PNG만 사용했습니다. SQL 마트는 기존 분석 CSV를 이용해 2026-09-16에 새로 구현했습니다.

## 기존 자료

2026-09-21 개편에서 SQL 코드와 근거 문서를 추가했습니다. 화면의 SQL은 `pipeline/schema.sql`에서 가져왔습니다. FineWeb 수치는 2026년 8월 공유 저장소에 기록된 메타데이터 값으로, 문서 50,000개와 시퀀스 104,683개, 시퀀스 길이 512, 잔여 토큰 152개입니다. Spark와 Milvus 구현은 [데이터 처리 기록](reports/data-pipelines.md)에, MySQL 담당 기능과 교과 실습은 [SQL 기록](reports/sql-experience.md)에 정리했습니다. 내부 서버 수집본과 인증 설정, 교과 원문은 각 작업 환경에서 관리합니다.

이미지는 실험 산출물, 발표 자료와 분석 노트북에서 추출했습니다. 궤적 그림은 실제 CSV 좌표로 다시 그렸습니다.

| 프로젝트           | 표시 자료                  | 원본 출처                                                                | 해석 범위                                                                                                                                                |
| ------------------ | -------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 분산 처리          | distributed-throughput.png | DBLAB/test/final_report_20260521 2/avg_images_per_sec.png                | ImageNet1K, ViT-B/16, GPU 3개, 5 epoch. DDP 81.36699, FSDP 78.97620, MWMS 76.8 img/s. 프레임워크별 실행 조건 포함                                      |
| 로그·CSV           | trajectory-recorded.png    | DBLAB/study/report/trajectory.csv                                        | 첫 10,000행 중 type=bus, objectid=790인 좌표 231개. 원본 순서로 표시한 무보간 표본                                                                    |
| 로그·CSV 보조 자료 | trajectory-7.png           | DBLAB/study/report/report2.pptx, 슬라이드 9, ppt/media/image7.png        | 버스 1368의 필터 적용 전·후 원본 캡처. 메인 차트의 버스 790과 다른 객체                                                                                  |
| Aquila             | aquila-29.png              | Aquila*최종발표*최종.pptx, 슬라이드 6, ppt/media/image29.png             | 발표 자료에 수록된 데이터셋 내부 학습·검증 지표                                                                                                         |
| Prophet            | prophet-components.png     | DBLAB/study/prophet/season2.png 및 prophet_season.py                     | seed=0으로 생성한 720일 합성 데이터의 성분 분해 실습                                                                                                    |
| 따릉이             | bike-result-0.png          | DBLAB/study/report2/code/1826015문경호.ipynb, 셀 인덱스 32의 첫 PNG 출력 | 저장된 Actual vs Predicted 결과. 급증 구간의 오차와 음수 예측 포함                                                                                      |
| 벡터 검색          | HTML 실행 기록             | DBLAB/study/vector_db_report/data/vector.ipynb, 셀 인덱스 5·17           | 199,992개 리뷰의 768차원 임베딩. 단일 질의에서 나온 Flat 첫 결과 유사도 0.8729                                                                           |

`benchmark-summary.csv`는 `final_benchmark_summary.csv`의 복사본입니다. `trajectory-sample.csv`에는 궤적 그림에 사용한 좌표가 모두 들어 있습니다. 나머지 PNG는 원본 바이트 그대로 보관했습니다.

로컬 study 폴더에서 `python3 extract_assets.py`를 실행하면 자료 추출과 궤적 그림 생성을 재현할 수 있습니다. 실행 환경에는 Python과 Matplotlib가 필요합니다. 전체 노트북과 API 키, 대용량 원천 데이터는 로컬 연구 환경에서 관리합니다.
