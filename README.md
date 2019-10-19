# trx_data.csv : danh sách 24429 user và số item mà họ đã mua
# number_bought.csv : ma trận biểu diễn số lượng mua của từng user/từng item
# matrix_bought.csv : ma trận biểu diễn từng user đã từng mua item này chưa, bằng cách đánh dấu là u[i,j] = 1 nếu user i đã mua item j và ngược lại, u[i,j] = 0 nếu user i chưa
# data_user_base_frame.csv : ma trận biểu diễn độ tương tự giữa các user.
# user_neighbor.csv : ma trận biểu diễn danh sách các 20 user có độ tương tự vs user i theo thứ tự tăng dần.

# test1.py : Từ file trx_data.csv, biến đổi được thành ma trận number_bought và lưu vào file number_bought
# test2.py : Từ ma trận number_bought, biến đổi được thành ma trận matrix_bought và lưu vào file matrix_bought.csv. Vì quá trình xử lý rất mất thời gian và file quá lớn nên ta có thể lấy tại địa chỉ: https://drive.google.com/open?id=1vh3ecImBt7QP7WaeCAUqSQDuiIfUMbmm
# test10.py : Từ ma trận matrix_bought, ta tính được khoảng cách giữa các user và được ma trận data_user_base_frame và lưu vào file data_user_base_frame.csv
# test11.py : Từ ma trận data_user_base_frame, ta tìm được danh sách các user có sở thích giống nhau nhất và được ma trận user_neighbor và lưu vào file user_neighbor.csv
# test15.py : Đưa ra danh sách 20 sản phẩm gợi ý cho user_id 
