# HieroglyphicKeyboards
Set of tools to facilitate the creation of keyman hieroglyphic keyboards (based on Andrew Glass' qwerty hieroglyphic keyboard)
Current version supports :
* creating keyboards based on non-qwerty layouts (for instance Belgian azerty)
* using JSesh-cycles based on phonetic shortcuts (such as aA -> 𓉻->𓃘 -> 𓉼 -> 𓉿 -> 𓉻 )
* adding user-defined shortcuts


# Requirements
* "Egyptian Text" font to be found at https://github.com/microsoft/font-tools/
* keyman ( https://keyman.com/ ) - compatible with Mac, Windows & Linux

# Installing
* If there is a .kmp file matching your physical keyboard in the [keyboards](https://github.com/PhilHen/HieroglyphicKeyboards/tree/main/keyboards) folder, download that file and use keyman to install it on your system (keyman should be the default handler for .kmp file). Currently this is only applicable to the Belgian azerty be layout.
* Otherwise, download the cldrbuilder, modify sources/localized.xml according to your needs, modify the global constants in code/buildCldrHiero.py and run that python script. Then copy the resulting xml in a CLDR keyman-developer project, compile and install

# Using
Signs encoding is similar to JSesh. Except for Egyptian hieroglyph format controls ( https://unicode.org/charts/PDF/U13430.pdf ), the keystrokes listed below act on the character (latin or hieroglyphic) immediately preceding the cursor.
What follows is based on the Azerty Belgian keyboard layout. 
* \+ means keypresses are simultaneous
* "then" means keypresses are successive
* key combinations in the same cell of the table are alternatives producing the same result

## Gardiner signs

| Keyboard keys (azerty be) | Result |
| --- | --- |
| A1 then \<SPACE\> | 𓀀 |
| \<ALTGR\> + \<SPACE\> | Convert hieroglyph to Gardiner code  (sign before cursor must be a hieroglyph) |
| \<ALTGR\> + \<)\> | Previous sign (sign before cursor must be a hieroglyph) |
| \<ALTGR\> + \<-\> | Next sign (sign before cursor must be a hieroglyph) |
| \<SHIFT\> + \<ALTGR\> + \<,\> | Previous Gardiner group (sign before cursor must be a hieroglyph) |
| \<SHIFT\> + \<ALTGR\> + \<;\> | Next Gardiner group (sign before cursor must be a hieroglyph) |
| \<ALTGR\> + \<=> | Rotate clockwise (sign before cursor must be a hieroglyph) |

In general, individual signs can be entered:
* using their Gardiner code followed by \<SPACE\> (in some cases, hitting \<SPACE\> more than once lets one access variants)
* variants are usually referred using the "O29a" convention
* using [phonetic shortcuts](https://htmlpreview.github.io/?https://github.com/PhilHen/HieroglyphicKeyboards/blob/main/Jsesh_phonetic_shortcuts.html), cycling using \<SPACE\>. These phonetic shortcuts have been extracted from JSesh. 
  
## Brackets
| Keyboard keys (azerty be) | Result |
| --- | --- |
| \<ALTGR\> + \<^\>|⸢ TOP LEFT HALF BRACKET|
| \<ALTGR\> + \<$\>|⸣ TOP RIGHT HALF BRACKET|
| \<ALTGR\> + \<,\>|⟨ MATHEMATICAL LEFT ANGLE BRACKET|
| \<ALTGR\> + \<;\>|⟩ MATHEMATICAL RIGHT ANGLE BRACKET|
| \<SHIFT\> + \<ALTGR\> + \<^\>|⟦ MATHEMATICAL LEFT WHITE SQUARE BRACKET|
| \<SHIFT\> + \<ALTGR\> + \<$\>|⟧ MATHEMATICAL RIGHT WHITE SQUARE BRACKET|


