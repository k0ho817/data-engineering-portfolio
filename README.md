# 문경호 · 데이터 엔지니어 포트폴리오

[포트폴리오 사이트](https://k0ho817.github.io/data-engineering-portfolio/)

## 소개

DBLAB에서 온프레미스 서버를 관리하고 분산 학습용 데이터 파이프라인을 구축했습니다. 로그와 지표로 문제를 확인하고, 해결 과정은 코드와 문서로 남기는 방식으로 일합니다.

문제 해결 순서:

`탐구 → 실행 → 관측 → 검증 → 해결 → 기록·공유`

## 대표 프로젝트

1. **온프레미스 인프라 복구**
   - 15개 노드의 실제 상태 조사
   - 11개 노드 복구
   - A100 MIG 구성과 가용 노드 10GbE 연결
   - 운영 현황 문서화와 공유
2. **Ray 데이터·학습 파이프라인**
   - ImageNet 원본과 라벨을 Parquet로 통합
   - NFS, Ray Data, Ray Train으로 이어지는 데이터 공급 경로 구성
   - shard 편차, PNG 디코딩 비용과 선읽기 범위 점검
3. **분산학습 벤치마크**
   - 대칭 2+2 GPU 배치와 공통 실행 환경 적용
   - DDP, FSDP2, DataLoader, Ray Data 반복 비교
   - 외부 시간, step 구간, PyTorch·NVML 메모리 기록

## SQL·데이터베이스

- **따릉이 SQL 마트:** SQLite 차원·사실 모델, 일별 집계 뷰, UPSERT와 입력 검증
- **Java·MySQL:** 회원가입, 로그인, 학생 정보 조회·수정 기능
- **Spark SQL:** 주문·상품·고객 조인, GROUP BY와 윈도우 연산
- **PostgreSQL:** 프로젝트 개발 중

## 기타 프로젝트

- **Aquila:** 탑다운 사람 데이터셋, YOLOv8n, DDP 학습과 Raspberry Pi 추론 조건 조정
- **벡터 검색:** 199,992개 리뷰의 768차원 임베딩과 Faiss·Milvus 색인 실험

## 확인

```sh
python3 pipeline/load.py assets/bike-hourly-source.csv --output assets
python3 -m unittest discover -s pipeline -v
python3 tests/verify_site.py
node tests/interaction.test.cjs
```

외부 라이브러리나 개발 서버 없이 `index.html`로 실행되는 정적 사이트입니다.
