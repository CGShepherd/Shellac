from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "test_ae071_prerouting_reconciliation.py",
    "test_ae071a_sch101_migration.py",
    "test_ae071b_native_mechanical_ownership.py",
    "test_ae074_dr039_product_migration.py",
    "test_ae075_b07_cartridge_harness.py",
    "test_ae075a_placement_and_sense_cap.py",
    "test_ae075b_configuration_coherence.py",
    "test_ae075b_xlr_lt5400_service_hardware.py",
    "test_ae075c_control_hardware_reconciliation.py",
    "test_ae075d_control_stack_discriminator.py",
    "test_ae075e_shared_ck_local_control_ownership.py",
    "test_ae075f_control_module_partition.py",
    "test_ae075g_output_interface_phase1.py",
    "test_ae075g_output_interface_phase2.py",
]

FORBIDDEN = {
    "absolute live product-population count": re.compile(r"len\(contract\.board_population_refs\)\s*==\s*\d+"),
    "whole live pre-RUN08 prerequisite equality": re.compile(r'hold\["pre_run08_prerequisites"\]\s*=='),
    "historical test pins live hold authority": re.compile(r'hold\["authority"\]\s*=='),
    "historical test pins live final-routing permission": re.compile(r'hold\["permissions"\]\["final_routing"\]'),
    "historical test pins exact current blocker set": re.compile(r"set\(blockers\)\s*=="),
}

def test_recent_assurance_tests_do_not_pin_mutable_live_state():
    failures = []
    for name in TARGETS:
        text = (ROOT / "tests" / name).read_text(encoding="utf-8")
        for reason, pattern in FORBIDDEN.items():
            if pattern.search(text):
                failures.append(f"{name}: {reason}")
    assert failures == [], "\n".join(failures)
