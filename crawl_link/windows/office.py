from . import src_base

def office():

    office_app = [
        "IDM", "Bandicam", "ccleaner", "driver booster pro", "winrar", "Foxit PDF", "EaseUS Partition Master",
        "Advanced SystemCare Pro", "Disk Drill Enterprise", "Remote Desktop Manager Enterprise", "Wondershare UniConverter",
        "Topaz Video AI", "CHITUBOX Pro", "PDF Architect Pro", "RAM Saver Pro", "Charles", "uTorrent Pro",
        "WinTools.Net Professional",
    ]

    path_name = "office_links"
    src_base.crawl_links(office_app, path_name)