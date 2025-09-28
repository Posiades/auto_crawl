from . import src_base

def crawl_category_game():
    name_category = [
        "action", "adventure", "arcade", "fighting", "horror",
        "puzzle", "racing", "shooting-games", "simulation",
        "war", "sci-fi", "rpg", "survival"
    ]

    for name in name_category:
        src_base.crawl_game(name)