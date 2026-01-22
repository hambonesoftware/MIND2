from __future__ import annotations

import threading
import time
from typing import Callable, Optional

import mido
from mido import MidiFile


class MidiPlayer:
    def __init__(self):
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._is_playing = False

    def is_playing(self) -> bool:
        with self._lock:
            return self._is_playing

    def stop(self) -> None:
        self._stop_event.set()

    def play_midifile(self, mid: MidiFile, output_name: str | None, on_done: Optional[Callable[[], None]] = None) -> None:
        if self.is_playing():
            self.stop()
            time.sleep(0.05)

        self._stop_event.clear()

        def run():
            out = None
            try:
                with self._lock:
                    self._is_playing = True

                if output_name:
                    out = mido.open_output(output_name)
                else:
                    names = mido.get_output_names()
                    if names:
                        out = mido.open_output(names[0])

                for msg in mid.play():
                    if self._stop_event.is_set():
                        break
                    if out and not msg.is_meta:
                        out.send(msg)

            except Exception as e:
                err = str(e)
                print("MIDI playback error:", err)
            finally:
                try:
                    if out:
                        out.close()
                except Exception:
                    pass
                with self._lock:
                    self._is_playing = False
                if on_done:
                    try:
                        on_done()
                    except Exception:
                        pass

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()
