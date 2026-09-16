# 문경호 · 데이터 엔지니어 포트폴리오

[포트폴리오 사이트](https://k0ho817.github.io/data-engineering-portfolio/)

## 대표 내용

1. 데이터 엔지니어링: DBLAB 분산 전처리·Parquet·데이터 공급, 객체 로그 정제, 리뷰 임베딩.
2. 데이터 분석: 분산 실행의 시간·메모리 비교, 따릉이 분석과 SQL 품질 검증.
3. 기타 프로젝트: Aquila 팀 캡스톤, 스케줄 자동화. 기초 실습은 추가 학습 기록으로 정리.

[DBLAB 상세 기록](reports/dblab.md) · [SQL 구현과 검증](pipeline/README.md) · [자료 출처](ASSET_SOURCES.md)

## 재현

정적 사이트이므로 index.html을 열 수 있습니다. 외부 라이브러리·CDN·개발 서버가 필요하지 않습니다.

```sh
python3 pipeline/load.py assets/bike-hourly-source.csv --output assets
python3 -m unittest discover -s pipeline -v
```

SQL 확장은 2026-09-16에 Codex와 함께 구현한 별도 포트폴리오 작업입니다. 기존 DBLAB 연구의 당시 성과로 소급하지 않습니다. 브라우저의 인쇄 / PDF 기능에서는 상세 내용을 펼쳐 인쇄합니다.
