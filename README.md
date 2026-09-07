# HieroglyphicKeyboards
Set of tools to facilitate the creation of keymnan hieroglyphic keyboards (based on Andrew Glass' qwerty hieroglyphic keyboard)
Current version supports :
* creating keyboards based on non-qwerty layouts (for instance Belgian azerty)
* using JSesh-cycles based on phonetic shortcuts (such as aA -> 𓉻->𓃘 -> 𓉼 -> 𓉿 -> 𓉻 )
* adding user-defined shortcuts


# Requirements
* "Egyptian Text" font to be found at https://github.com/microsoft/font-tools/
* keyman ( https://keyman.com/ ) - compatible with Mac, Windows & Linux

# Installation
* If there is a .kmp file matching your physical keyboard in the [keyboards](https://github.com/PhilHen/HieroglyphicKeyboards/tree/main/keyboards) folder, download that file and use keyman to install it on your system (keyman should be the default handler for .kmp file)
* Otherwise, download the cldrbuilder, modify sources/localized.xml according to your needs, modify the global constants in code/buildCldrHiero.py and run that python script. Then copy the resulting xml in a CLDR keyman-developer project, compile and install

# How does it work?
Signs encoding is similar to JSesh. Except for Egyptian hieroglyph format controls ( https://unicode.org/charts/PDF/U13430.pdf ), the keystrokes listed below act on the character (latin or hieroglyphic) immediately preceding the cursor.

## Gardiner signs

| Keyboard keys | Result |
| --- | --- |
| A1 <SPACE> | 𓀀 |
| <ALTGR>+<SPACE> | Convert hieroglyphic sign to Gardiner code |
| <ALTGR>+) | Previous sign (preceding sign must be a hieroglyph) |
| <ALTGR>+- | Next sign (preceding sign must be a hieroglyph) |
| <SHIFT>+<ALTGR>+, | Previous Gardiner group (preceding sign must be a hieroglyph) |
| <SHIFT>+<ALTGR>+; | Next Gardiner group (preceding sign must be a hieroglyph) |

In general, individual signs can be entered:
* using their Gardiner code followed by <SPACE> (in some cases, hitting <SPACE> more than once lets one access variants)
* using [phonetic shortcuts](Jsesh_phonetic_shortcuts.html), cycling using <SPACE>. These phonetic shortcuts have been extracted from JSesh. 
  

## Transliteration

| Keyboard keys | Result |
| --- | --- |
| <ALTGR>+a | ꜣ |
| <ALTGR>+d | ḏ |
| <ALTGR>+h | ḥ |
| <ALTGR>+k | ḳ |
| <ALTGR>+i | ꞽ |
| <ALTGR>+s | š |
| <ALTGR>+t | ṯ |
| <ALTGR>+ù𓏤 (azerty be) | ꜥ |

Corresponding uppercase glyphs can be obtained with <SHIFT>.

