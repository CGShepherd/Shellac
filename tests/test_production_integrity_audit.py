from generator.model.production_integrity_audit import *
def test_findings_are_well_formed(): validate_findings()
def test_later_controlled_closures_are_reflected():
 assert {x.identifier for x in closed_findings()}==CLOSED_IDS
 for ident,auth in (('AE071-F02','AE-074'),('AE071-F04','AE-075A'),('AE071-F05','AE-075B'),('AE071-F06','AE-075-B07'),('AE071-F07','AE-075G'),('AE036-F07','AE-076C'),('AE036-F08','AE-071B')):
  assert auth in next(x for x in FINDINGS if x.identifier==ident).resolution_evidence
def test_current_open_set_is_explicit():
 assert {x.identifier for x in open_findings()}==OPEN_IDS
 assert {x.identifier for x in routing_blockers()}==ROUTING_BLOCKER_IDS
def test_genuine_routing_blockers_remain_open():
 f03=next(x for x in FINDINGS if x.identifier=='AE071-F03'); f08=next(x for x in FINDINGS if x.identifier=='AE071-F08'); f05=next(x for x in FINDINGS if x.identifier=='AE036-F05')
 assert 'RUN10' in f03.summary and 'personality' in f08.summary and 'B.Cu' in f05.summary
 assert all(x.state=='OPEN' and x.routing_blocker for x in (f03,f08,f05))
