# SQL·데이터 모델링 경험

## 따릉이 SQL 마트

기존 DBLAB 분석용 CSV를 사용해 2026년 9월에 구현했다. SQLite 차원·사실 테이블과 GROUP BY 뷰를 만들고 복합 기본키, 외래키, CHECK 제약조건을 적용했다. 적재 과정에는 UPSERT와 입력 검사를 넣었다.

소스와 실행 방법: [pipeline](../pipeline/README.md). 데이터 품질: [JSON](../assets/bike-quality.json).

입력은 기존 분석에서 만든 시간별 CSV다. 같은 파일을 다시 적재하는 경우, 일부 시간대가 수정된 경우, 잘못된 값이 들어온 경우를 각각 테스트했다.

## Java·MySQL 학생 관리 시스템

2022년 3인 팀 프로젝트에서 회원가입, 로그인, 학생 조회와 수정 기능을 맡았다. 화면에서 받은 값을 PreparedStatement의 조회 조건과 갱신 값으로 전달하고, 처리 결과를 다시 화면에 표시했다.

[팀 저장소](https://github.com/KNUTPatAMat/Integrated-Information-Student-Management-System)

전체 학생 조회는 먼저 학번 목록을 가져온 뒤 학생별 상세 정보를 반복해서 읽는다. JOIN을 사용하는 단일 쿼리로 바꾸고 쿼리 수와 응답 시간을 비교할 예정이다.

## Spark SQL·관계 모델링 학습

2025년 빅데이터 수업의 `week10-lab.ipynb`에서 주문·상품·고객 데이터를 결합하고 국가별 매출을 집계했다. SQL과 DataFrame API의 결과를 비교하고 윈도우 연산의 실행계획도 확인했다. 최신 주문, 순위, LAG, 이동평균은 주로 PySpark DataFrame API로 작성했다.

교과 실습은 제공된 코드에 풀이를 추가하는 방식이었다. Top-2 요구를 Top-3로 작성한 부분과 최근 7개 행을 달력상 7일로 해석한 부분은 다시 수정할 항목으로 기록했다.

2024년 데이터베이스 과제에서는 Hotel, Customer, Room, Reservation, Stay의 ERD와 MySQL Workbench 모델을 작성했다. 요구사항에서 엔터티와 관계를 정리한 뒤 기본키와 외래키를 배치했다.
