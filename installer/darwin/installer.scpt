tell application "Finder"
  tell disk "###APP_NAME###"
    open
    set current view of container window to icon view
    set toolbar visible of container window to false
    set statusbar visible of container window to false
    set the bounds of container window to {200, 120, 800, 530}
    set theViewOptions to the icon view options of container window
    set arrangement of theViewOptions to not arranged
    set icon size of theViewOptions to 106
    set background picture of theViewOptions to file ".background:###BACKGROUND###"
    make new alias file at container window to POSIX file "/Applications" with properties {name:"Applications"}
    set position of item "###APP_NAME###" of container window to {150, 180}
    set position of item "Applications" of container window to {450, 180}
    update without registering applications
    delay 5
    close
  end tell
end tell