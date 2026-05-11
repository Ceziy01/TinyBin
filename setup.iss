[Setup]
AppName=TinyBin
AppVersion=0.2.2
AppPublisher=Ceziy
DefaultDirName={autopf}\TinyBin
DefaultGroupName=TinyBin
OutputBaseFilename=TinyBinInstaller
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\bin.ico
UninstallIconFile=assets\bin.ico
WizardStyle=modern
OutputDir=installer

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "app/TinyBin/TinyBin.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "app/TinyBin/source/*"; DestDir: "{app}/source"; Flags: ignoreversion recursesubdirs
Source: "assets/bin.ico"; DestDir: "{app}/assets"; Flags: ignoreversion
Source: "assets/bin.png"; DestDir: "{app}/assets"; Flags: ignoreversion
Source: "assets/bundle.png"; DestDir: "{app}/assets"; Flags: ignoreversion
Source: "assets/bin_inv.png"; DestDir: "{app}/assets"; Flags: ignoreversion

[UninstallRun]
Filename: "{cmd}"; Parameters: "/C ""taskkill /im TinyBin.exe /f /t"; Flags: runhidden
Filename: "{cmd}"; Parameters: "/C reg delete ""HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"" /v TinyBin /f"; Flags: runhidden

[UninstallDelete]
Type: files; Name: "{app}\settings.json"
Type: dirifempty; Name: "{app}"

[Icons]
Name: "{autoprograms}\TinyBin"; Filename: "{app}\TinyBin.exe"; IconFilename: "{app}\assets\bin.ico"

[Run]
Filename: "{app}\TinyBin.exe"; Description: "{cm:LaunchProgram,TinyBin}"; Flags: nowait postinstall skipifsilent

[Dirs]
Name: "{app}"; Permissions: everyone-full