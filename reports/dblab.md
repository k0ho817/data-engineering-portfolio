# DBLAB 데이터 파이프라인 연구 기록

DBLAB에서 진행한 데이터 준비와 분산 학습 실험을 시간순으로 정리했습니다. 2026년 4~5월에는 ImageNet을, 8~9월에는 KubeRay 언어모델을 다뤘습니다.

## ImageNet 데이터 준비

- 원본 이미지와 XML에서 라벨 정보를 읽어 매핑합니다.
- 이미지를 224×224로 변환하고 PNG 바이트로 인코딩합니다.
- 이미지 바이트, 정답 라벨, 원본 경로, WNID를 Parquet에 저장합니다.
- 전처리 결과를 Ray Train의 PyTorch·TensorFlow 실행에서 공통 입력으로 사용합니다.
- 연구 문서에 기록된 데이터 규모는 train 1,281,167장, validation 50,000장입니다.

![ImageNet 파이프라인](../assets/imagenet-pipeline.png)

진행 과정에서는 전처리 종료 집계 오류, Parquet shard별 행 수 차이, worker별 batch 수 불균형, 학습 중 PNG 디코딩 비용을 확인했습니다. 이후 산출 파일뿐 아니라 행 수와 완료 상태까지 함께 확인하는 방식으로 점검 항목을 늘렸습니다.

## KubeRay 입력 제어와 관측

2026년 8~9월에는 로컬 캐시, Ray Train, Ray Data의 입력 경로를 나눠 기록하고, 다중 노드 비교는 2+2 GPU 배치로 맞췄습니다. 선읽기 문제를 확인한 진단 실행에서는 27.1k행·3.5GiB를 읽었고, shard 내부 제한을 적용한 실행에서는 12행·약 61KiB를 읽었습니다.

NVML의 GPU index 오류는 UUID 조회로 수정했습니다. 메모리는 PyTorch allocated, reserved, NVML 값을 각각 기록해 지표별 차이를 확인했습니다.

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

원 보고서에서 DataLoader 조건의 PyTorch peak는 DDP 20.62, FSDP2 15.81 GiB/GPU였고, 평균 step은 각각 0.911, 17.898초였습니다. FSDP2는 메모리를 줄였지만 실행 시간은 크게 늘어 두 지표를 함께 비교했습니다.

[전체 통계 CSV](../assets/benchmark-statistics.csv) · [네 조건의 실행별 시간](../assets/benchmark-run-times.csv)

## 리뷰 임베딩

기존 vector.ipynb에는 Polars 정제, Ko-SBERT 인코딩, Parquet 저장, Faiss Flat·IVFFlat·IVFPQ·HNSW 비교 코드가 있습니다. 저장 출력 기준으로 199,992개 리뷰를 768차원 임베딩으로 변환했습니다. 단일 질의의 Flat 첫 결과 유사도는 0.8729였습니다. 다음 단계는 반복 질의와 Recall@k를 추가하는 것입니다.

## 자료 계보

| 범위      | 원본 프로젝트 내 자료                                                                                |
| --------- | ---------------------------------------------------------------------------------------------------- |
| ImageNet  | ray_imagenet_bench/docs/presentation_pipeline.md, preprocess_imagenet.py, 2026-04-28 파이프라인 PNG  |
| KubeRay   | kuberay-benchmark/RESULTS_SUMMARY.md, run_ray_train.py, common.py                                    |
| 반복 분석 | results/paper-statistics/training_wall_time_statistics.csv, STATISTICAL_REPORT.md, 성공 RUN_END 로그 |
| 리뷰      | DBLAB/study/vector_db_report/data/vector.ipynb의 셀 인덱스 5·17 저장 출력                            |

각 실험은 DBLAB 공동 연구 환경에서 진행했습니다. 포트폴리오에는 제가 다룬 데이터 처리 흐름과 공개 가능한 결과를 중심으로 정리했습니다.
