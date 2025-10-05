import pandas as pd
from pathlib import Path
import re
from datetime import datetime



def extract_datetime_from_filename(filename, pattern='result'):
    """Trích xuất datetime từ tên file

    Args:
        filename: Path object
        pattern: 'result' hoặc 'update'
    """
    try:
        match = re.search(rf'{pattern}_(\d{{8}}_\d{{6}})', filename.stem)
        if match:
            datetime_str = match.group(1)
            return datetime.strptime(datetime_str, '%Y%m%d_%H%M%S')
    except Exception as e:
        print(f"Không parse được datetime từ {filename.name}: {e}")
    return None


def get_last_file():
    """Lấy file result mới nhất"""
    base_dir = Path(__file__).resolve().parents[2]
    folder = base_dir / "excel" / "link" / "win_link"

    if not folder.exists():
        return None

    all_files = list(folder.glob("result_*.xlsx"))
    if not all_files:
        return None

    files_with_dt = []
    for f in all_files:
        dt = extract_datetime_from_filename(f, pattern='result')
        if dt:
            files_with_dt.append((f, dt))

    if not files_with_dt:
        return None

    files_with_dt.sort(key=lambda x: x[1], reverse=True)
    return files_with_dt[0][0]


def get_latest_update_file():
    """Lấy file update mới nhất"""
    base_dir = Path(__file__).resolve().parents[2]
    folder = base_dir / "excel" / "link" / "win_link" / "update"

    if not folder.exists():
        return None

    all_files = list(folder.glob("update_*.xlsx"))
    if not all_files:
        return None

    files_with_dt = []
    for f in all_files:
        dt = extract_datetime_from_filename(f, pattern='update')
        if dt:
            files_with_dt.append((f, dt))

    if not files_with_dt:
        return None

    files_with_dt.sort(key=lambda x: x[1], reverse=True)
    return files_with_dt[0][0]


def get_latest_files():
    """
    Lấy cả result file và update file mới nhất

    Returns:
        tuple: (result_data, update_data)
        - result_data: list of dict hoặc None
        - update_data: list of dict hoặc None
    """
    result_file = get_last_file()
    update_file = get_latest_update_file()

    result_data = None
    update_data = None

    if result_file:
        df_result = pd.read_excel(result_file)
        result_data = df_result.to_dict(orient="records")

    if update_file:
        df_update = pd.read_excel(update_file)
        update_data = df_update.to_dict(orient="records")

    return result_data, update_data,

