# QA Test Result Analyzer

pytest가 생성한 JUnit XML을 읽어 **전체 테스트 수와 PASS·FAIL·SKIP을 집계하고, 실패 테스트의 상세 정보를 출력하는 Python CLI 도구**입니다.

테스트 실행 후 결과를 확인하는 반복 작업을 보조하기 위해 만들었습니다. XML 파싱, 오류 메시지 분류, CLI 출력을 모듈별로 분리하고 단위 테스트를 작성했습니다.

> **구현 범위:** 기존 XML 파일을 입력받아 콘솔에 분석 결과를 출력합니다. 브라우저 테스트 실행, 실제 장애 원인 확정, HTML 보고서 생성, CI 연동은 현재 구현 범위에 포함하지 않습니다.

## 1. 주요 기능

| 기능 | 현재 동작 |
| --- | --- |
| XML 파일 입력 | CLI 인자로 전달한 파일 경로 읽기 |
| 결과 집계 | XML의 `testcase` 요소를 순회해 TOTAL·PASS·FAIL·SKIP 계산 |
| 실패 상세 출력 | 테스트 이름, 클래스명, 분류 유형, 오류 메시지 출력 |
| 메시지 기반 분류 | ASSERTION·TIMEOUT·NETWORK·UNKNOWN 분류 |
| 입력 오류 처리 | 경로 누락 시 사용법 안내, 파일·XML 처리 오류 시 오류 메시지 출력 |
| 단위 테스트 | 파서 집계와 메시지 분류 검증 |

### 결과 집계 기준

| XML의 테스트 상태 | 집계 결과 |
| --- | --- |
| `failure` 또는 `error` 하위 요소가 있음 | FAIL |
| 위 요소가 없고 `skipped` 하위 요소가 있음 | SKIP |
| 위 요소가 모두 없음 | PASS |

`failure`와 `error`는 현재 하나의 FAIL 항목으로 합산합니다. XML 상위 요소의 요약 숫자를 그대로 읽는 대신, 개별 `testcase`를 기준으로 집계합니다.

### 오류 메시지 분류 기준

오류 요소의 `message` 속성을 우선 사용하고, 값이 없으면 요소 본문을 사용합니다. 앞뒤 공백을 제거한 메시지의 **첫 줄을 소문자로 변환한 뒤** 다음 순서로 확인합니다.

| 우선순위 | 첫 줄에 포함된 키워드 | 분류 |
| --- | --- | --- |
| 1 | `timeouterror` | TIMEOUT |
| 2 | `assertionerror` | ASSERTION |
| 3 | `networkerror`, `connectionerror`, `connectionrefusederror`, `net::err_` 중 하나 | NETWORK |
| 4 | 일치하는 키워드가 없거나 빈 메시지 | UNKNOWN |

이 분류는 오류 메시지에 기반한 규칙입니다. 예를 들어 TIMEOUT으로 분류되어도 UI 변경, 네트워크 지연, 잘못된 Locator 중 어느 것이 실제 원인인지는 별도 확인이 필요합니다. 키워드가 메시지의 두 번째 줄 이후에만 있으면 분류에 반영되지 않습니다.

## 2. 구조와 기술 스택

| 파일 | 역할 |
| --- | --- |
| [`main.py`](main.py) | CLI 인자 처리, 입력 오류 안내, 결과 출력 |
| [`analyzer/parser.py`](analyzer/parser.py) | XML 파싱, 집계, 실패 테스트 정보 추출 |
| [`analyzer/classifier.py`](analyzer/classifier.py) | 오류 메시지 기반 유형 분류 |
| [`tests/test_parser.py`](tests/test_parser.py) | 혼합 상태 XML의 집계와 실패 상세 검증 |
| [`tests/test_classifier.py`](tests/test_classifier.py) | 매개변수화한 메시지 분류 검증 |

- **Python 표준 라이브러리:** `xml.etree.ElementTree`, `pathlib`, `sys`
- **pytest:** 파서와 분류기 단위 테스트
- **Git / GitHub:** 코드 및 변경 이력 관리

분석기 실행에는 별도 외부 패키지가 필요하지 않습니다. 단위 테스트를 실행할 때는 pytest가 필요합니다. 현재 저장소에는 패키지 버전을 고정하는 의존성 파일이 없습니다.

## 3. 설치 및 실행

아래 명령은 **Windows PowerShell**, 저장소 루트 기준입니다. 가상환경의 Python을 직접 지정하므로 별도 활성화 없이 실행할 수 있습니다.

### 저장소 복제 및 가상환경 생성

```powershell
git clone https://github.com/HEECHANG96/qa-result-analyzer.git
cd qa-result-analyzer
python -m venv .venv
```

### 결과 XML 분석

```powershell
.\.venv\Scripts\python.exe main.py "XML 파일 경로"
```

예를 들어 저장소 루트에 `sample-result.xml`을 저장했다면 다음과 같이 실행합니다.

```powershell
.\.venv\Scripts\python.exe main.py sample-result.xml
```

경로에 공백이 포함되면 큰따옴표로 감싸고, 상대 경로는 명령을 실행하는 현재 폴더 기준으로 지정합니다. 실제 XML 경로를 인자로 전달해야 하며, `main.py`만 실행하면 사용법이 출력됩니다.

## 4. 입력과 출력 예시

아래는 [`tests/test_parser.py`](tests/test_parser.py)에서 사용하는 **테스트용 XML**입니다. 실제 네이버 서비스 테스트 결과와는 별개의 예시입니다. 내용을 `sample-result.xml`로 저장하면 앞의 명령으로 분석할 수 있습니다.

```xml
<testsuites>
    <testsuite name="pytest">
        <testcase name="test_pass" classname="tests.test_sample"/>
        <testcase name="test_assertion" classname="tests.test_sample">
            <failure message="AssertionError: assert False"/>
        </testcase>
        <testcase name="test_timeout" classname="tests.test_sample">
            <error message="TimeoutError: Locator.click failed"/>
        </testcase>
        <testcase name="test_skip" classname="tests.test_sample">
            <skipped message="Not implemented"/>
        </testcase>
    </testsuite>
</testsuites>
```

현재 코드에 위 XML을 전달해 확인한 출력입니다.

```text
===== QA Test Result Analyzer =====
TOTAL : 4
PASS  : 1
FAIL  : 2
SKIP  : 1

===== Failed Test Details =====

[ASSERTION]
Test: test_assertion
Class: tests.test_sample
Message: AssertionError: assert False

[TIMEOUT]
Test: test_timeout
Class: tests.test_sample
Message: TimeoutError: Locator.click failed

===================================
```

실패가 없는 XML에는 같은 집계 항목과 함께 `실패한 테스트가 없습니다.`를 출력합니다. 이때 SKIP이 있으면 해당 테스트는 PASS에 포함되지 않습니다.

## 5. 웹 테스트 자동화 프로젝트와의 연결

관련 프로젝트인 **[portfolio-test-automation](https://github.com/HEECHANG96/portfolio-test-automation)**에서 생성한 결과 XML을 입력으로 전달할 수 있습니다.

두 저장소를 같은 상위 폴더에 내려받고, 각 프로젝트의 실행 환경을 준비했다는 전제입니다.

1. `portfolio-test-automation` 루트에서 결과 XML을 생성합니다.

   ```powershell
   .\.venv\Scripts\python.exe -m pytest tests/ -v --junitxml=reports/result.xml
   ```

2. `qa-result-analyzer` 루트로 이동한 뒤 해당 XML을 분석합니다.

   ```powershell
   .\.venv\Scripts\python.exe main.py ../portfolio-test-automation/reports/result.xml
   ```

현재는 파일 경로를 통해 수동으로 연결하는 방식입니다. 테스트 실행부터 분석까지 자동으로 이어지는 파이프라인은 구현하지 않았습니다. 위 네이버 브라우저 테스트와 분석기의 연결 절차는 이번 문서 검증에서 재실행하지 않았습니다.

## 6. 단위 테스트

테스트 실행용 패키지를 설치한 뒤 실행합니다.

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

| 테스트 | 실행 항목 수 | 검증 범위 |
| --- | ---: | --- |
| `test_analyze_test_results` | 1 | 전체 4개, PASS 1개, FAIL 2개, SKIP 1개 집계 및 실패 상세·분류 확인 |
| `test_classify_failure` | 5 | ASSERTION·TIMEOUT·NETWORK·알 수 없는 메시지·빈 메시지 분류 |
| **합계** | **6** | 파서와 메시지 분류의 기본 동작 |

함수는 2개지만 분류 테스트에 5개 입력을 매개변수화하여, 총 6개 항목으로 수집됩니다.

### 문서 작성 시 검증 결과

- 검증일: 2026-11-07
- 기준 코드: [`4382201`](https://github.com/HEECHANG96/qa-result-analyzer/commit/438220170092a78cd9fe660880eef132a4dcbd08)
- 검증 환경: Linux / Python 3.12.14 / pytest 8.4.1
- 결과: **6 PASS · 0 FAIL**
- 별도 확인: 4절의 테스트용 XML을 CLI에 전달하여 집계와 상세 출력 일치 확인

위 결과는 문서 작성 환경의 실행 기록입니다. 사용자의 Windows 환경에서 다시 실행한 결과는 아닙니다.

## 7. 현재 한계와 다음 개선

| 현재 한계 | 다음 개선 방향 |
| --- | --- |
| 첫 줄의 고정 키워드만 사용해 유형을 분류 | 실제 pytest·Playwright 오류 예시를 모아 분류 정확도와 예외 조건 검증 |
| FAIL과 ERROR를 하나로 합산 | Assertion 실패와 실행 환경 오류의 별도 집계 검토 |
| XML 구조·스키마를 검증하지 않아 잘못된 종류의 XML도 0건으로 처리할 수 있음 | 입력 형식 검증과 명확한 오류 안내 |
| 파일 없음·잘못된 XML 등의 오류 처리 분기는 자동 테스트 미작성 | 오류 처리 분기의 단위 테스트 추가 |
| CLI 오류 시 메시지 출력 후 종료하며 비정상 종료 코드를 명시하지 않음 | 스크립트·CI에서 실패를 판단할 수 있는 종료 코드 정의 |
| 콘솔 출력과 수동 파일 입력 중심 | 결과 파일 저장 및 CI 연결 검토 |

현재 단위 테스트와 예시는 기본 XML 집계와 메시지 분류를 검증합니다. 다양한 JUnit XML 변형, 모든 오류 메시지, 실제 장애 원인 판별까지 검증한 것은 아닙니다.
