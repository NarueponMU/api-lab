# Another user cannot read someone else's rating.
def test_other_user_cannot_read(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    print("read by other user:", res.status_code, res.text)
    assert 400 <= res.status_code <= 499
    after = api.get(path, headers=auth)
    assert after.status_code == 200
    assert after.json() == rating


# Another user cannot change someone else's rating.
def test_other_user_cannot_update(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 5}, headers=other_auth)
    print("update by other user:", res.status_code, res.text)
    assert 400 <= res.status_code <= 499
    after = api.get(path, headers=auth)
    assert after.status_code == 200
    assert after.json() == rating


# Another user cannot delete someone else's rating.
def test_other_user_cannot_delete(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    print("delete by other user:", res.status_code, res.text)
    assert 400 <= res.status_code <= 499
    after = api.get(path, headers=auth)
    assert after.status_code == 200
    assert after.json() == rating