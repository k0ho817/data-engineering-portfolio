# 문경호 · 데이터 엔지니어 포트폴리오

[포트폴리오 사이트](https://k0ho817.github.io/data-engineering-portfolio/)

## 대표 내용

1. SQL·데이터 모델링: 따릉이 SQL 마트, Java·MySQL 팀 프로젝트, Spark SQL·ERD 학습.
2. 데이터 파이프라인: FineWeb 입력 표준화, 센서 데이터 정제, Spark ImageNet 전처리.
3. 연구·협업: DBLAB 분산 실행 비교, 벡터 검색 실험, Aquila, 스케줄 자동화.

2026-09-21: SQL과 데이터 품질을 중심으로 개편했습니다. SQL 자료 탭은 클릭과 좌우 방향키·Home·End로 전환할 수 있습니다.

[DBLAB 상세 기록](reports/dblab.md) · [SQL 구현과 검증](pipeline/README.md) · [자료 출처](ASSET_SOURCES.md)

## 재현

정적 사이트이므로 index.html을 열 수 있습니다. 외부 라이브러리·CDN·개발 서버가 필요하지 않습니다.

```sh
python3 pipeline/load.py assets/bike-hourly-source.csv --output assets
python3 -m unittest discover -s pipeline -v
python3 tests/verify_site.py
node tests/interaction.test.cjs
```

따릉이 SQL 마트는 2026-09-16에 기존 분석 데이터를 바탕으로 추가한 확장 구현입니다. 브라우저의 인쇄 / PDF 기능에서는 상세 내용을 펼쳐 인쇄합니다.
