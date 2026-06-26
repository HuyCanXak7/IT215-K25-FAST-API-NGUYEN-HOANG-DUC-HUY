(1) Phân tích lỗi

1.1 Trace luồng xử lý khi gọi /getStudents:

- B1 FastAPI nhận request
- B2 FastAPI tìm router trùng
+ nó sẽ tìm thấy @app.get("/getStudents")
+ sẽ gọi hàm get_students():
- B3 Hàm get_students(): sẽ được thực hiện
+ return "Danh sach sinh vien: " + str(students)
+ do str(students) nên nó sẽ chuyển thành chuỗi không phải dạng list của JSON nữa
- B4 FastAPI gữi chuỗi đó về Fontend

1.2 Giải thích vì sao FastAPI không nên trả về string trong API JSON:

- Do FastAPI gữi về chuỗi nên fontend sẽ bị lỗi fontend chỉ nhận list
+ Nếu gữi str cho fontend nó sẽ không xử lý được

1.3 Chỉ ra lỗi trong thiết kế REST endpoint (naming convention):

- trong bài dùng /getStudents
- Tên này chưa đúng chuẩn REST,REST quy ước:Không dùng động từ
- nên dùng là /students 