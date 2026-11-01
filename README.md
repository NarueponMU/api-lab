# api-lab

## Input domain model for POST /api/ratings

| Characteristic | Block | Value | Covered by |
|---|---|---|---|
| C1 Value of stars | below 1 | 0 | `test_stars_out_of_range[0]` |
| | 1 to 5 (base) | 3 | `test_base_choice_is_saved` |
| | above 5 | 6 | `test_stars_out_of_range[6]` |
| C2 Type of stars | whole number (base) | 3 | `test_base_choice_is_saved` |
| | decimal | 3.5 | `test_stars_decimal_is_refused` |
| | text | "3" | `test_stars_text_is_refused` |
| | missing | no field | `test_stars_missing_is_refused` |
| C3 Pizza | exists (base) | a new pizza | `test_base_choice_is_saved` |
| | does not exist | 999999999 | `test_pizza_not_found_is_refused` |
| C4 Token | the user's own (base) | from auth | `test_base_choice_is_saved` |
| | none | no header | `test_no_token_is_refused` |
| | wrong length | token short | `test_wrong_length_token_is_refused` |

Base choice coverage needs 1 + 2 + 3 + 1 + 2 = 9 tests, and all of them are in `test_create_rating.py`.

API tests for the QuickPizza demo site, written with pytest and requests.

## How to install

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## How to run

```
pytest -v
```

To save an HTML report of a full run:

```
pytest -v --html=report.html --self-contained-html
```