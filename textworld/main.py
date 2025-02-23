from textworld.logs import init_logging
from textworld.tui.app import TextWorldApp

if __name__ == "__main__":
    init_logging()
    app = TextWorldApp()
    app.run()
