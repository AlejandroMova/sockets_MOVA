
REM Set the variables
set HOST=m1.server.mx
set CALL=pull

REM Run the Python script with the specified arguments
python client.py --host=%HOST% --call=%CALL%

REM Pause to keep the command prompt open after the script runs
pause
