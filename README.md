## Usage
### Locally
1. Clone the repo
2. `cd backend-automation`
3. Setup Virtual Environment
   - Linux/Mac:
     * `scripts/setup_env.sh`  
   - Windows CMD:
     * `scripts/setup_env.bat`
   - Windows Powershell:
     * `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
     * `.\scripts\setup_env.bat`
4. Enter the Python VENV
   - Linux/Mac:
     * `source ~/python_core_env/bin/activate`
   - Windows CMD:
     * `%HOMEDRIVE%%HOMEPATH%\python_core_env\Scripts\activate.bat`
   - Windows Powershell:
     * `&$env:userprofile\python_core_env\Scripts\Activate.ps1`
5. Run tests
   * `pytest --host=api.dev.kingpin.global --username=${Your_login} --password=${Your_password} --log-cli-level=INFO -s core/tests/`

