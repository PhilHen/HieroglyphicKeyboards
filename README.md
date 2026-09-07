# HieroglyphicKeyboards
Set of tools to facilitate the creation of keyman hieroglyphic keyboards (based on Andrew Glass' qwerty hieroglyphic keyboard)
Current version supports :
* creating keyboards based on non-qwerty layouts (for instance Belgian azerty)
* using JSesh-cycles based on phonetic shortcuts (such as aA -> 𓉻->𓃘 -> 𓉼 -> 𓉿 -> 𓉻 )
* adding user-defined shortcuts


# Requirements
* "Egyptian Text" font to be found at https://github.com/microsoft/font-tools/
* keyman ( https://keyman.com/ ) - compatible with Mac, Windows & Linux

# Installation
* If there is a .kmp file matching your physical keyboard in the [keyboards](https://github.com/PhilHen/HieroglyphicKeyboards/tree/main/keyboards) folder, download that file and use keyman to install it on your system (keyman should be the default handler for .kmp file). Currently this is only applicable to the Belgian "azerty be" layout.
* Otherwise
  ** download the entire cldrbuilder folder with subfolders from this repository
  ** modify the xml file sources/localized.xml according to your needs
  ** modify the global constants in code/buildCldrHiero.py (if needed)
  ** run code/buildCldrHiero.py , which will generate an xml file in the output folder
  ** open keyman developer (windows only), new project, LDML Keyboard - paste the generated xml file
  ** compile and install
  It IS possible to build the keyboard on a linux or apple computer, using [keyman developer command tools](https://help.keyman.com/developer/14.0/guides/command-line)
  


# How to use the keyboard
Once the keyboard is installed, switch to that keyboard (refer to the [keyman documentation](https://help.keyman.com/)).

Signs encoding is similar to JSesh. Except for Egyptian hieroglyph format controls (see below), the keystrokes listed below act on the character (latin or hieroglyphic) immediately preceding the cursor.
What follows is based on the Azerty Belgian keyboard layout. 
*\<v\> means the key "v"
* abc means the text abc, typed in the usual manner
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

## Format controls
See https://unicode.org/charts/PDF/U13430.pdf 
| Keyboard keys (azerty be) | Result |
| --- | --- |
| \<v\> then \<SPACE\><br/>/vj then \<SPACE\><br/>vj/ then \<SPACE\><br/> vj then \<SPACE\><br/>\<:\> then \<SPACE\>|vertical joiner (":" in JSesh, "subordination" in MdC)|
| \<c\> then \<SPACE\><br/>/hj then \<SPACE\><br/>hj/ then \<SPACE\><br/> hj then \<SPACE\><br/>\<*\> then \<SPACE\>|horizontal joiner ("*" in JSesh, "juxtaposition" in MdC)|
| ss then \<SPACE\><br/>/ss then \<SPACE\><br/>ss/ then \<SPACE\><br/>\<ALTGR\> + \<ç\>|begin segment (gives control over the sequence of application of format controls)|
| se then \<SPACE\><br/>/se then \<SPACE\><br/>se/ then \<SPACE\><br/>\<ALTGR\> + \<à\>|end segment (gives control over the sequence of application of format controls)|

Inserts can be done at 7 positions, as illustrated below. Note that it is preferred to use the mi/ syntax (with a forward slash at the end /), since other syntaxes may collide with phonetic sign abreviations (e.g. mi = 𓏇)

 <img src="https://raw.githubusercontent.com/PhilHen/HieroglyphicKeyboards/refs/heads/main/images/inserts.png"  />

| Keyboard keys (azerty be) | Result |
| --- | --- |
| ts then \<SPACE\><br/>/ts then \<SPACE\><br/>ts/ then \<SPACE\>|insert the sign that follows at the top start (i.e. top left if writing left-to-right) of the sign that precedes the cursor|
| /ti then \<SPACE\><br/>ti/ then \<SPACE\>|insert the sign that follows at the top of the sign that precedes the cursor|
| te then \<SPACE\><br/>/te then \<SPACE\><br/>te/ then \<SPACE\>|insert the sign that follows at the top end (i.e. top right if writing left-to-right) of the sign that precedes the cursor|
| /mi then \<SPACE\><br/>mi/ then \<SPACE\>|insert the sign that follows at the middle of the sign that precedes the cursor|
| /bs then \<SPACE\><br/>bs/ then \<SPACE\>|insert the sign that follows at the bottom start (i.e. bottom left if writing left-to-right) of the sign that precedes the cursor|
| /mi then \<SPACE\><br/>mi/ then \<SPACE\>|insert the sign that follows at the bottom of the sign that precedes the cursor|
| be then \<SPACE\><br/>/be then \<SPACE\><br/>be/ then \<SPACE\>|insert the sign that follows at the bottom end (i.e. bottom right if writing left-to-right) of the sign that precedes the cursor|
| om then \<SPACE\><br/>/om then \<SPACE\><br/>om/ then \<SPACE\>|overla𓏭(stack) the sign that follows over the sign that precedes the cursor|


TO DO:
* transliteration
* blank signs/lacunae
* damage modifiers
 <img src="https://raw.githubusercontent.com/PhilHen/HieroglyphicKeyboards/refs/heads/main/images/4quadrants.png"  />

 
* mirror
* cartouche / enclosure 
* numbers


