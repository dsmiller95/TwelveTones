"""
play_note(index, instrument='piano', duration=0.5)

index       0–12  : C, C♯/D♭, D, …, B, C¹
instrument  str   : 'piano', 'guitar', or any GM patch below
duration    float : seconds
"""
import time
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

def play_note(index: int, instrument: str = "piano",
              duration: float = 0.5, velocity: int = 100):
    if not 0 <= index <= 12:
        raise ValueError("index must be 0-12")
    prog = GM_PATCH.get(instrument, 0)
    _fs.program_select(0, _sfid, 0, prog)   # (chan, sfid, bank, program)
    midi_key = NOTE_NUM[index]
    _fs.noteon(0, midi_key, velocity)       # channel 0
    time.sleep(duration)
    _fs.noteoff(0, midi_key)

# demo: play C♯ (index=1) on nylon-guitar
if __name__ == "__main__":
    play_note(1, "guitar")
