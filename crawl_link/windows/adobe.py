from . import src_base

def adobe():
    adobe_apps = [
        "Acrobat", "Photoshop", "Illustrator", "After Effects", "Premiere Pro",
        "Lightroom", "InDesign", "Animate", "Audition", "Bridge", "Dreamweaver",
        "Fresco", "Character Animator", "Dimension", "Media Encoder", "XD" ]
    path_name = 'adobe_links'

    src_base.crawl_links(adobe_apps, path_name)
