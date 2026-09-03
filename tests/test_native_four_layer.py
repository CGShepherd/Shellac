from generator.layout.native_four_layer import CONTRACT,audit,configure_layers
S='(kicad_pcb\n\t(layers\n\t\t(0 "F.Cu" signal)\n\t\t(31 "B.Cu" signal)\n\t)\n)'
def test_insert_and_audit():
    t=configure_layers(S); assert '"In1.Cu" power' in t and '"In2.Cu" power' in t; assert audit(t)==[]
def test_idempotent():
    t=configure_layers(S); assert configure_layers(t)==t
def test_routing_rejected(): assert audit(configure_layers(S)+'\n(segment foo)')
def test_manufacturer_neutral(): assert CONTRACT.fabrication_stack_policy=="manufacturer_standard_4_layer_stack" and CONTRACT.board_thickness_mm==1.6
