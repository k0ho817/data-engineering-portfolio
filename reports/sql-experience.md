# SQL·데이터 모델링 경험

## 따릉이 SQL 마트

기존 DBLAB 분석용 CSV를 대상으로 2026년 9월 Codex와 함께 추가한 확장 구현이다. SQLite의 차원/사실 테이블, 복합 기본키, 외래키, CHECK, GROUP BY 뷰, UPSERT 적재와 입력 검증을 포함한다.

소스와 실행 방법: [pipeline](../pipeline/README.md). 데이터 품질: [JSON](../assets/bike-quality.json).

학부 연구 당시 운영한 SQL 시스템으로 소급하지 않는다. 원천 대여 이력 전체가 아니라 기존 분석 export를 사용했다. 동일 입력 재실행·수정 배치·오류 입력 보존 테스트를 포함하며 운영 동시성과 스케줄링은 범위 밖이다.

## Java·MySQL 학생 관리 시스템

2022년 팀 프로젝트. 회원가입·로그인·학생 조회·수정 기능 관련 본인 계정의 커밋을 확인했다. DB 연결 및 SQL 주요 계층은 팀원의 구현으로 구분한다. 사용자의 입력을 DB 접근 계층과 연결한 경험이며 전체 스키마와 SQL의 단독 설계를 주장하지 않는다.

[팀 저장소](https://github.com/KNUTPatAMat/Integrated-Information-Student-Management-System)

전체 학생 조회는 학번 목록 조회 후 학생별 조회를 반복한다. 일괄 조회 전환과 쿼리 수 측정은 후속 개선 항목이다.

## Spark SQL·관계 모델링 학습

2025년 빅데이터 수업의 `week10-lab.ipynb`에서 주문·상품·고객 데이터 결합과 국가별 매출 집계를 학습했다. SQL과 DataFrame API의 결과를 비교하며 윈도우 연산과 실행계획도 확인했다. 최신 주문·순위·LAG·이동평균 풀이 상당 부분은 PySpark DataFrame API다.

수업 제공 코드와 풀이가 섞인 자료이며 독립 구축 프로젝트가 아니다. Top-2 요구에 Top-3로 작성된 부분과 최근 7개 행을 달력상 7일로 해석할 수 있는 부분은 추가 검증 대상이다. 성능 개선 실적으로 제시하지 않는다.

2024년 데이터베이스 과제에서는 Hotel·Customer·Room·Reservation·Stay의 ERD와 MySQL Workbench 모델을 작성했다. 설계 산출물과 실제 서비스 구축 경험은 구분한다. 교과 원문과 팀원의 자료는 이 저장소에 복제하지 않았다.
