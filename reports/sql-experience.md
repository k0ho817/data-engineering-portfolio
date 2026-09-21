# SQL·데이터 모델링 경험

## 따릉이 SQL 마트

기존 DBLAB 분석용 CSV를 대상으로 2026년 9월 추가한 확장 구현이다. SQLite의 차원/사실 테이블, 복합 기본키, 외래키, CHECK, GROUP BY 뷰, UPSERT 적재와 입력 검증을 포함한다.

소스와 실행 방법: [pipeline](../pipeline/README.md). 데이터 품질: [JSON](../assets/bike-quality.json).

입력 데이터는 기존 분석에서 만든 시간별 export다. 단일 대여소의 로컬 배치 적재를 대상으로 동일 입력 재실행, 수정 배치, 오류 입력 보존을 테스트했다.

## Java·MySQL 학생 관리 시스템

2022년 3인 팀 프로젝트. 회원가입·로그인·학생 조회·수정 기능을 맡아 팀원이 만든 DB 연결 계층과 연동했다. 사용자 입력이 PreparedStatement의 조회 조건과 갱신 값으로 전달되는 흐름을 경험했다.

[팀 저장소](https://github.com/KNUTPatAMat/Integrated-Information-Student-Management-System)

전체 학생 조회는 학번 목록 조회 후 학생별 조회를 반복한다. 일괄 조회 전환과 쿼리 수 측정은 후속 개선 항목이다.

## Spark SQL·관계 모델링 학습

2025년 빅데이터 수업의 `week10-lab.ipynb`에서 주문·상품·고객 데이터 결합과 국가별 매출 집계를 학습했다. SQL과 DataFrame API의 결과를 비교하며 윈도우 연산과 실행계획도 확인했다. 최신 주문·순위·LAG·이동평균 풀이 상당 부분은 PySpark DataFrame API다.

교과 실습에서는 제공 코드 위에 풀이를 작성했다. Top-2 요구에 Top-3로 작성한 부분과 최근 7개 행을 달력상 7일로 해석한 부분은 수정 과제로 남겼다.

2024년 데이터베이스 과제에서는 Hotel·Customer·Room·Reservation·Stay의 ERD와 MySQL Workbench 모델을 작성했다. 요구사항에서 엔터티와 관계를 찾고 기본키·외래키를 배치하는 연습이었다.
