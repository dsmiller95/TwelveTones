"""
play_note(index, instrument='piano', duration=0.5)

index       0–12  : C, C♯/D♭, D, …, B, C¹
instrument  str   : 'piano', 'guitar', or any GM patch below
duration    float : seconds
"""
import time
import threading
import fluidsynth

# Map 0‒12 to one octave starting at middle-C (MIDI 60)
NOTE_NUM = [60 + i for i in range(13)]

GM_PATCH = {
    "piano": 0,          # Acoustic Grand Piano
    "guitar": 24,        # Nylon-string Guitar
    "elec_guitar": 26,   # Jazz Guitar
    "strings": 48,       # String Ensemble
}

SF2 = r'C:\source\TwelveTones\SoundFonts\default.sf2'

# one global synth keeps things simple
_fs = fluidsynth.Synth()
_fs.start()              # auto-pick best audio driver
_sfid = _fs.sfload(SF2)  # load sound-font into RAM

# Channel management for up to 3 simultaneous notes
_available_channels = [0, 1, 2]
_channel_lock = threading.Lock()

def _get_next_channel() -> int:
    """Get the next available channel, cycling through 0-2"""
    with _channel_lock:
        if _available_channels:
            return _available_channels.pop(0)
        else:
            # If no channels available, use channel 0 (oldest note gets interrupted)
            return 0

def _release_channel(channel: int) -> None:
    """Release a channel back to the available pool"""
    with _channel_lock:
        if channel not in _available_channels:
            _available_channels.append(channel)
            _available_channels.sort()

def _play_note_async(channel: int, midi_key: int, duration: float) -> None:
    """Internal function to handle note timing in a separate thread"""
    time.sleep(duration)
    _fs.noteoff(channel, midi_key)
    _release_channel(channel)

def play_note(index: int, instrument: str = "piano",
              duration: float = 0.5, velocity: int = 100) -> None:
    if not 0 <= index <= 12:
        raise ValueError("index must be 0-12")

    channel = _get_next_channel()
    prog = GM_PATCH.get(instrument, 0)
    _fs.program_select(channel, _sfid, 0, prog)   # (chan, sfid, bank, program)
    midi_key = NOTE_NUM[index]
    _fs.noteon(channel, midi_key, velocity)

    # Start a thread to handle note-off timing
    threading.Thread(target=_play_note_async, args=(channel, midi_key, duration), daemon=True).start()

# demo: play C♯ (index=1) on nylon-guitar
if __name__ == "__main__":
    play_note(1, "guitar", duration=4)
    play_note(6, "guitar", duration=2)
    play_note(9, "guitar", duration=1)
    time.sleep(5)
