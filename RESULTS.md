# API lab results
## Part 0
- Step 0.1, the number of pizza names: 18

- Step 0.3, status code of the request without a token: 401 (body: {"error":"authentication failed"})

- Step 0.4, the name of your pizza: The Fresh Frutti di Mare

- Step 0.12, results of the three runs without a session (optional): failed, failed, failed. Each run created the user with 201, then the login got 401, because without the AWSALB cookie the load balancer sent the login to a server that did not know the new user.

- Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2, 3. The original test covered only block 1. Block 3 (all three tools excluded) makes QuickPizza answer 500.

## Defect report

- Title: Excluding all three tools returns 500 with an empty body
- Request:

  ```
  POST https://quickpizza.grafana.com/api/pizza
  Authorization: token <token of a logged-in user>
  Content-Type: application/json

  {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
  ```

- Expected result: status 400 with a JSON error message that says no pizza can satisfy the restrictions.
- Actual result: status 500 with an empty body.
- Severity: Medium. The server crashes on a valid request that any customer can send, and the app that calls the API gets no message to show or act on. No data is lost, and the input is uncommon.

## Part A
- Step A4, status codes when the other user reads, changes and deletes:
## Part B
1.
2.
3.
4.
5.
6.
7.
8.