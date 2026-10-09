
from analyzer.parser import analyze_test_results


def test_analyze_test_results(tmp_path):
    # 1. 테스트용 XML 데이터
    xml_content = """
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
    """

    # 2. 임시 XML 파일 생성
    xml_file = tmp_path / "result.xml"
    xml_file.write_text(xml_content, encoding="utf-8")

    # 3. XML 분석 실행
    results = analyze_test_results(xml_file)

    # 4. 테스트 결과 검증
    assert results["total"] == 4
    assert results["passed"] == 1
    assert results["failed"] == 2
    assert results["skipped"] == 1

    # 5. 실패 원인 분류 검증
    assert len(results["failures"]) == 2

    assert results["failures"][0]["test_name"] == "test_assertion"
    assert results["failures"][0]["error_type"] == "ASSERTION"

    assert results["failures"][1]["test_name"] == "test_timeout"
    assert results["failures"][1]["error_type"] == "TIMEOUT"
