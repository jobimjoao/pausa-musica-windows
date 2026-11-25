' Roda o monitor sem janela. Coloque um atalho deste arquivo em shell:startup
' para iniciar junto com o Windows.
Set sh = CreateObject("WScript.Shell")
pasta = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
sh.Run "pythonw """ & pasta & "\pausa_musica.py""", 0, False
