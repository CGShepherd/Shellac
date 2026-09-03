from generator.layout.native_copper_preflight import inspect_native_board,validate_preflight
S='(kicad_pcb\n(layers\n (0 "F.Cu" signal)\n (2 "In1.Cu" power)\n (4 "In2.Cu" power)\n (31 "B.Cu" signal)\n)\n(net 0 "")\n(net 1 "0VA")\n(net 2 "+17V")\n(net 3 "-17V")\n(gr_line (start 0 0) (end 1 0) (layer "Edge.Cuts"))\n(gr_line (start 1 0) (end 1 1) (layer "Edge.Cuts"))\n(gr_line (start 1 1) (end 0 1) (layer "Edge.Cuts"))\n(gr_line (start 0 1) (end 0 0) (layer "Edge.Cuts"))\n)'
def test_preflight_identifies_0va():
    x=inspect_native_board(S); validate_preflight(x); assert x.zero_va_net_id==1 and x.zero_va_name=='0VA'
def test_preflight_counts_copper_state():
    x=inspect_native_board(S); assert x.segment_count==0 and x.via_count==0 and x.zone_count==0
def test_exact_0va_wins_over_generic_ground_name():
    x=inspect_native_board(S.replace('(net 2 "+17V")','(net 2 "GND")')); assert x.zero_va_name=='0VA'
