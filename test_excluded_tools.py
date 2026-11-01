import pytest


# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize("excluded", [
    [],                         # block 0
    ["Knife"],                  # block 1
    ["Scissors"],               # block 1
    ["Knife", "Scissors"],      # block 2
])
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Block 3: a request that no pizza can satisfy gets 400 and a JSON error, never 500.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools returns 500 with an empty body",
    strict=True,
)
def test_all_tools_excluded_is_refused(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()