
import sys
from analyzer.parser import analyze_test_results


def main():
    if len(sys.argv) < 2:
        print("사용법: python main.py <XML 파일 경로>")
        return

    xml_path = sys.argv[1]

    try:
        results = analyze_test_results(xml_path)

    except (FileNotFoundError, OSError, ValueError) as e:
        print(f"오류 발생: {e}")
        return

    print("\n===== QA Test Result Analyzer =====")
    print(f"TOTAL : {results['total']}")
    print(f"PASS  : {results['passed']}")
    print(f"FAIL  : {results['failed']}")
    print(f"SKIP  : {results['skipped']}")
    print("===================================")


if __name__ == "__main__":
    main()
