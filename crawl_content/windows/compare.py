import pandas as pd
from pathlib import Path
import os
import re
from datetime import datetime
from openpyxl import Workbook

def normalize_text(text):
    """Chuẩn hóa text mạnh mẽ hơn"""
    if pd.isna(text):
        return ""
    text = str(text).strip().lower()
    text = re.sub(r'\s+', ' ', text)
    text = ''.join(char for char in text if char.isprintable() or char.isspace())
    return text.strip()


def extract_datetime_from_filename(filename, pattern='result'):
    """Trích xuất datetime từ tên file

    Args:
        filename: Path object
        pattern: 'result' hoặc 'update'

    Returns:
        datetime object hoặc None nếu không parse được
    """
    try:
        match = re.search(rf'{pattern}_(\d{{8}}_\d{{6}})', filename.stem)
        if match:
            datetime_str = match.group(1)
            return datetime.strptime(datetime_str, '%Y%m%d_%H%M%S')
    except Exception as e:
        print(f"Không parse được datetime từ {filename.name}: {e}")
    return None


def cleanup_old_files(folder, pattern='result', keep_count=5):
    """Xóa file cũ, chỉ giữ lại N file mới nhất

    Args:
        folder: Path đến thư mục chứa file
        pattern: Pattern tên file ('result' hoặc 'update')
        keep_count: Số lượng file mới nhất cần giữ lại (mặc định: 5)
    """
    print(f"\nDọn dẹp file {pattern} cũ (giữ lại {keep_count} file mới nhất)...")

    # Tìm tất cả file theo pattern
    all_files = list(folder.glob(f"{pattern}_*.xlsx"))

    if len(all_files) <= keep_count:
        print(f"   Có {len(all_files)} file, không cần xóa")
        return

    # Sắp xếp theo thời gian (mới nhất trước)
    files_with_dt = []
    for f in all_files:
        dt = extract_datetime_from_filename(f, pattern=pattern)
        if dt:
            files_with_dt.append((f, dt))
        else:
            print(f"   ⚠️ Không parse được: {f.name}")

    # Sắp xếp theo datetime (mới nhất trước)
    files_with_dt.sort(key=lambda x: x[1], reverse=True)

    # Lấy danh sách file cần xóa (bỏ qua N file mới nhất)
    files_to_delete = files_with_dt[keep_count:]

    if not files_to_delete:
        print("Không có file nào cần xóa")
        return

    print(f"   Tìm thấy {len(files_to_delete)} file cũ cần xóa:")
    deleted_count = 0

    for f, dt in files_to_delete:
        try:
            os.remove(f)
            print(f"   ✓ Đã xóa: {f.name} ({dt.strftime('%Y-%m-%d %H:%M:%S')})")
            deleted_count += 1
        except Exception as e:
            print(f"   ✗ Lỗi xóa {f.name}: {e}")

    print(f"   Đã xóa {deleted_count}/{len(files_to_delete)} file")


def main():
    base_dir = Path(__file__).resolve().parents[2]
    folder = base_dir / "excel" / "link" / "win_link"

    print("Đang tìm file trong:", folder)
    all_files = list(folder.glob("result_*.xlsx"))

    # SẮP XẾP THEO DATETIME TRONG TÊN FILE
    files_with_dt = []
    for f in all_files:
        dt = extract_datetime_from_filename(f, pattern='result')
        if dt:
            files_with_dt.append((f, dt))
        else:
            print(f"Bỏ qua file không đúng format: {f.name}")

    if not files_with_dt:
        print("Không tìm thấy file nào đúng format result_YYYYMMDD_HHMMSS.xlsx")
        return []

    # Sắp xếp theo datetime (mới nhất trước)
    files_with_dt.sort(key=lambda x: x[1], reverse=True)
    files = [f[0] for f in files_with_dt]

    print("Tìm thấy (sắp xếp theo thời gian):")
    for f, dt in files_with_dt:
        print(f"   - {f.name} ({dt.strftime('%Y-%m-%d %H:%M:%S')})")

    if len(files) < 2:
        print(f"Chưa đủ file để so sánh (cần ít nhất 2). Tìm thấy {len(files)} file.")
        return []

    latest_file, previous_file = files[0], files[1]
    print(f"\nFile mới nhất: {latest_file.name}")
    print(f"File so sánh: {previous_file.name}")

    # Đọc dữ liệu
    df_latest = pd.read_excel(latest_file)
    df_previous = pd.read_excel(previous_file)

    # Chuẩn hóa tên cột
    df_latest.columns = df_latest.columns.str.lower().str.strip()
    df_previous.columns = df_previous.columns.str.lower().str.strip()

    # Xử lý cột
    required_cols = ['category', 'title', 'link']
    available_cols = df_latest.columns.tolist()

    if not all(col in available_cols for col in required_cols):
        print("Lấy 3 cột đầu tiên làm category, title, link")
        df_latest = df_latest.iloc[:, :3]
        df_previous = df_previous.iloc[:, :3]
        df_latest.columns = required_cols
        df_previous.columns = required_cols
    else:
        df_latest = df_latest[required_cols]
        df_previous = df_previous[required_cols]

    # Chuẩn hóa dữ liệu
    for df in (df_latest, df_previous):
        for col in required_cols:
            df[col] = df[col].apply(normalize_text)

    # So sánh
    a = df_latest.drop_duplicates(subset=['category', 'title']).reset_index(drop=True)
    b = df_previous.drop_duplicates(subset=['category', 'title']).reset_index(drop=True)

    print(f"\nFile mới: {len(a)} dòng unique")
    print(f"File cũ: {len(b)} dòng unique")

    # Tìm mục mới
    a['_key'] = a['category'] + '|||' + a['title']
    b['_key'] = b['category'] + '|||' + b['title']
    new_keys = set(a['_key']) - set(b['_key'])

    print(f"\nPhát hiện {len(new_keys)} mục mới")

    new_items = []
    if new_keys:
        only_in_latest = a[a['_key'].isin(new_keys)].drop(columns=['_key'])
        new_items = only_in_latest.to_dict(orient="records")

        print(f"{len(new_items)} mục mới:")
        for i, item in enumerate(new_items[:5], 1):
            print(f"   {i}. {item['category']} - {item['title']}")
        if len(new_items) > 5:
            print(f"   ... và {len(new_items) - 5} mục khác")
    else:
        print("Không có mục mới")

    # DỌN DẸP FILE result_* CŨ (giữ lại 5 file mới nhất)
    cleanup_old_files(folder, pattern='result', keep_count=5)

    # LƯU KẾT QUẢ VÀO FILE MỚI
    if new_items:
        wb = Workbook()
        ws = wb.active
        ws.title = "Updates"

        # Header
        ws.append(["Category", "Title", "Link"])

        # Data
        for item in new_items:
            ws.append([item['category'], item['title'], item['link']])

        # Tạo đường dẫn file
        output_folder = base_dir / "excel" / "link" / "windows" / "update"
        output_folder.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_folder / f"update_{timestamp}.xlsx"

        wb.save(output_file)
        print(f"\nĐã lưu {len(new_items)} mục mới vào: {output_file}")

        # DỌN DẸP FILE update_* CŨ (giữ lại 5 file mới nhất)
        cleanup_old_files(output_folder, pattern='update', keep_count=5)
    else:
        print("\nKhông có gì để lưu (không có mục mới)")

    return new_items


if __name__ == "__main__":
    main()