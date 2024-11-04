[Setup]
AppName=TinyBin
AppVersion=0.1.2
AppPublisher=Ceziy
DefaultDirName={pf}\TinyBin
DefaultGroupName=TinyBin
OutputBaseFilename=TinyBinInstaller
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Users\cesiy\Desktop\d2\python\minibin\app\bin.ico
UninstallIconFile=C:\Users\cesiy\Desktop\d2\python\minibin\app\bin.ico
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "armenian"; MessagesFile: "compiler:Languages\Armenian.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "bulgarian"; MessagesFile: "compiler:Languages\Bulgarian.isl"
Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"
Name: "corsican"; MessagesFile: "compiler:Languages\Corsican.isl"
Name: "czech"; MessagesFile: "compiler:Languages\Czech.isl"
Name: "danish"; MessagesFile: "compiler:Languages\Danish.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "finnish"; MessagesFile: "compiler:Languages\Finnish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "hebrew"; MessagesFile: "compiler:Languages\Hebrew.isl"
Name: "hungarian"; MessagesFile: "compiler:Languages\Hungarian.isl"
Name: "icelandic"; MessagesFile: "compiler:Languages\Icelandic.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"
Name: "norwegian"; MessagesFile: "compiler:Languages\Norwegian.isl"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "slovak"; MessagesFile: "compiler:Languages\Slovak.isl"
Name: "slovenian"; MessagesFile: "compiler:Languages\Slovenian.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"
Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"

[Files]
Source: "TinyBin.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin_inv.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "settings.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "eng.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "rus.json"; DestDir: "{app}"; Flags: ignoreversion

[UninstallRun]
Filename: "{cmd}"; Parameters: "/C ""taskkill /im TinyBin.exe /f /t"; Flags: runhidden
Filename: "{cmd}"; Parameters: "/C reg delete ""HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"" /v TinyBin /f"; Flags: runhidden

[Icons]
Name: "{autoprograms}\TinyBin"; Filename: "{app}\TinyBin.exe"; IconFilename: "{app}\bin.ico"

[Run]
Filename: "{app}\TinyBin.exe"; Description: "{cm:LaunchProgram,TinyBin}"; Flags: nowait postinstall skipifsilent

[Dirs]
Name: "{app}"; Permissions: everyone-full