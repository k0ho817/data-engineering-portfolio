# 따릉이 시간별 데이터 SQL 마트

2026-09-16에 기존 2023년 따릉이 분석용 CSV를 활용하여 추가한 포트폴리오 확장 구현입니다. 기존 연구 당시의 배포·운영 실적으로 소급하지 않습니다. Codex와 함께 구현하고 로컬에서 검증했습니다.

## 데이터와 모델

- 입력: `assets/bike-hourly-source.csv`. 기존 노트북 export의 dateTime, rental_count, temperature 열만 추출했습니다. 원천 대여 이력 전체를 다시 검증한 데이터는 아닙니다.
- 대상: 여의나루역 1번출구 앞 대여소, 2023년, 한국 현지 시간.
- `dim_station`: 대여소 차원 테이블.
- `fact_rental_hour`: 대여소·시간 복합 기본키, 0 이상의 정수 대여량, 기온.
- `mart_rental_day`: SQL GROUP BY로 일별 대여량·관측 시간 수·평균 기온을 집계하는 뷰.

## 실행

저장소 루트에서 Python 표준 라이브러리만으로 실행할 수 있습니다.

```sh
python3 pipeline/load.py assets/bike-hourly-source.csv --output assets
python3 -m unittest discover -s pipeline -v
```

기본값은 메모리 내 SQLite입니다. 지속 저장 시 `--database bike.sqlite`를 지정합니다.

## 검증 결과

- 8,758시간, 대여량 합계 119,605건.
- 2023년 기대 시간 8,760개 중 12월 31일 22시·23시 누락. 결측을 0건으로 대체하지 않고 `status=warning`으로 기록합니다.
- 입력을 두 번 적재한 후 전체 저장 행의 해시가 동일함을 확인했습니다.
- 수정된 시간대만 UPSERT로 갱신하고 다른 시간대는 보존하는 테스트를 통과했습니다.
- 중복 시간대, 음수·비정수·NaN 대여량을 거부합니다. 입력 전체 검증 이후 트랜잭션으로 반영하므로 잘못된 입력 배치가 기존 값을 부분 변경하지 않습니다.
- 삭제된 원천 행의 삭제 전파, 다중 대여소, 스케줄링, 알림, 운영 DB 동시성은 이번 범위에 포함하지 않습니다.

실행 산출물: `assets/bike-quality.json`, `assets/bike-daily.csv`.

`plot_benchmark.py`는 별도의 DBLAB 통계 CSV에서 비교 가능한 QLoRA 네 조건을 선택해 신뢰구간 차트를 만듭니다. 이 시각화에만 Matplotlib가 필요합니다.
