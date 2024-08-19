streamlit:
	streamlit run streamlit_app.py

edit:
	emacs streamlit_app.py &

lint:
	black . 
	flake8 . --max-line-length=91

build_pip:
	pip-compile resources/requirements.in -o requirements.txt

install_env:
	pip install pip --upgrade
	pip install -r requirements.txt
	pip install black flake8 pip-tools

core_dependencies:
	pyenv install 3.12.0
	pyenv virtualenv 3.12.0 inbxo

#	pyenv activate inbxo # Run in shell

