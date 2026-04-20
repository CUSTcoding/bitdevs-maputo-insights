import pandas as pd
from pathlib import Path
from deep_translator import GoogleTranslator

df = pd.read_csv("data/bitdevsinquete.csv")

df.columns = [
    'Timestamp',
    '1. Are you a software developer?',
    '2. What is your current level as a software developer?', 
    '3. Which technologies do you work with? (select all that apply)', 
    '4. How many years of programming experience do you have?', 
    '5. Do you know Bitcoin?', 
    '6. If not, are you interested in learning about Bitcoin?', 
    '7. Would you participate in a Bitcoin developer community in Maputo (BitDevs Maputo)?', 
    '8. What would most motivate you to participate and stay active in the community? (select all that apply)', 
    '9. What do you expect to achieve by participating in the community?', 'Email address'
    ]


cols_to_translate = [
    "2. What is your current level as a software developer?",
    "3. Which technologies do you work with? (select all that apply)",
    "4. How many years of programming experience do you have?",
    "8. What would most motivate you to participate and stay active in the community? (select all that apply)",
    "9. What do you expect to achieve by participating in the community?"
]

def normalize_yes_no(text):
    if pd.isna(text):
        return text

    return str(text).strip().lower()



yes_no_map = {
    "sim": "yes",
    "não": "no",
    "nao": "no",
    "talvez": "maybe"
}

for col in [
    "1. Are you a software developer?",
    "5. Do you know Bitcoin?",
    "6. If not, are you interested in learning about Bitcoin?",
    "7. Would you participate in a Bitcoin developer community in Maputo (BitDevs Maputo)?"
]:
    df[col] = df[col].apply(normalize_yes_no).map(yes_no_map)

    
cache = {}

def translate(text):

    if pd.isna(text):
        return text

    text = str(text).strip()

    if text in cache:
        return cache[text]

    try:
        translated = GoogleTranslator(source="pt", target="en").translate(text)
        cache[text] = translated
        return translated
    except:
        return text

for col in cols_to_translate:
    df[col + "_en"] = df[col].apply(translate)

output_dir = Path("en_translate")
output_dir.mkdir(exist_ok=True)

df.to_csv(output_dir / "bitdevsinquete.csv", index=False)

print(df.head())