@echo off
REM Point public\Prime Books at the MEGA masters as a junction, or remove it.
REM
REM WHY A JUNCTION: the repo used to hold a 27 GB byte-for-byte COPY of the
REM masters inside public\. That copy carried PDF\Input (third-party publisher
REM material kept for scope only), teacher feedback and build exhaust, and it
REM had already DRIFTED from MEGA (nine files existed only in the copy). With a
REM junction there is exactly ONE tree of truth: the path
REM   public\Prime Books\1. Lower Primary\Year 01\Art & Design\PDF\Output\...
REM resolves to the MEGA master, and editing either path edits the same bytes.
REM
REM It is gitignored, so nothing here is ever committed or deployed. The public
REM site is served from public\library\, built by tools\sync_library.py.
REM
REM   tools\link_books.cmd          create or refresh the junction
REM   tools\link_books.cmd remove   remove the junction (masters untouched)
setlocal
set LINK=C:\Users\alexa\Documents\GitHub\prime-books\public\Prime Books
set TARGET=C:\Users\alexa\Documents\MEGA\Projects\Prime Books\BOOKS

if exist "%LINK%" (
  echo Removing existing link: "%LINK%"
  rmdir "%LINK%"
)
if /I "%~1"=="remove" (
  echo Removed. The masters at "%TARGET%" are untouched.
  goto :done
)
mklink /J "%LINK%" "%TARGET%"
:done
dir /AL "C:\Users\alexa\Documents\GitHub\prime-books\public"
endlocal
