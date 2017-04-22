import tvm

def test_for():
    ib = tvm.ir_builder.create()
    n = tvm.var("n")
    A = ib.allocate("float32", n, name="A", scope="global")
    with ib.for_range(0, n, name="i") as i:
        A[i] = A[i] + 1
        with ib.for_range(0, 10, name="j") as j:
            A[j] = A[j] + 2

    body = ib.get()
    print(body)
    assert isinstance(body, tvm.stmt.AttrStmt)
    body = body.body
    assert isinstance(body, tvm.stmt.Allocate)
    body = body.body
    assert isinstance(body, tvm.stmt.For)
    body = body.body
    assert isinstance(body, tvm.stmt.Block)
    assert isinstance(body.rest, tvm.stmt.For)

def test_if():
    ib = tvm.ir_builder.create()
    n = tvm.var("n")
    A = ib.pointer("float32", name="A")
    with ib.for_range(0, n, name="i") as i:
        with ib.if_scope((i % 2) == 0):
            A[i] = A[i] + 1
        with ib.else_scope():
            A[0] = A[i] + 2

    body = ib.get()
    assert isinstance(body, tvm.stmt.For)
    body = body.body
    assert isinstance(body, tvm.stmt.IfThenElse)
    assert isinstance(body.then_case.index, tvm.expr.Var)
    assert body.else_case.index.value == 0

if __name__ == "__main__":
    test_if()
    test_for()
