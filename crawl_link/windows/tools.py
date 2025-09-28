from . import src_base

def tools():
    tools_app = [
        "HEU KMS", "c2r", "Ankh Tech Toolbox", ""
    ]
    path_name = "tool_links"

    src_base.crawl_links(tools_app, path_name)