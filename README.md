# HieroglyphicKeyboards
Set of tools aimed at facilitating the creation and usage of keyman hieroglyphic keyboards (based on Andrew Glass' qwerty hieroglyphic keyboard - the tools in this repository only slightly expand and internationalize Andrew's work)
Current version supports :
* creating keyboards based on non-qwerty layouts (for instance Belgian AZERTY)
* using JSesh-cycles based on phonetic shortcuts (such as aA -> 𓉻->𓃘 -> 𓉼 -> 𓉿 -> 𓉻 )
* adding user-defined shortcuts


# Requirements
* "Egyptian Text" font to be found at https://github.com/microsoft/font-tools/
* keyman ( https://keyman.com/ ) - compatible with Mac, Windows & Linux

# Installation
* If there is a .kmp file matching your physical keyboard in the [keyboards](https://github.com/PhilHen/HieroglyphicKeyboards/tree/main/keyboards) folder, download that file and use keyman to install it on your system (keyman should be the default handler for .kmp file). Currently this is only applicable to the Belgian "azerty be" layout (https://www.kbdlayout.info/kbdbe).
* Otherwise you will need to install Keyman developer, to modify the localized keyboard definition and to run a python script.
   * download the entire cldrbuilder folder with subfolders from this repository
   * modify the xml file sources/localized.xml according to your needs
   * modify the global constants in code/buildCldrHiero.py (if needed)
   * run code/buildCldrHiero.py , which will generate an xml file in the output folder
   * open keyman developer (windows only), new project, LDML Keyboard - paste the contents of the generated xml file
   * using keyman developer, compile the keyboard and install it

It IS possible to build the keyboard on a linux or apple computer, using [keyman developer command tools](https://help.keyman.com/developer/14.0/guides/command-line)
  


# How to use the keyboard
Once the keyboard is installed, switch to that keyboard (refer to the [keyman documentation](https://help.keyman.com/)).

Keys are specific to the hardware layout, and usage instructions can therefore be found in layout-specific help pages
* [azerty-be instructions](https://github.com/PhilHen/HieroglyphicKeyboards/wiki/Using-the-azerty%E2%80%90be-keyboard)
* qwerty-us instructions (TO BE COMPLETED)
