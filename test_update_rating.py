import pytest


# Updating stars saves 1 and 5, and refuses 0 and 6 without changing the rating.
@pytest.mark.parametrize("stars, status", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_boundary(api, auth, rating, stars, status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == status
    expected = stars if status == 200 else rating["stars"]
    after = api.get(path, headers=auth)
    assert after.status_code == 200
    assert after.json()["stars"] == expected