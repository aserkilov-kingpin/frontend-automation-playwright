$SCRIPT_DIR=(get-item $PSScriptRoot ).parent.FullName
Write-Host "CREATING PYTHON VENV python_env_playwright"
python -m venv $env:userprofile\python_env_playwright
Write-Host "SOURCING VENV"
$Script = $env:userprofile + "\python_env_playwright\Scripts\Activate.ps1"
(Get-Content $Script) |
    Foreach-Object {
        if ($_ -match "# SIG # Begin signature block")
        {
            '$env:PYTHONPATH=' + "`"$SCRIPT_DIR`""
            '$env:MYPYPATH=' + "`"$SCRIPT_DIR`""
            ''
        }
        $_
    } | Set-Content $Script
&$Script
Write-Host "UPGRADING PIP"
python -m pip install --upgrade pip
Write-Host "INSTALLING PACKAGES"
pip install --no-cache-dir -r $SCRIPT_DIR\scripts\requirements.txt
