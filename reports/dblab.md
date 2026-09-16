# DBLAB 데이터 파이프라인 연구 기록

이 문서는 보관 중인 연구 코드·발표 자료·실험 결과를 토대로 작성한 포트폴리오 요약입니다. ImageNet 처리와 KubeRay 언어모델 실험은 같은 연구 활동의 서로 다른 실행이며 하나의 성능 개선 전후 실험으로 합치지 않습니다.

## ImageNet 데이터 준비

- 원본 이미지와 XML의 라벨 정보를 매핑합니다. XML bounding box로 이미지를 자른 실험은 아닙니다.
- 이미지를 224×224로 변환하고 PNG 바이트로 인코딩합니다.
- 이미지 바이트, 정답 라벨, 원본 경로, WNID를 Parquet에 저장합니다.
- 전처리 결과를 Ray Train의 PyTorch·TensorFlow 실행에서 공통 입력으로 사용합니다.
- 연구 문서상 데이터 규모는 train 1,281,167장, validation 50,000장입니다. 포트폴리오 작성 시 전체 원천 데이터 수를 다시 세지는 않았습니다.

![ImageNet 파이프라인](../assets/imagenet-pipeline.png)

문제 기록에는 전처리 종료 시 집계 오류, Parquet shard별 행 수 차이, worker별 batch 수 불균형, 학습 중 PNG 디코딩 비용이 포함돼 있습니다. 파일이 생성됐다는 사실과 데이터 행 수·완료 상태 확인을 구분하는 것이 중요했습니다.

## KubeRay 입력 제어와 관측

2026년 8~9월 결과 원장은 로컬 캐시, Ray Train과 Ray Data 입력 경로, DDP·FSDP 계열 실행을 구분합니다. 정식 다중 노드 비교에서는 2+2 GPU 배치를 통제했습니다. 문서에는 선읽기 진단에서 27.1k행·3.5GiB 입력이 발생하고 shard 내부 제한 읽기 적용 후 12행·약 61KiB로 감소한 기록이 있습니다. 이는 해당 진단 조건의 관측이며 모든 작업의 개선율은 아닙니다.

NVML 관측에서 GPU index 오류를 UUID 조회로 수정하고 잘못된 이전 관측값을 제외한 기록이 있습니다. PyTorch allocated, reserved, NVML은 의미가 달라 동일 수치처럼 취급하지 않았습니다.

## 반복 실험 분석

Gemma 4 E2B text-QLoRA, 대칭 2+2 GPU 조건에서 성공 실행의 외부 wall-time을 집계했습니다. 2026-09-16 자료 정리 과정에서 다음 네 행의 표본 수와 평균을 RUN_END 기록으로 재계산하여 기존 통계 CSV와 대조했습니다.

| 조건             | 관측 시간(초)           | 평균(초) |   n |
| ---------------- | ----------------------- | -------: | --: |
| DDP DataLoader   | 89, 87, 89, 88, 88      |    88.20 |   5 |
| DDP Ray Data     | 90, 94, 90, 89, 91      |    90.80 |   5 |
| FSDP2 DataLoader | 599, 573, 558, 567, 611 |   581.60 |   5 |
| FSDP2 Ray Data   | 567, 576, 580           |   574.33 |   3 |

![외부 실행 시간](../assets/qlora-wall-time.png)

신뢰구간은 Student t 기반 평균의 95% CI이며 원본 통계 CSV에서 읽어 시각화합니다. 학습 결과 수와 외부 타이머 표본 수는 다를 수 있습니다. 특히 마지막 조건은 학습 결과 5회 중 외부 시간 3회만 확보돼 있습니다.

원 보고서는 DataLoader 조건의 PyTorch peak를 DDP 20.62, FSDP2 15.81 GiB/GPU로, 평균 step을 각각 0.911, 17.898초로 기록합니다. 이 두 지표는 이번 작성에서 전체 rank 로그를 재집계하지 않았습니다. 메모리 절감과 시간 증가를 함께 해석하고 모델 품질 우위로 일반화하지 않습니다.

[전체 통계 CSV](../assets/benchmark-statistics.csv) · [네 조건의 실행별 시간](../assets/benchmark-run-times.csv)

## 리뷰 임베딩

기존 vector.ipynb에는 Polars 정제, Ko-SBERT 인코딩, Parquet 저장, Faiss Flat·IVFFlat·IVFPQ·HNSW 비교 코드가 있습니다. 저장 출력은 199,992개 리뷰와 768차원 임베딩을 보여줍니다. 단일 질의의 Flat 첫 결과 유사도는 0.8729이며 정확도나 Recall@k는 아닙니다.

## 자료 계보

| 범위      | 원본 프로젝트 내 자료                                                                                |
| --------- | ---------------------------------------------------------------------------------------------------- |
| ImageNet  | ray_imagenet_bench/docs/presentation_pipeline.md, preprocess_imagenet.py, 2026-04-28 파이프라인 PNG  |
| KubeRay   | kuberay-benchmark/RESULTS_SUMMARY.md, run_ray_train.py, common.py                                    |
| 반복 분석 | results/paper-statistics/training_wall_time_statistics.csv, STATISTICAL_REPORT.md, 성공 RUN_END 로그 |
| 리뷰      | DBLAB/study/vector_db_report/data/vector.ipynb의 셀 인덱스 5·17 저장 출력                            |

팀 연구 자료의 존재만으로 단독 구현이나 전체 서비스 운영을 주장하지 않습니다. 개인의 변경 이력·정확한 역할 분담을 대체하는 문서가 아닙니다. 내부 서버 경로·접속 정보가 포함된 원본 문서 전체는 게시하지 않았습니다.
