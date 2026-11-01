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
- Step A4, status codes when the other user reads, changes and deletes: read 404 {"error":"not found"}, change 400 {"error":"rating ID ... not found"}, delete 400 {"error":"rating ID ... not found"}

## Part B

1. **Your tests talk to a real server over the internet. Name two kinds of failure that they can find and a unit test with stubs cannot. Then give one reason to write unit tests with stubs as well.**

   Failure สองแบบที่ unit test ที่ใช้ stub หาไม่เจอ แบบแรกคือปัญหาที่ infrastructure ระหว่าง client กับโค้ด เช่น load balancer ใน Step 0.12 ที่ส่ง request login ไปยัง server ที่ไม่รู้จัก user ใหม่ ทำให้ login ได้ 401 แบบที่สองคือ server จริงพังเมื่อเจอ input จริง เช่น Defect 1 ที่ exclude ครบทั้งสาม tool แล้ว server ตอบ 500 พร้อม body ว่าง stub จะคืนค่าตามที่เรากำหนดไว้เท่านั้น จึงไม่มีทางเห็นปัญหาแบบนี้ แต่เรายังควรเขียน unit test ที่ใช้ stub ด้วย เพราะรันได้เร็ว ไม่ต้องใช้ network ไม่ flaky เพราะ server อื่น และชี้ได้ตรงว่า function ไหนผิด ขณะที่ API test บอกได้แค่ว่ามีอะไรสักอย่างพัง

2. **Why does every test create its own user with a new name, rather than use the public token? How will you apply the same idea to the shared shop or hotel in Project 2?**

   Public token เป็นของที่ทุกคนที่ฝึกบน QuickPizza ใช้ร่วมกัน คนอื่นจึงอาจแก้หรือลบ rating ของเราระหว่างที่ test กำลังรัน และ test ของเราก็อาจไปแก้ของคนอื่นด้วย การสร้าง user ใหม่ด้วยชื่อใหม่ทำให้แต่ละ test มีข้อมูลของตัวเองที่ไม่มีใครแตะได้ ทุก test จึงเป็นอิสระต่อกันและได้ผลเหมือนเดิมทุกครั้ง และชื่อแบบสุ่มก็ไม่ชนกับ user ที่มีอยู่แล้ว ใน Project 2 จะใช้เฉพาะ credential ของกลุ่มตัวเอง ให้ fixture สร้าง customer, cart หรือ booking ที่แต่ละ test ต้องใช้ด้วยชื่อที่ไม่ซ้ำ ลบทิ้งหลัง test จบ และจะไม่อ่านหรือแก้ข้อมูลของกลุ่มอื่น

3. **Explain in your own words why the tests send every request through one session. If you did Step 0.12, describe what happened in your three runs.**

   QuickPizza รันอยู่บนหลาย server หลัง load balancer และแต่ละ server เก็บ user แยกกัน Session จะเก็บ cookie AWSALB ที่ load balancer ส่งกลับมา ทุก request ในการรันจึงไปถึง server เดียวกัน user ที่สร้างใน request หนึ่งจึง login ได้ใน request ถัดไป ใน Step 0.12 ที่ไม่ใช้ session ทั้งสามรอบ fail หมด คือสร้าง user ได้ 201 แต่ login ได้ 401 เพราะ load balancer ส่ง request login ไปยัง server ที่ไม่เคยเห็น user ใหม่นั้น

4. **Which block of the excluded tools revealed the defect in Step 0.16? Why is a 500 with an empty body worse for an app that calls the API than a 400 with a message? Why does the test stay in the suite as xfail instead of being deleted?**

   Block "exclude ครบทั้งสาม tool" เป็น block ที่ทำให้เจอ defect การตอบ 500 พร้อม body ว่างแย่กว่า 400 ที่มีข้อความ เพราะแอปที่เรียก API แยกไม่ออกว่า input ของตัวเองผิด หรือ server พัง และไม่มีข้อความให้แสดงต่อผู้ใช้หรือใช้ตัดสินใจว่าต้องแก้อะไร Test นี้ยังอยู่ใน suite ในรูป xfail เพื่อให้ defect ยังมองเห็นได้ในทุกการรัน โดยไม่ทำให้ทั้ง suite เป็นสีแดง และเพราะตั้ง strict=True การรันจะ fail ทันทีที่ QuickPizza แก้ defect นี้แล้ว ซึ่งเป็นสัญญาณให้เราเอา mark ออก

5. **How many tests does base choice coverage need for the model in Step A1, and how many would all combinations coverage need? Show how you counted.**

   Base choice coverage ต้องใช้ 9 test คือ base test 1 test บวกกับ test สำหรับทุก block ที่ไม่ใช่ base อีก (3 − 1) + (4 − 1) + (2 − 1) + (3 − 1) = 2 + 3 + 1 + 2 = 8 รวมเป็น 1 + 8 = 9 ส่วน all combinations coverage ต้องใช้ 3 × 4 × 2 × 3 = 72 test

6. **In Step A4, which status codes did you get when the other user read, changed and deleted the rating? Which codes would you expect? Is the difference a defect? Explain.**

   User อื่นได้ 404 ตอนอ่าน rating ได้ 400 ตอนแก้ และได้ 400 ตอนลบ และเจ้าของอ่านซ้ำแล้วพบว่า rating ไม่เปลี่ยนเลยทุกครั้ง ผมคาดว่าควรได้ 404 ทั้งสามกรณี เพราะสำหรับ user คนนั้น rating นี้ไม่มีอยู่ และ 404 ยังช่วยซ่อนไม่ให้คนแปลกหน้ารู้ว่ามี rating id นี้อยู่จริงหรือไม่ ส่วน 403 Forbidden ก็ยอมรับได้เช่นกัน ความต่างนี้ถือเป็น defect แต่ระดับต่ำ เพราะ access control ทำงานถูกต้อง ไม่มีอะไรเปลี่ยน แต่ 400 หมายถึง input ผิดกฎของ API ทั้งที่ body {"stars": 5} ถูกต้องทุกอย่าง และข้อความ error ของ server เองก็บอกว่า "not found" นอกจากนี้สถานการณ์เดียวกันยังได้ status code สองแบบ ทำให้แอปต้องรับมือทั้งสองแบบ

7. **Create madeup.txt with a made-up token of 16 characters and run the curl command. What comes back? Is this a defect, and what could a stranger do with it on a real system?**

   Request ที่ใช้ token แต่งขึ้นเอง 0000000000000000 ได้ status 200 กลับมาพร้อมรายการ rating จำนวนมากที่ผมไม่เคยสร้าง นี่เป็น defect เพราะ QuickPizza เช็กแค่ว่า token ยาว 16 ตัวอักษร ไม่ได้เช็กว่าเป็น token ที่ได้จากการ login จริง Token สั้นอย่าง "token short" ถูกปฏิเสธด้วย 401 แต่ token อะไรก็ได้ที่ยาว 16 ตัวอักษรกลับใช้ได้ บนระบบจริง คนแปลกหน้าสามารถแต่ง token ขึ้นมาเองแล้วอ่านข้อมูลของ user คนอื่นได้ และถ้า operation อื่นตรวจ token แบบเดียวกัน ก็อาจสร้าง แก้ หรือลบข้อมูลในนามคนอื่นได้ด้วย ซึ่งเป็น security defect ระดับ critical สำหรับ QuickPizza อาจตั้งใจให้เป็นแบบนี้เพราะเป็นเว็บเดโมสำหรับฝึก แต่ก็แสดงให้เห็นว่า test ควรลองใช้ token ที่ server ไม่เคยออกให้ด้วย

8. **Name one thing that an API test checks better than a test through the web pages, and one thing that only a test through the web pages can check.**

   API test เช็ก status code ทุก field ใน JSON body และข้อความ error ได้โดยตรง และรันเร็วกว่า test ผ่านหน้าเว็บ อีกทั้งยังส่ง input ที่หน้าเว็บไม่มีทางยอมให้ส่งได้ เช่น 3.5 ดาว ดาวที่เป็น text หรือไม่มี field stars ซึ่งเป็นวิธีที่ Part A ใช้หาว่า server จัดการกับ input เหล่านี้อย่างไร ส่วนสิ่งที่มีแค่ test ผ่านหน้าเว็บเท่านั้นที่เช็กได้คือสิ่งที่ผู้ใช้เห็นและทำจริง เช่น หน้าเว็บแสดงข้อความ error ชัดเจนหรือไม่ ปุ่มและ layout ใช้งานได้หรือไม่ และหน้าเว็บตอบสนองต่อคำตอบของ API ถูกต้องหรือไม่