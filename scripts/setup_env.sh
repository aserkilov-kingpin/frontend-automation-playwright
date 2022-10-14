SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )"/.. &> /dev/null && pwd )"
echo "CREATING PYTHON VENV python_env_playwright"
python3 -m venv ~/python_env_playwright
echo "export PYTHONPATH=$SCRIPT_DIR" >> ~/python_env_playwright/bin/activate
echo "export MYPYPATH=$SCRIPT_DIR" >> ~/python_env_playwright/bin/activate
echo "SOURCING VENV"
source ~/python_env_playwright/bin/activate
echo "UPGRADING PIP"
python3 -m pip install --upgrade pip
echo "INSTALLING PACKAGES"
pip3 install --no-cache-dir -r ${SCRIPT_DIR}/scripts/requirements.txt
