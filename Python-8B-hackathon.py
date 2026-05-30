import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError:
        pass

def calculate_rank(avg_score):
    if avg_score < 5.0:
        return "Yếu"
    elif avg_score < 7.0:
        return "Trung Bình"
    elif avg_score < 8.0:
        return "Khá"
    else:
        return "Giỏi"

def input_score(subject_name):
    while True:
        try:
            score_str = input(f"Nhập điểm môn {subject_name}: ").strip()
            score = float(score_str)
            if 0 <= score <= 10:
                return score
            print("[Lỗi] Điểm số nhập vào phải nằm trong khoảng từ 0.0 đến 10.0!")
        except ValueError:
            print("[Lỗi] Định dạng không hợp lệ! Vui lòng nhập vào một số thực.")

student_list = load_data()

while True:
    print("\n===== HỆ THỐNG QUẢN LÝ SINH VIÊN =====")
    print("1. Hiển thị danh sách sinh viên")
    print("2. Thêm mới sinh viên")
    print("3. Cập nhật thông tin sinh viên")
    print("4. Xóa sinh viên")
    print("5. Tìm kiếm sinh viên")
    print("6. Sắp xếp danh sách sinh viên")
    print("7. Thống kê điểm TB")
    print("8. Liệt kê sinh viên có điểm TB cao nhất / thấp nhất")
    print("9. Phân loại học lực sinh viên")
    print("10. Thoát")
    print("======================================")

    menu_choice = int(input("Nhập lựa chọn của bạn (1-10): ").strip())
    match menu_choice:
        case 1:
            print("\n--- DANH SÁCH SINH VIÊN HIỆN TẠI ---")
            if not student_list:
                print("Danh sách sinh viên hiện đang trống.")
            else:
                print(f"{'STT':<4} | {'Mã SV':<8} | {'Họ và Tên':<20} | {'Toán':<5} | {'Lý':<5} | {'Hóa':<5} | {'Điểm TB':<8} | Xếp Loại")
                print("-" * 80)
                for index, sv in enumerate(student_list, start=1):
                    print(f"{index:<4} | {sv['id']:<8} | {sv['ten']:<20} | {sv['diem_toan']:<5} | {sv['diem_ly']:<5} | {sv['diem_hoa']:<5} | {sv['diem_tb']:<8} | {sv['xep_loai']}")
        case 2:
            print("\n--- THÊM MỚI SINH VIÊN ---")
            raw_id = input("Nhập mã số sinh viên (MSV): ").strip().upper()
            if not raw_id:
                print("[Lỗi] Mã sinh viên không được để trống!")
                continue

            is_duplicated = any(sv['id'] == raw_id for sv in student_list)
            if is_duplicated:
                print(f"[Lỗi] Thao tác thất bại: Mã sinh viên '{raw_id}' đã tồn tại!")
                continue
            name = input("Nhập họ và tên sinh viên: ").strip()
            if not name:
                print("[Lỗi] Tên sinh viên không được để trống!")
                continue
            math = input_score("Toán")
            physics = input_score("Lý")
            chemistry = input_score("Hóa")

            avg_score = round((math + physics + chemistry) / 3, 2)
            rank = calculate_rank(avg_score)

            new_student = {
                "id": raw_id,
                "ten": name,
                "diem_toan": math,
                "diem_ly": physics,
                "diem_hoa": chemistry,
                "diem_tb": avg_score,
                "xep_loai": rank
            }
            student_list.append(new_student)
            save_data(student_list)
            print(f"=> Thành công: Đã thêm mới sinh viên '{name}'.")
        case 3:
            print("\n--- CẬP NHẬT THÔNG TIN SINH VIÊN ---")
            target_id = input("Nhập Mã SV cần sửa: ").strip().upper()

            found_student = None
            for sv in student_list:
                if sv['id'] == target_id:
                    found_student = sv
                    break
            if not found_student:
                print(f"[Thất bại] Không tìm thấy sinh viên có mã '{target_id}'!")
            else:
                print(f"-> Đang sửa điểm cho sinh viên: {found_student['ten']}")
                new_math = input_score("Toán mới")
                new_physics = input_score("Lý mới")
                new_chemistry = input_score("Hóa mới")

                found_student['diem_toan'] = new_math
                found_student['diem_ly'] = new_physics
                found_student['diem_hoa'] = new_chemistry
                found_student['diem_tb'] = round((new_math + new_physics + new_chemistry) / 3, 2)
                found_student['xep_loai'] = calculate_rank(found_student['diem_tb'])

                save_data(student_list)
                print("=> Thành công: Cập nhật thông tin điểm số hoàn tất.")
        case 4:
            print("\n--- XÓA SINH VIÊN ---")
            target_id = input("Nhập Mã SV muốn xóa: ").strip().upper()

            target_index = -1
            for index, sv in enumerate(student_list):
                if sv['id'] == target_id:
                    target_index = index
                    break
            if target_index == -1:
                print(f"[Thất bại] Không tìm thấy sinh viên có mã '{target_id}'!")
            else:
                confirm = input(f"Bạn có chắc muốn xóa sinh viên '{student_list[target_index]['ten']}' không? (Y/N): ").strip().upper()
                if confirm == "Y":
                    removed_student = student_list.pop(target_index)
                    save_data(student_list)
                    print(f"=> Thành công: Đã xóa sinh viên '{removed_student['ten']}'.")
                else:
                    print("=> Đã hủy bỏ thao tác xóa.")
        case 5:
            print("\n--- TÌM KIẾM SINH VIÊN ---")
            keyword = input("Nhập Mã SV hoặc Tên cần tìm: ").strip().lower()
            if not keyword:
                print("[Lỗi] Vui lòng nhập từ khóa tìm kiếm!")
                continue
            search_results = []
            for sv in student_list:
                if keyword in sv['id'].lower() or keyword in sv['ten'].lower():
                    search_results.append(sv)

            if not search_results:
                print("Không tìm thấy kết quả phù hợp.")
            else:
                print(f"\nTìm thấy {len(search_results)} sinh viên:")
                print(f"{'Mã SV':<8} | {'Họ và Tên':<20} | {'Điểm TB':<8} | Xếp Loại")
                print("-" * 55)
                for sv in search_results:
                    print(f"{sv['id']:<8} | {sv['ten']:<20} | {sv['diem_tb']:<8} | {sv['xep_loai']}")
        case 6:
            if not student_list:
                print("\n[Lỗi] Danh sách trống, không thể sắp xếp!")
                continue
            print("\n--- SẮP XẾP DANH SÁCH SINH VIÊN ---")
            print("1. Sắp xếp theo Điểm TB giảm dần")
            print("2. Sắp xếp theo Tên tăng dần (A-Z)")
            try:
                sort_choice = int(input("Nhập lựa chọn của bạn (1-2): ").strip())
            except ValueError:
                sort_choice = 0

            if sort_choice == 1:
                student_list.sort(key=lambda x: x['diem_tb'], reverse=True)
                save_data(student_list)
                print("=> Đã sắp xếp theo Điểm TB giảm dần. Chọn chức năng 1 để xem kết quả.")
            elif sort_choice == 2:
                student_list.sort(key=lambda x: x['ten'])
                save_data(student_list)
                print("=> Đã sắp xếp theo Tên tăng dần. Chọn chức năng 1 để xem kết quả.")
            else:
                print("[Lỗi] Tùy chọn sắp xếp không hợp lệ!")
        case 7:
            print("\n--- THỐNG KÊ ĐIỂM TB (SỐ LƯỢNG) ---")
            counts = {"Giỏi": 0, "Khá": 0, "Trung Bình": 0, "Yếu": 0}
            for sv in student_list:
                if sv['xep_loai'] in counts:
                    counts[sv['xep_loai']] += 1
            print(f"Tổng số sinh viên: {len(student_list)}")
            print(f" - Loại Giỏi: {counts['Giỏi']}")
            print(f" - Loại Khá: {counts['Khá']}")
            print(f" - Loại Trung Bình: {counts['Trung Bình']}")
            print(f" - Loại Yếu: {counts['Yếu']}")
        case 8:
            print("\n--- SINH VIÊN CÓ ĐIỂM TB CAO NHẤT / THẤP NHẤT ---")
            if not student_list:
                print("Danh sách trống, không thể thống kê cực trị!")
                continue
            max_score = max(sv['diem_tb'] for sv in student_list)
            min_score = min(sv['diem_tb'] for sv in student_list)

            highest_students = [sv for sv in student_list if sv['diem_tb'] == max_score]
            lowest_students = [sv for sv in student_list if sv['diem_tb'] == min_score]

            print(f"\n[*] Sinh viên có Điểm TB Cao Nhất ({max_score}):")
            for sv in highest_students:
                print(f" - Mã SV: {sv['id']} | Tên: {sv['ten']} | Xếp loại: {sv['xep_loai']}")

            print(f"\n[*] Sinh viên có Điểm TB Thấp Nhất ({min_score}):")
            for sv in lowest_students:
                print(f" - Mã SV: {sv['id']} | Tên: {sv['ten']} | Xếp loại: {sv['xep_loai']}")
        case 9:
            print("\n--- PHÂN LOẠI HỌC LỰC SINH VIÊN (CHI TIẾT) ---")
            if not student_list:
                print("Danh sách sinh viên hiện đang trống.")
                continue
            categories = {"Giỏi": [], "Khá": [], "Trung Bình": [], "Yếu": []}
            for sv in student_list:
                if sv['xep_loai'] in categories:
                    categories[sv['xep_loai']].append(sv)

            for rank, svs in categories.items():
                print(f"\n[ Danh sách học lực: {rank} ]")
                if not svs:
                    print(" (Không có sinh viên nào)")
                else:
                    for sv in svs:
                        print(f" - Mã SV: {sv['id']} | Tên: {sv['ten']} | ĐTB: {sv['diem_tb']}")
        case 10:
            print("\nThoát chương trình thành công!")
            break
        case _:
            print("\n[Lỗi] Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 10!")
            continue