.\venv\Scripts\Activate.ps1

Write-Output mypy...
mypy . 

Write-Output lint...
pylint app test --ignore="venv,test\snapshots" --disable="fixme,duplicate-code"

Write-Output pytest...
pytest --quiet
