import pandas as pd
from pathlib import Path
import os
import re
from datetime import datetime


def normalize_text(text):
    """Chuẩn hóa text mạnh mẽ hơn"""
    if pd.isna(text):
        return ""
    text = str(text).strip().lower()
    text = re.sub(r'\s+', ' ', text)
    text = ''.join(char for char in text if char.isprintable() or char.isspace())
    return text.strip()


def extract_datetime_from_filename(filename):
    """Trích xuất datetime từ tên file result_YYYYMMDD_HHMMSS.xlsx

    Returns:
        datetime object hoặc None nếu không parse được
    """
    try:
        match = re.search(r'result_(\d{8}_\d{6})', filename.stem)
        if match:
            datetime_str = match.group(1)
            return datetime.strptime(datetime_str, '%Y%m%d_%H%M%S')
    except Exception as e:
        print(f"⚠️ Không parse được datetime từ {filename.name}: {e}")
    return None


def main():
    base_dir = Path(__file__).resolve().parents[2]
    folder = base_dir / "excel" / "link" / "win_link"

    print("📂 Đang tìm file trong:", folder)
    all_files = list(folder.glob("result_*.xls*"))

    # SẮP XẾP THEO DATETIME TRONG TÊN FILE (cross-platform safe)
    files_with_dt = []
    for f in all_files:
        dt = extract_datetime_from_filename(f)
        if dt:
            files_with_dt.append((f, dt))
        else:
            print(f"⚠️ Bỏ qua file không đúng format: {f.name}")

    if not files_with_dt:
        print("❌ Không tìm thấy file nào đúng format result_YYYYMMDD_HHMMSS.xlsx")
        return []

    # Sắp xếp theo datetime (mới nhất trước)
    files_with_dt.sort(key=lambda x: x[1], reverse=True)
    files = [f[0] for f in files_with_dt]

    print("🔍 Tìm thấy (sắp xếp theo tên file):")
    for f, dt in files_with_dt:
        print(f"   - {f.name} ({dt.strftime('%Y-%m-%d %H:%M:%S')})")

    if len(files) < 2:
        print(f"❗ Chưa đủ file để so sánh (cần ít nhất 2). Tìm thấy {len(files)} file.")
        return []

    latest_file, previous_file = files[0], files[1]
    print(f"\n✅ File mới nhất: {latest_file.name}")
    print(f"📄 File so sánh: {previous_file.name}")

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
        print("⚠️ Lấy 3 cột đầu tiên làm category, title, link")
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

    print(f"\n📊 File mới: {len(a)} dòng unique")
    print(f"📊 File cũ: {len(b)} dòng unique")

    # Tìm mục mới
    a['_key'] = a['category'] + '|||' + a['title']
    b['_key'] = b['category'] + '|||' + b['title']
    new_keys = set(a['_key']) - set(b['_key'])

    print(f"\n🔍 Phát hiện {len(new_keys)} mục mới")

    new_items = []
    if new_keys:
        only_in_latest = a[a['_key'].isin(new_keys)].drop(columns=['_key'])
        new_items = only_in_latest.to_dict(orient="records")

        print(f"✨ {len(new_items)} mục mới:")
        for i, item in enumerate(new_items[:5], 1):
            print(f"   {i}. {item['category']} - {item['title']}")
        if len(new_items) > 5:
            print(f"   ... và {len(new_items) - 5} mục khác")
    else:
        print("✅ Không có mục mới")

    # XÓA FILE CŨ (giữ lại file mới nhất)
    print("\n🗑️ Dọn dẹp file cũ...")
    files_to_delete = files[1:]

    for old_file in files_to_delete:
        try:
            os.remove(old_file)
            print(f"   ✅ Đã xóa: {old_file.name}")
        except Exception as e:
            print(f"   ❌ Lỗi xóa {old_file.name}: {e}")

    print(f"\n📁 Giữ lại: {latest_file.name} (tham chiếu cho lần sau)")

    return new_items


if __name__ == "__main__":
    new_arr = main()
    print(f"\n📦 Kết quả: {len(new_arr)} items mới")