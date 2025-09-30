import re
import pandas as pd
from pathlib import Path

def load_latest_to_df(folder: str, base_name: str) -> pd.DataFrame:
    """
    Tìm và nạp file Excel mới nhất dạng base_name_YYYYMMDD_HHMMSS.xlsx
    """
    folder = Path(folder)
    # pattern ví dụ: win_link_20250930_153000.xlsx
    pattern = re.compile(rf"{base_name}_(\d{{8}}_\d{{6}})\.xlsx$")

    files = []
    for f in folder.glob(f"{base_name}_*.xlsx"):
        if pattern.search(f.name):
            files.append(f)

    if not files:
        raise FileNotFoundError(f"❌ Không tìm thấy file nào dạng {base_name}_*.xlsx trong {folder}")

    # sort theo tên (timestamp format YYYYMMDD_HHMMSS đảm bảo đúng thứ tự)
    files_sorted = sorted(files, key=lambda f: f.name)
    latest_file = files_sorted[-1]

    print(f"📂 Nạp file mới nhất: {latest_file}")
    return pd.read_excel(latest_file)

