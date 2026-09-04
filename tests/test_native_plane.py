from generator.layout.native_plane import add_in1_zone,audit_in1_zone,discover_power_nets,deterministic_uuid
S='(kicad_pcb\n(layers\n (0 "F.Cu" signal)\n (2 "In1.Cu" power)\n (4 "In2.Cu" power)\n (31 "B.Cu" signal)\n)\n(net 0 "")\n(net 6 "0VA")\n(net 12 "+17V")\n(net 13 "-17V")\n)'
def test_power_net_discovery():
    p=discover_power_nets(S); assert p.zero_va==(6,"0VA") and p.positive_rail==(12,"+17V") and p.negative_rail==(13,"-17V")
def test_in1_zone_added_and_idempotent():
    t=add_in1_zone(S); assert deterministic_uuid("In1_0VA_zone") in t and audit_in1_zone(t)==[] and add_in1_zone(t)==t
def test_zone_binds_to_0va_net_id():
    t=add_in1_zone(S); assert '(net 6)' in t and '(net_name "0VA")' in t
