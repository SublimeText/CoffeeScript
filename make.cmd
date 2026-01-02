@echo off
setlocal
chcp 65001 >nul
pushd %~dp0

if /i "%1" == "release" goto RELEASE
goto :usage

:RELEASE
    if "%2"== "" goto :usage

    for %%d in ("%~dp0.") do set package=%%~nxd

    echo Createing assets for "%package%"...

    set build=4143
    set archive=%package%.sublime-package
    call git archive --format zip -o "%archive%" master

    :: create the release
    gh release create --target master -t "v%2" "%build%-%2" *.sublime-package
    del /f /q *.sublime-package
    git fetch
    goto :eof

:USAGE
    echo USAGE:
    echo.
    echo   make ^[release^]
    echo.
    echo   release ^<semver^> -- create and publish a release (e.g. 1.2.3)
    goto :eof
