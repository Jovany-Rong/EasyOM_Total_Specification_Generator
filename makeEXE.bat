d:
cd D:\dev\python3\EasyOM_Total_Specification_Generator

del *.spec
rd /s /q build 
rd /s /q dist

pyinstaller -F -i "icon.ico" "EasyOM_TSG.py"

xcopy conf dist\conf\ /s
md dist\Input
md dist\Output

del *.spec
rd /s /q build

pause