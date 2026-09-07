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
* If there is a .kmp file matching your physical keyboard in the [keyboards] folder, download this file and use keyman to install it on your system (keyman should be the default handler for .kmp file)
* Otherwise, download the cldrbuilder, modify sources/localized.xml according to your needs, modify the global constants in code/buildCldrHiero.py and run that python script. Then copy the resulting xml in a CLDR keyman-developer project, compile and install


