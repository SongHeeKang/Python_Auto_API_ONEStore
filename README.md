# Python_Auto_API_ONEStore

ONE store API 자동화 테스트 플랫폼(**onetests**)의 테스트 Suite를 Selenium으로 자동 실행하고, 결과를 수집해 **JANDI 웹훅**으로 리포트하는 Python 스크립트 모음입니다.

Jenkins 등 스케줄러에서 주기적으로 실행하여 QA / 상용 환경의 API 상태를 점검하는 용도로 만들어졌습니다.

## 동작 흐름

```
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────┐
│  run_*_suite.py      │ ──▶  │  get_*_result.py     │ ──▶  │  JANDI 채널  │
│  (Suite 실행 트리거)   │      │  (결과 수집 / 파싱)    │      │  (웹훅 알림)  │
└──────────────────────┘      └──────────────────────┘      └──────────────┘
        onetests 웹 UI 자동 조작 (Selenium + Chrome headless)
```

1. **Suite 실행** – onetests 사이트에 로그인 → Suites 메뉴 → SERVICE / SERVICE-VARIABLES 필터 선택 → 전체 Suite 체크 → 실행. 통신사(SKT / KT / LG)별로 새 탭을 열어 순차 실행하고, 마지막 Suite가 `Case(0/0)` 상태가 될 때까지 대기합니다.
2. **결과 수집** – 다시 로그인하여 Suite 결과 테이블을 파싱합니다. 실패 케이스가 있으면 상세 화면으로 진입해 `Status / Header / Body / Script` 판정 중 `BAD`가 있는 케이스의 제목과 *호출이력 상세 보기* 링크를 추출합니다.
3. **리포트 전송** – 통신사별 Passed / Failed 집계와 실패 상세 목록을 JANDI Connect 웹훅으로 POST합니다.

## 파일 구성

| 파일 | 역할 | 대상 환경 / Suite |
|---|---|---|
| `run_unittest_suite.py` | UNIT TEST Suite 실행 | QA – SKT / KT / LG |
| `run_scenariotest_suite.py` | SCENARIO TEST Suite 실행 | QA – SKT / KT / LG |
| `run_unittest_suite_Production.py` | UNIT TEST Suite 실행 (MEM / SAC / CCS만 선택) | 상용 – `PROD-AUTOMATION-UNITTEST` |
| `get_unittest_result.py` | UNIT TEST 결과 수집 및 JANDI 전송 | QA – SKT / KT / LG |
| `get_unittest_result_OSB.py` | UNIT TEST 결과 수집 (`[ERR]` 제외) | QA – OSB |
| `get_unittest_result_Production.py` | UNIT TEST 결과 수집 | 상용 |
| `get_scenariotest_result.py` | SCENARIO TEST 결과 수집 (복합 시나리오 41개) | QA – SKT / KT / LG |
| `get_scenariotest_result_OSB.py` | SCENARIO TEST 결과 수집 (복합 시나리오 21개) | QA – OSB |

### UNIT TEST 카테고리

결과 스크립트는 Suite 이름 접두어를 아래와 같이 매핑해 리포트합니다.

| 접두어 | 표시 이름 |
|---|---|
| `[ERR]` | 예외 관련 |
| `[MEM]` | 회원 관련 |
| `[SAC]` | SAC 단위 |
| `[CCS]` | CCS 단위 |

## 리포트 예시

```
QA환경 API Check [UNIT TEST]
실행시간 : 2024-01-01 09:00:00

※ [SKT QA환경 API Check]
예외 관련 = 95 Passed : 0 Failed (00:01:23)
회원 관련 = 40 Passed : 1 Failed (00:00:45)
SAC 단위 = 120 Passed : 0 Failed (00:02:10)
CCS 단위 = 60 Passed : 0 Failed (00:01:05)

*SKT API 호출 실패 내역
회원 관련
회원 정보 조회    http://onetests.onestorecorp.com/...

※ [KT QA환경 API Check]
...
```

## 요구 사항

- **Python 2.7** (`reload(sys)`, `print` 문 등 Python 2 전용 문법 사용)
- Google Chrome + 동일 버전의 [ChromeDriver](https://chromedriver.chromium.org/)
- Python 패키지

```bash
pip install selenium requests
```

> 스크립트는 `driver.find_element_by_*` 등 Selenium 3.x API를 사용합니다. Selenium 4 이상에서는 동작하지 않으므로 `pip install "selenium<4"`로 설치하세요.

## 설정

각 스크립트 상단에서 환경에 맞게 값을 수정합니다.

### ChromeDriver 경로

```python
# linux (Jenkins / headless)
driver = webdriver.Chrome('/chromedriver/chromedriver', chrome_options=options)
# windows
# driver = webdriver.Chrome('D:\Python\Chromedriver\chromedriver.exe', chrome_options=options)
```

`run_*` 스크립트는 기본으로 Linux + headless, `get_*` 스크립트는 Windows + GUI 브라우저로 설정되어 있습니다. 필요한 쪽의 주석을 해제하세요.

### 로그인 계정

```python
driver.find_element_by_name("username").send_keys("<onetests 계정>")
driver.find_element_by_name("password").send_keys("<비밀번호>")
```

### JANDI 웹훅

```python
jandi_url_HK = 'https://wh.jandi.com/connect-api/webhook/<team_id>/<token>'
```

JANDI Connect에서 *Incoming Webhook*을 생성해 발급받은 URL로 교체합니다.

## 실행

```bash
# 1. Suite 실행 (완료까지 대기)
python run_unittest_suite.py
python run_scenariotest_suite.py

# 2. 결과 수집 및 JANDI 전송
python get_unittest_result.py
python get_scenariotest_result.py
```

Jenkins에서는 `run_*` → `get_*` 순서로 Job을 구성하거나, 하나의 Shell 스텝에서 순차 실행하면 됩니다.

## 주의 사항

- **XPath 하드코딩** – onetests 웹 UI의 XPath / 요소 ID에 의존하므로 UI 변경 시 스크립트 수정이 필요합니다.
- **테이블 행 인덱스 하드코딩** – 결과 파싱 시 `tableRowNum = [1, 9, 17, 25]`와 같이 Suite 개수 × 8줄 간격으로 행을 읽습니다. Suite가 추가·삭제되면 이 값을 함께 갱신해야 합니다.
- **대기 시간** – `time.sleep()`과 `WebDriverWait`(최대 500 ~ 1000초)로 동기화하므로 네트워크 상황에 따라 타임아웃이 발생할 수 있습니다.
- **자격 증명 관리** – 계정 정보와 웹훅 URL은 소스에 직접 기재되어 있습니다. 공개 저장소에 올릴 경우 환경 변수나 별도 설정 파일로 분리하는 것을 권장합니다.
