"""Regression test: get_descendants / get_ancestors must terminate on a
cyclic subclass graph (A subClassOf B subClassOf C subClassOf A).

Before commit 38e0883 the recursion inserted the current node and recursed
unconditionally, so a cycle caused unbounded recursion -> stack overflow.
The fix only recurses when HashSet::insert reports the node was newly added.
"""
import pyhornedowl

A = "http://example.com/A"
B = "http://example.com/B"
C = "http://example.com/C"

onto = pyhornedowl.open_ontology("test/cyclic.owx")
assert len(onto.get_classes()) == 3, onto.get_classes()

# If the cycle were not broken, either of these would recurse forever and
# crash the interpreter instead of returning.
for start in (A, B, C):
    descendants = pyhornedowl.get_descendants(onto, start)
    ancestors = pyhornedowl.get_ancestors(onto, start)
    # Every class is reachable both ways around the 3-cycle, and each set
    # includes the starting node itself.
    assert descendants == {A, B, C}, f"descendants({start}) = {descendants}"
    assert ancestors == {A, B, C}, f"ancestors({start}) = {ancestors}"
    print(f"start={start}: descendants={descendants} ancestors={ancestors}")

print("OK: cyclic hierarchy handled without infinite recursion")
