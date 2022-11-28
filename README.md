## Usage
### Locally
1. Clone the repo
2. `cd frontend-automation-playwright`
3. Setup Virtual Environment
   - Linux/Mac:
     * `scripts/setup_env.sh`  
   - Windows CMD:
     * `scripts/setup_env.bat`
   - Windows Powershell:
     * `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
     * `scripts/setup_env.ps1`
4. Enter the Python VENV
   - Linux/Mac:
     * `source ~/python_env_playwright/bin/activate`
   - Windows CMD:
     * `%HOMEDRIVE%%HOMEPATH%\python_env_playwright\Scripts\activate.bat`
   - Windows Powershell:
     * `&$env:userprofile\python_env_playwright\Scripts\Activate.ps1`
5. Upgrade packages:
   - Windows Powershell:
     * `pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}`
6. Install playwright:
   * `playwright install`
7. Run tests
   * `pytest --base-url=https://dev.kingpin.global --host=https://dev.kingpin.global --api=https://api-dev.kingpin.global --log-cli-level=INFO -s tests\portal --no-header`

