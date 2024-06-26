Set up environment variable

mkdir bot_interface
cd bot_interface
python3 -m venv venv
source venv\Scripts\activate

pip install flask openai

export OPENAI_API_KEY='your_openai_api_key_here'