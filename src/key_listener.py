from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Callable, Set

from utils import ConfigManager


class InputEvent(Enum):
    KEY_PRESS = auto()
    KEY_RELEASE = auto()
    MOUSE_PRESS = auto()
    MOUSE_RELEASE = auto()

class KeyCode(Enum):
    # Modifier keys
    CTRL_LEFT = auto()
    CTRL_RIGHT = auto()
    SHIFT_LEFT = auto()
    SHIFT_RIGHT = auto()
    ALT_LEFT = auto()
    ALT_RIGHT = auto()
    META_LEFT = auto()
    META_RIGHT = auto()

    # Function keys
    F1 = auto()
    F2 = auto()
    F3 = auto()
    F4 = auto()
    F5 = auto()
    F6 = auto()
    F7 = auto()
    F8 = auto()
    F9 = auto()
    F10 = auto()
    F11 = auto()
    F12 = auto()
    F13 = auto()
    F14 = auto()
    F15 = auto()
    F16 = auto()
    F17 = auto()
    F18 = auto()
    F19 = auto()
    F20 = auto()
    F21 = auto()
    F22 = auto()
    F23 = auto()
    F24 = auto()

    # Number keys
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    ZERO = auto()

    # Letter keys
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()
    U = auto()
    V = auto()
    W = auto()
    X = auto()
    Y = auto()
    Z = auto()

    # Special keys
    SPACE = auto()
    ENTER = auto()
    TAB = auto()
    BACKSPACE = auto()
    ESC = auto()
    INSERT = auto()
    DELETE = auto()
    HOME = auto()
    END = auto()
    PAGE_UP = auto()
    PAGE_DOWN = auto()
    CAPS_LOCK = auto()
    NUM_LOCK = auto()
    SCROLL_LOCK = auto()
    PAUSE = auto()
    PRINT_SCREEN = auto()

    # Arrow keys
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    # Numpad keys
    NUMPAD_0 = auto()
    NUMPAD_1 = auto()
    NUMPAD_2 = auto()
    NUMPAD_3 = auto()
    NUMPAD_4 = auto()
    NUMPAD_5 = auto()
    NUMPAD_6 = auto()
    NUMPAD_7 = auto()
    NUMPAD_8 = auto()
    NUMPAD_9 = auto()
    NUMPAD_ADD = auto()
    NUMPAD_SUBTRACT = auto()
    NUMPAD_MULTIPLY = auto()
    NUMPAD_DIVIDE = auto()
    NUMPAD_DECIMAL = auto()
    NUMPAD_ENTER = auto()

    # Additional special characters
    MINUS = auto()
    EQUALS = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    SEMICOLON = auto()
    QUOTE = auto()
    BACKQUOTE = auto()
    BACKSLASH = auto()
    COMMA = auto()
    PERIOD = auto()
    SLASH = auto()

    # Media keys
    MUTE = auto()
    VOLUME_DOWN = auto()
    VOLUME_UP = auto()
    PLAY_PAUSE = auto()
    NEXT_TRACK = auto()
    PREV_TRACK = auto()

    # Additional Media and Special Function Keys
    MEDIA_PLAY = auto()
    MEDIA_PAUSE = auto()
    MEDIA_PLAY_PAUSE = auto()
    MEDIA_STOP = auto()
    MEDIA_PREVIOUS = auto()
    MEDIA_NEXT = auto()
    MEDIA_REWIND = auto()
    MEDIA_FAST_FORWARD = auto()
    AUDIO_MUTE = auto()
    AUDIO_VOLUME_UP = auto()
    AUDIO_VOLUME_DOWN = auto()
    MEDIA_SELECT = auto()
    WWW = auto()
    MAIL = auto()
    CALCULATOR = auto()
    COMPUTER = auto()
    APP_SEARCH = auto()
    APP_HOME = auto()
    APP_BACK = auto()
    APP_FORWARD = auto()
    APP_STOP = auto()
    APP_REFRESH = auto()
    APP_BOOKMARKS = auto()
    BRIGHTNESS_DOWN = auto()
    BRIGHTNESS_UP = auto()
    DISPLAY_SWITCH = auto()
    KEYBOARD_ILLUMINATION_TOGGLE = auto()
    KEYBOARD_ILLUMINATION_DOWN = auto()
    KEYBOARD_ILLUMINATION_UP = auto()
    EJECT = auto()
    SLEEP = auto()
    WAKE = auto()
    EMOJI = auto()
    MENU = auto()
    CLEAR = auto()
    LOCK = auto()

    # Mouse Buttons
    MOUSE_LEFT = auto()
    MOUSE_RIGHT = auto()
    MOUSE_MIDDLE = auto()
    MOUSE_BACK = auto()
    MOUSE_FORWARD = auto()
    MOUSE_SIDE1 = auto()
    MOUSE_SIDE2 = auto()
    MOUSE_SIDE3 = auto()

class InputBackend(ABC):
    """
    Abstract base class for input backends.
    This class defines the interface that all input backends must implement.
    """

    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        """
        Check if this input backend is available on the current system.

        Returns:
            bool: True if the backend is available, False otherwise.
        """
        pass

    @abstractmethod
    def start(self):
        """
        Start the input backend.
        This method should initialize any necessary resources and begin listening for input events.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Stop the input backend.
        This method should clean up any resources and stop listening for input events.
        """
        pass

    @abstractmethod
    def on_input_event(self, event: tuple[KeyCode, InputEvent]):
        """
        Handle an input event.
        This method is called when an input event is detected.

        :param event (Tuple[KeyCode, InputEvent]): A tuple containing the key code and the type of event.
        """
        pass

class KeyChord:
    """
    Represents a combination of keys that need to be pressed simultaneously.
    """

    def __init__(self, keys: Set[KeyCode | frozenset[KeyCode]]):
        """Initialize the KeyChord."""
        self.keys = keys
        self.pressed_keys: Set[KeyCode] = set()

    def update(self, key: KeyCode, event_type: InputEvent) -> bool:
        """Update the state of pressed keys and check if the chord is active."""
        if event_type == InputEvent.KEY_PRESS:
            self.pressed_keys.add(key)
        elif event_type == InputEvent.KEY_RELEASE:
            self.pressed_keys.discard(key)

        return self.is_active()

    def is_active(self) -> bool:
        """Check if all keys in the chord are currently pressed."""
        for key in self.keys:
            if isinstance(key, frozenset):
                if not any(k in self.pressed_keys for k in key):
                    return False
            elif key not in self.pressed_keys:
                return False
        return True

class KeyListener:
    """
    Manages input backends and listens for specific key combinations.
    """

    def __init__(self):
        """Initialize the KeyListener with backends and activation keys."""
        self.input_backend = None

        self.typing_only_chord = None
        self.typing_and_clipboard_chord = None
        self.clipboard_only_chord = None

        self.key_listener = None
        
        self.callbacks = {
            "on_activate_typing_only": [],
            "on_activate_clipboard_only": [],
            "on_activate_typing_and_clipboard": [],
            "on_deactivate": []
        }
        self.load_activation_keys_from_config()
        self.initialize_backend()

    def initialize_backend(self):
        """Initialize pynput backend."""
        self.input_backend = PynputBackend()
        self.input_backend.on_input_event = self.on_input_event

    def start(self):
        self.input_backend.start()

    def stop(self):
        self.input_backend.stop()

    def load_activation_keys_from_config(self):
        typing_only_key = ConfigManager.get_config_value('recording_options', 'typing_activation_key')
        typing_and_clipboard_key = ConfigManager.get_config_value('recording_options', 'typing_and_clipboard_activation_key')
        clipboard_only_key = ConfigManager.get_config_value('recording_options', 'clipboard_activation_key')


        typing_only_keys = self.parse_key_combination(typing_only_key)
        typing_and_clipboard_keys = self.parse_key_combination(typing_and_clipboard_key)
        clipboard_only_keys = self.parse_key_combination(clipboard_only_key)
        self.set_activation_keys(typing_only_keys, typing_and_clipboard_keys, clipboard_only_keys)

    def parse_key_combination(self, combination_string: str) -> Set[KeyCode | frozenset[KeyCode]]:
        """Parse a string representation of key combination into a set of KeyCodes."""
        keys = set()
        key_map = {
            'CTRL': frozenset({KeyCode.CTRL_LEFT, KeyCode.CTRL_RIGHT}),
            'SHIFT': frozenset({KeyCode.SHIFT_LEFT, KeyCode.SHIFT_RIGHT}),
            'ALT': frozenset({KeyCode.ALT_LEFT, KeyCode.ALT_RIGHT}),
            'META': frozenset({KeyCode.META_LEFT, KeyCode.META_RIGHT}),
        }

        for key in combination_string.upper().split('+'):
            key = key.strip()
            if key in key_map:
                keys.add(key_map[key])
            else:
                try:
                    keycode = KeyCode[key]
                    keys.add(keycode)
                except KeyError:
                    print(f"Unknown key: {key}, in key combination: {combination_string}.")
        return keys

    def set_activation_keys(self, 
            typing_only_keys: Set[KeyCode], 
            typing_and_clipboard_keys: Set[KeyCode], 
            clipboard_only_keys: Set[KeyCode]
        ):
        """Set the activation keys for the KeyChord."""

        self.typing_only_chord = KeyChord(typing_only_keys)
        self.typing_and_clipboard_chord = KeyChord(typing_and_clipboard_keys)
        self.clipboard_only_chord = KeyChord(clipboard_only_keys)

    def on_input_event(self, event):
        """Handle input events and trigger callbacks if the key chord becomes active or inactive."""
        if not self.typing_only_chord or not self.input_backend:
            return

        key, event_type = event

        was_active = {
            "typing_only": self.typing_only_chord.is_active(),
            "typing_and_clipboard": self.typing_and_clipboard_chord.is_active(),
            "clipboard_only": self.clipboard_only_chord.is_active()
        }
        is_active = {
            "typing_only": self.typing_only_chord.update(key, event_type),
            "typing_and_clipboard": self.typing_and_clipboard_chord.update(key, event_type),
            "clipboard_only": self.clipboard_only_chord.update(key, event_type)
        }

        if not was_active["typing_only"] and is_active["typing_only"]:
            self._trigger_callbacks("on_activate_typing_only")
        elif not was_active["typing_and_clipboard"] and is_active["typing_and_clipboard"]:
            self._trigger_callbacks("on_activate_typing_and_clipboard")
        elif not was_active["clipboard_only"] and is_active["clipboard_only"]:
            self._trigger_callbacks("on_activate_clipboard_only")
        elif any(was_active.values()) and not any(is_active.values()):
            self._trigger_callbacks("on_deactivate")

    def add_callback(self, event: str, callback: Callable):
        """Add a callback function for a specific event."""
        if event in self.callbacks:
            self.callbacks[event].append(callback)

    def _trigger_callbacks(self, event: str):
        """Trigger all callbacks associated with a specific event."""
        for callback in self.callbacks.get(event, []):
            callback()

    def update_activation_keys(self):
        """Update activation keys from the current configuration."""
        self.load_activation_keys_from_config()

class PynputBackend(InputBackend):
    """
    Input backend implementation using the pynput library.
    """

    @classmethod
    def is_available(cls) -> bool:
        """Check if pynput library is available."""
        try:
            import pynput
            return True
        except ImportError:
            return False

    def __init__(self):
        """Initialize PynputBackend."""
        self.keyboard_listener = None
        self.mouse_listener = None
        self.keyboard = None
        self.mouse = None
        self.key_map = None

    def start(self):
        """Start listening for keyboard and mouse events."""
        if self.keyboard is None or self.mouse is None:
            from pynput import keyboard, mouse
            self.keyboard = keyboard
            self.mouse = mouse
            self.key_map = self._create_key_map()

        self.keyboard_listener = self.keyboard.Listener(
            on_press=self._on_keyboard_press,
            on_release=self._on_keyboard_release)

        self.mouse_listener = self.mouse.Listener(
            on_click=self._on_mouse_click
        )

        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop(self):
        """Stop listening for keyboard and mouse events."""
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None

    def _translate_key_event(self, key_event, is_press) -> tuple[KeyCode, InputEvent]:
        """Translate a pynput event to our internal event representation."""
        
        key_code = self.key_map.get(key_event, KeyCode.SPACE)
        event_type = InputEvent.KEY_PRESS if is_press else InputEvent.KEY_RELEASE
        return key_code, event_type 
        
    def _on_keyboard_press(self, key):
        """Handle keyboard press events."""

        key = self.keyboard_listener.canonical(key)
        translated_event = self._translate_key_event(key, True)
        self.on_input_event(translated_event)

    def _on_keyboard_release(self, key):
        """Handle keyboard release events."""

        key = self.keyboard_listener.canonical(key)
        translated_event = self._translate_key_event(key, False)
        self.on_input_event(translated_event)

    def _on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click events."""
        
        translated_event = self._translate_key_event(button, pressed)
        self.on_input_event(translated_event)

    def _create_key_map(self):
        """Create a mapping from pynput keys to our internal KeyCode enum."""
        return {
            # Modifier keys
            self.keyboard.Key.ctrl: KeyCode.CTRL_LEFT,
            self.keyboard.Key.ctrl_l: KeyCode.CTRL_LEFT,
            self.keyboard.Key.ctrl_r: KeyCode.CTRL_RIGHT,
            self.keyboard.Key.shift: KeyCode.SHIFT_LEFT,
            self.keyboard.Key.shift_l: KeyCode.SHIFT_LEFT,
            self.keyboard.Key.shift_r: KeyCode.SHIFT_RIGHT,
            self.keyboard.Key.alt: KeyCode.ALT_LEFT,
            self.keyboard.Key.alt_l: KeyCode.ALT_LEFT,
            self.keyboard.Key.alt_r: KeyCode.ALT_RIGHT,
            self.keyboard.Key.cmd: KeyCode.META_LEFT,
            self.keyboard.Key.cmd_l: KeyCode.META_LEFT,
            self.keyboard.Key.cmd_r: KeyCode.META_RIGHT,

            # Function keys
            self.keyboard.Key.f1: KeyCode.F1,
            self.keyboard.Key.f2: KeyCode.F2,
            self.keyboard.Key.f3: KeyCode.F3,
            self.keyboard.Key.f4: KeyCode.F4,
            self.keyboard.Key.f5: KeyCode.F5,
            self.keyboard.Key.f6: KeyCode.F6,
            self.keyboard.Key.f7: KeyCode.F7,
            self.keyboard.Key.f8: KeyCode.F8,
            self.keyboard.Key.f9: KeyCode.F9,
            self.keyboard.Key.f10: KeyCode.F10,
            self.keyboard.Key.f11: KeyCode.F11,
            self.keyboard.Key.f12: KeyCode.F12,
            self.keyboard.Key.f13: KeyCode.F13,
            self.keyboard.Key.f14: KeyCode.F14,
            self.keyboard.Key.f15: KeyCode.F15,
            self.keyboard.Key.f16: KeyCode.F16,
            self.keyboard.Key.f17: KeyCode.F17,
            self.keyboard.Key.f18: KeyCode.F18,
            self.keyboard.Key.f19: KeyCode.F19,
            self.keyboard.Key.f20: KeyCode.F20,

            # Number keys
            self.keyboard.KeyCode.from_char('1'): KeyCode.ONE,
            self.keyboard.KeyCode.from_char('2'): KeyCode.TWO,
            self.keyboard.KeyCode.from_char('3'): KeyCode.THREE,
            self.keyboard.KeyCode.from_char('4'): KeyCode.FOUR,
            self.keyboard.KeyCode.from_char('5'): KeyCode.FIVE,
            self.keyboard.KeyCode.from_char('6'): KeyCode.SIX,
            self.keyboard.KeyCode.from_char('7'): KeyCode.SEVEN,
            self.keyboard.KeyCode.from_char('8'): KeyCode.EIGHT,
            self.keyboard.KeyCode.from_char('9'): KeyCode.NINE,
            self.keyboard.KeyCode.from_char('0'): KeyCode.ZERO,

            # Letter keys
            self.keyboard.KeyCode.from_char('a'): KeyCode.A,
            self.keyboard.KeyCode.from_char('b'): KeyCode.B,
            self.keyboard.KeyCode.from_char('c'): KeyCode.C,
            self.keyboard.KeyCode.from_char('d'): KeyCode.D,
            self.keyboard.KeyCode.from_char('e'): KeyCode.E,
            self.keyboard.KeyCode.from_char('f'): KeyCode.F,
            self.keyboard.KeyCode.from_char('g'): KeyCode.G,
            self.keyboard.KeyCode.from_char('h'): KeyCode.H,
            self.keyboard.KeyCode.from_char('i'): KeyCode.I,
            self.keyboard.KeyCode.from_char('j'): KeyCode.J,
            self.keyboard.KeyCode.from_char('k'): KeyCode.K,
            self.keyboard.KeyCode.from_char('l'): KeyCode.L,
            self.keyboard.KeyCode.from_char('m'): KeyCode.M,
            self.keyboard.KeyCode.from_char('n'): KeyCode.N,
            self.keyboard.KeyCode.from_char('o'): KeyCode.O,
            self.keyboard.KeyCode.from_char('p'): KeyCode.P,
            self.keyboard.KeyCode.from_char('q'): KeyCode.Q,
            self.keyboard.KeyCode.from_char('r'): KeyCode.R,
            self.keyboard.KeyCode.from_char('s'): KeyCode.S,
            self.keyboard.KeyCode.from_char('t'): KeyCode.T,
            self.keyboard.KeyCode.from_char('u'): KeyCode.U,
            self.keyboard.KeyCode.from_char('v'): KeyCode.V,
            self.keyboard.KeyCode.from_char('w'): KeyCode.W,
            self.keyboard.KeyCode.from_char('x'): KeyCode.X,
            self.keyboard.KeyCode.from_char('y'): KeyCode.Y,
            self.keyboard.KeyCode.from_char('z'): KeyCode.Z,

            # Special keys
            self.keyboard.Key.space: KeyCode.SPACE,
            self.keyboard.Key.enter: KeyCode.ENTER,
            self.keyboard.Key.tab: KeyCode.TAB,
            self.keyboard.Key.backspace: KeyCode.BACKSPACE,
            self.keyboard.Key.esc: KeyCode.ESC,
            self.keyboard.Key.insert: KeyCode.INSERT,
            self.keyboard.Key.delete: KeyCode.DELETE,
            self.keyboard.Key.home: KeyCode.HOME,
            self.keyboard.Key.end: KeyCode.END,
            self.keyboard.Key.page_up: KeyCode.PAGE_UP,
            self.keyboard.Key.page_down: KeyCode.PAGE_DOWN,
            self.keyboard.Key.caps_lock: KeyCode.CAPS_LOCK,
            self.keyboard.Key.num_lock: KeyCode.NUM_LOCK,
            self.keyboard.Key.scroll_lock: KeyCode.SCROLL_LOCK,
            self.keyboard.Key.pause: KeyCode.PAUSE,
            self.keyboard.Key.print_screen: KeyCode.PRINT_SCREEN,

            # Arrow keys
            self.keyboard.Key.up: KeyCode.UP,
            self.keyboard.Key.down: KeyCode.DOWN,
            self.keyboard.Key.left: KeyCode.LEFT,
            self.keyboard.Key.right: KeyCode.RIGHT,

            # Numpad keys
            self.keyboard.Key.num_lock: KeyCode.NUM_LOCK,
            self.keyboard.KeyCode.from_vk(96): KeyCode.NUMPAD_0,
            self.keyboard.KeyCode.from_vk(97): KeyCode.NUMPAD_1,
            self.keyboard.KeyCode.from_vk(98): KeyCode.NUMPAD_2,
            self.keyboard.KeyCode.from_vk(99): KeyCode.NUMPAD_3,
            self.keyboard.KeyCode.from_vk(100): KeyCode.NUMPAD_4,
            self.keyboard.KeyCode.from_vk(101): KeyCode.NUMPAD_5,
            self.keyboard.KeyCode.from_vk(102): KeyCode.NUMPAD_6,
            self.keyboard.KeyCode.from_vk(103): KeyCode.NUMPAD_7,
            self.keyboard.KeyCode.from_vk(104): KeyCode.NUMPAD_8,
            self.keyboard.KeyCode.from_vk(105): KeyCode.NUMPAD_9,
            self.keyboard.KeyCode.from_vk(107): KeyCode.NUMPAD_ADD,
            self.keyboard.KeyCode.from_vk(109): KeyCode.NUMPAD_SUBTRACT,
            self.keyboard.KeyCode.from_vk(106): KeyCode.NUMPAD_MULTIPLY,
            self.keyboard.KeyCode.from_vk(111): KeyCode.NUMPAD_DIVIDE,
            self.keyboard.KeyCode.from_vk(110): KeyCode.NUMPAD_DECIMAL,

            # Additional special characters
            self.keyboard.KeyCode.from_char('-'): KeyCode.MINUS,
            self.keyboard.KeyCode.from_char('='): KeyCode.EQUALS,
            self.keyboard.KeyCode.from_char('['): KeyCode.LEFT_BRACKET,
            self.keyboard.KeyCode.from_char(']'): KeyCode.RIGHT_BRACKET,
            self.keyboard.KeyCode.from_char(';'): KeyCode.SEMICOLON,
            self.keyboard.KeyCode.from_char("'"): KeyCode.QUOTE,
            self.keyboard.KeyCode.from_char('`'): KeyCode.BACKQUOTE,
            self.keyboard.KeyCode.from_char('\\'): KeyCode.BACKSLASH,
            self.keyboard.KeyCode.from_char(','): KeyCode.COMMA,
            self.keyboard.KeyCode.from_char('.'): KeyCode.PERIOD,
            self.keyboard.KeyCode.from_char('/'): KeyCode.SLASH,

            # Media keys
            self.keyboard.Key.media_volume_mute: KeyCode.AUDIO_MUTE,
            self.keyboard.Key.media_volume_down: KeyCode.AUDIO_VOLUME_DOWN,
            self.keyboard.Key.media_volume_up: KeyCode.AUDIO_VOLUME_UP,
            self.keyboard.Key.media_play_pause: KeyCode.MEDIA_PLAY_PAUSE,
            self.keyboard.Key.media_next: KeyCode.MEDIA_NEXT,
            self.keyboard.Key.media_previous: KeyCode.MEDIA_PREVIOUS,

            # Mouse buttons
            self.mouse.Button.left: KeyCode.MOUSE_LEFT,
            self.mouse.Button.right: KeyCode.MOUSE_RIGHT,
            self.mouse.Button.middle: KeyCode.MOUSE_MIDDLE,
        }

    def on_input_event(self, event):
        """
        Callback method to be set by the KeyListener.
        This method is called for each processed input event.
        """
        pass
