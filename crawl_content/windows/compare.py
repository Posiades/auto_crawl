from pathlib import Path
import re
import pandas as pd

def get_two_latest_files(folder: str, base_name: str):
    """
    Lấy ra 2 file Excel mới nhất theo tên base_name_YYYYMMDD_HHMMSS.xlsx
    """
    folder = Path(folder)
    pattern = re.compile(rf"{base_name}_(\d{{8}}_\d{{6}})\.xlsx$")

    files = [f for f in folder.glob(f"{base_name}_*.xlsx") if pattern.search(f.name)]

    if len(files) < 2:
        raise FileNotFoundError(f"⚠️ Cần ít nhất 2 file {base_name}_*.xlsx trong {folder}")

    files_sorted = sorted(files, key=lambda f: f.name)
    return files_sorted[-2], files_sorted[-1]  # (file_cũ, file_mới)


def load_and_diff(folder: str, base_name: str) -> pd.DataFrame:
    """
    Nạp 2 file Excel mới nhất, so sánh và trả về phần mới có trong file mới nhất.
    """
    old_file, new_file = get_two_latest_files(folder, base_name)
    print(f"📂 File cũ: {old_file}")
    print(f"📂 File mới: {new_file}")

    df_old = pd.read_excel(old_file)
    df_new = pd.read_excel(new_file)

    # So sánh: giữ lại các dòng có trong df_new nhưng không có trong df_old
    df_diff = pd.concat([df_new, df_old, df_old]).drop_duplicates(keep=False)

    if df_diff.empty:
        print("ℹ️ Không có dữ liệu mới.")
    else:
        print(f"✅ Tìm thấy {len(df_diff)} dòng dữ liệu mới.")

    return df_diff
