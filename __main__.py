from conifg import Config
from grid import run_interactive_demo

config = Config(
    note_duration=0.4,
    auto_advance_period=0.2
)

run_interactive_demo(config)