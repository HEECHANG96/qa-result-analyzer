
import xml.etree.ElementTree as ET
from pathlib import Path

from analyzer.classifier import classify_failure


def analyze_test_results(xml_path):
    # 1. XML 파일 경로 확인
    xml_path = Path(xml_path)

    if not xml_path.is_file():
        raise FileNotFoundError(
            f"XML 파일을 찾을 수 없습니다: {xml_path}"
        )

    # 2. XML 파일 읽기
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 3. 테스트 결과 저장
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "failures": []
    }

    # 4. 각 테스트 케이스 분석
    for testcase in root.iter("testcase"):
        results["total"] += 1

        test_name = testcase.get("name", "UNKNOWN_TEST")
        class_name = testcase.get("classname", "")

        # 실패 또는 에러 요소 확인
        failure = testcase.find("failure")

        if failure is None:
            failure = testcase.find("error")

        # 5. 실패 테스트 상세 정보 추출
        if failure is not None:
            results["failed"] += 1

            error_message = (
                failure.get("message")
                or failure.text
                or ""
            ).strip()

            error_type = classify_failure(error_message)

            results["failures"].append({
                "test_name": test_name,
                "class_name": class_name,
                "error_type": error_type,
                "message": error_message
            })

        # 6. 건너뛴 테스트 확인
        elif testcase.find("skipped") is not None:
            results["skipped"] += 1

        # 7. 정상 통과 테스트
        else:
            results["passed"] += 1

    return results
