from generator.kicad_erc import summarise_erc_report


def test_erc_report_summary_is_deterministic_and_category_based():
    report = """ERC report
[pin_not_connected]: Pin not connected
[label_dangling]: Label not connected
[pin_not_connected]: Pin not connected
"""
    assert summarise_erc_report(report) == {
        "label_dangling": 1,
        "pin_not_connected": 2,
    }
