
import xml.etree.ElementTree as ET
from pathlib import Path


def analyze_test_results(xml_path):
    # 1. XML 파일 경로 확인
    xml_path = Path(xml_path)

    if not xml_path.is_file():
        raise FileNotFoundError(f"XML 파일을 찾을 수 없습니다: {xml_path}")

    # 2. XML 파일 읽기
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 3. 테스트 결과 저장
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }

    # 4. testcase 요소 순회
    for testcase in root.iter("testcase"):
        results["total"] += 1

        if testcase.find("failure") is not None:
            results["failed"] += 1

        elif testcase.find("error") is not None:
            results["failed"] += 1

        elif testcase.find("skipped") is not None:
            results["skipped"] += 1

        else:
            results["passed"] += 1

    return results
