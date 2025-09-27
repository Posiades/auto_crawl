from windows_crawl import base_src

def adobe():
    adobe_apps = [
        "Acrobat", "Photoshop", "Illustrator", "After Effects", "Premiere Pro",
        "Lightroom", "InDesign", "Animate", "Audition", "Bridge", "Dreamweaver",
        "Fresco", "Character Animator", "Dimension", "Media Encoder", "XD" ]
    path_name = 'adobe_links'

    base_src.crawl_links(adobe_apps, path_name)
