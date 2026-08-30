from tools.ae019_design_record_reconcile import scan
def test_scan(tmp_path):
 (tmp_path/"docs").mkdir(); (tmp_path/"docs/DR-001.md").write_text("DR-001 Status SELECTED")
 r=scan(tmp_path); assert r[0][1]==["DR-001"]; assert "SELECTED" in r[0][2]
