
import sys
import xml.etree.ElementTree as ET

from analyzer.parser import analyze_test_results


def main():
    if len(sys.argv) < 2:
        print("사용법: python main.py <XML 파일 경로>")
        return

    xml_path = sys.argv[1]

    try:
        results = analyze_test_results(xml_path)

    except (OSError, ValueError, ET.ParseError) as e:
        print(f"오류 발생: {e}")
        return

    # 1. 전체 테스트 결과 출력
    print("\n===== QA Test Result Analyzer =====")
    print(f"TOTAL : {results['total']}")
    print(f"PASS  : {results['passed']}")
    print(f"FAIL  : {results['failed']}")
    print(f"SKIP  : {results['skipped']}")

    # 2. 실패 테스트 상세 정보 출력
    print("\n===== Failed Test Details =====")

    if not results["failures"]:
        print("실패한 테스트가 없습니다.")

    for failure in results["failures"]:
        print(f"\n[{failure['error_type']}]")
        print(f"Test: {failure['test_name']}")
        print(f"Class: {failure['class_name']}")
        print(f"Message: {failure['message']}")

    print("\n===================================")


if __name__ == "__main__":
    main()
