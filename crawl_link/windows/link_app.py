from . import src_base

def link_app():
    links = [ "systema", "internet", "grafika", "dannye",
    "multimedia", "drajvery", "os", "bezopasnot",
    "sbornik-programm", "mobilework", "mac-os"
    ]

    path = "../../excel/link/windows/result.xlsx"

    src_base.craw_link(links, path)