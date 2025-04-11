import openai
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request


load_dotenv()
openai.api_key = os.getenv('FANFICGEN_API_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # The form HTML file
@app.route('/generate', methods=['POST'])
def generate():
    fandom= request.form['fandom']
    main_character_type = request.form['main_character_type']  # self_insert or character
    if main_character_type == 'self_insert':
        main_character = request.form['main_character']  # The name from the self-insert text box
    elif main_character_type == 'character':
        main_character = request.form['character_name'] 
    main_character_traits= request.form['main_character_traits']
    love_interest = request.form['love_interest']
    love_interest_traits = request.form['love_interest_traits']
    tropes= request.form['tropes']
    setting= request.form['setting']
    conflict = request.form['conflict'] if 'conflict' in request.form else "No conflict provided"
    word_length = request.form['word_length']

    return generate_fanfic_gpt3(fandom, main_character, main_character_traits, love_interest, love_interest_traits, tropes, setting, conflict, word_length)

def generate_fanfic_gpt3(fandom, main_character, main_character_traits, love_interest, love_interest_traits, tropes, setting, conflict, word_length):
        prompt = f"""
        Write a {word_length} word romance fanfic for {fandom}. The main character is {main_character} who has the traits {main_character_traits}, and they are falling in love with {love_interest} who has the following traits: {love_interest_traits}.
        The relationship should have {tropes} tropes and the setting/ universe should be {setting}. The story should include the following conflict: {conflict}.
        """
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the appropriate model here
             messages=[
            {"role": "system", "content": "You are a helpful assistant that generates romance fanfics."},
            {"role": "user", "content": prompt}
        ],
            max_tokens = int(int(word_length) * 1.33),  # Estimate of word count
            temperature=0.7
        )

        return response.choices[0].message.content.strip()



if __name__ == '__main__':
    app.run(debug=True)
