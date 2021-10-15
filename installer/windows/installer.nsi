!include MUI2.nsh
!include FileFunc.nsh
!define MUI_ICON "###ICON###"
!define MUI_UNICON "###ICON###"

!getdllversion "###APP###" ver
!define VERSION "###VERSION###"

VIProductVersion "${VERSION}"
VIAddVersionKey "ProductName" "###APP_NAME###"
VIAddVersionKey "FileVersion" "${VERSION}"
VIAddVersionKey "ProductVersion" "${VERSION}"
VIAddVersionKey "LegalCopyright" "###AUTHOR###"



# perform system-level install if possible

!define MULTIUSER_EXECUTIONLEVEL Highest
# add support for command-line args that let uninstaller know whether to
# uninstall system- or user installation:
!define MULTIUSER_INSTALLMODE_COMMANDLINE
!include MultiUser.nsh
!include LogicLib.nsh

Function .onInit
  !insertmacro MULTIUSER_INIT
  ${If} $InstDir == ""
      ${If} $MultiUser.InstallMode == "AllUsers"
          StrCpy $InstDir "$PROGRAMFILES\###APP_NAME###"
      ${Else}
          StrCpy $InstDir "$LOCALAPPDATA\###APP_NAME###"
      ${EndIf}
  ${EndIf}
FunctionEnd

Function un.onInit
  !insertmacro MULTIUSER_UNINIT
FunctionEnd



# general

  Name "###APP_NAME###"
  OutFile "###OUTPUT###"



# interface settings

  !define MUI_ABORTWARNING



# pages

  !define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of ###APP_NAME###.$\r$\n$\r$\n$\r$\nClick Next to continue."
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
    !define MUI_FINISHPAGE_NOAUTOCLOSE
    !define MUI_FINISHPAGE_RUN
    !define MUI_FINISHPAGE_RUN_CHECKED
    !define MUI_FINISHPAGE_RUN_TEXT "Run ###APP_NAME###"
    !define MUI_FINISHPAGE_RUN_FUNCTION "LaunchAsNonAdmin"
  !insertmacro MUI_PAGE_FINISH
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES



# languages

  !insertmacro MUI_LANGUAGE "English"



# installer sections

!define UNINST_KEY \
  "Software\Microsoft\Windows\CurrentVersion\Uninstall\###APP_NAME###"
Section
  SetOutPath "$InstDir"
  File /r "###APP###/*"
  WriteRegStr SHCTX "Software\###APP_NAME###" "" $InstDir
  WriteUninstaller "$InstDir\uninstall.exe"
  CreateShortCut "$SMPROGRAMS\###APP_NAME###.lnk" "$InstDir\###APP_NAME###.exe"
  WriteRegStr SHCTX "${UNINST_KEY}" "DisplayName" "###APP_NAME###"
  WriteRegStr SHCTX "${UNINST_KEY}" "UninstallString" \
    "$\"$InstDir\uninstall.exe$\" /$MultiUser.InstallMode"
  WriteRegStr SHCTX "${UNINST_KEY}" "QuietUninstallString" \
    "$\"$InstDir\uninstall.exe$\" /$MultiUser.InstallMode /S"
  WriteRegStr SHCTX "${UNINST_KEY}" "Publisher" "###AUTHOR###"
  WriteRegStr SHCTX "${UNINST_KEY}" "DisplayIcon" "$InstDir\uninstall.exe"
  ${GetSize} "$InstDir" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD SHCTX "${UNINST_KEY}" "EstimatedSize" "$0"
SectionEnd



# uninstaller section

Section "Uninstall"
  RMDir /r "$InstDir"
  Delete "$SMPROGRAMS\###APP_NAME###.lnk"
  DeleteRegKey /ifempty SHCTX "Software\###APP_NAME###"
  DeleteRegKey SHCTX "${UNINST_KEY}"
SectionEnd

Function LaunchAsNonAdmin
  Exec '"$WINDIR\explorer.exe" "$InstDir\###APP_NAME###.exe"'
FunctionEnd