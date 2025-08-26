import google.generativeai as genai

API_KEY = "AIzaSyBHBhQn0iqqa7UpJkRa6SBCsCfRzFK2Ha8"
genai.configure(api_key=API_KEY)

for m in genai.list_models():
    print(m.name)


