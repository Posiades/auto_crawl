from windows_crawl import base_src

def engineer():
    path_name = 'adobe_links'
    engineer_app = [
        # CAD – Thiết kế kỹ thuật
        "AutoCAD", "SolidWorks", "CATIA", "SketchUp",
        # CAE – Phân tích kỹ thuật / mô phỏng
        "ANSYS", "MATLAB", "Simulink", "COMSOL Multiphysics",
        # CAM – Sản xuất hỗ trợ máy tính
        "Mastercam", "Fusion 360", "NX CAM",
        # GIS – Hệ thống thông tin địa lý
        "ArcGIS", "QGIS",
        # Kỹ thuật phần mềm / IT
        "LabVIEW",
        # Quản lý dự án kỹ thuật
        "Primavera P6", "MS Project"
    ]

    base_src.crawl_links(engineer_app, path_name)