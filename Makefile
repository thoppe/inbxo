streamlit:
	streamlit run streamlit_app.py

edit:
	emacs streamlit_app.py &

lint:
	black . 
	flake8 . --max-line-length=91

