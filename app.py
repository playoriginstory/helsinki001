from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import replicate

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the Replicate client with your API token
client = replicate.Client(api_token=os.environ['REPLICATE_API_TOKEN'])

@app.route('/')
def home():
    # This route will render your home page
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    # Check which form was submitted
    if 'moon_input' in request.form:
        user_input = request.form['moon_input']
        # Prompt for the moon section
        prompt = f'a still from a film "a cold December night", low snowfall, winters, purples, and blues, abstract shot on the moon, {user_input} on the surface of the Moon, no walls, detailed, cinematic'
    elif 'car_input' in request.form:
        user_input = request.form['car_input']
        # Prompt for the car section
        prompt = f'rear view of a {user_input}, indie film, surrealism, symmetrical, vibrant colors, nostalgic, bluebonnets, cinematic, evening sun' 
    elif 'ramithawi_input' in request.form:
        user_input = request.form['ramithawi_input']
        # Prompt for the ramithawi section
        prompt = f'still from a film, photorealistic, a classic hand-drawn 3D animation, close up of felt puppets {user_input} , classy, ancient, tribal in a forest in the 1800's greens, oranges, blacks, reds, golds, styled like a classical painting, cinematic'
    elif 'tropical_input' in request.form:
        user_input = request.form['tropical_input']
        # Prompt for the tropical section
        prompt = f'{user_input} from an all {user_input} penthouse, HD, coming off the water, cinematic'
    else:
        # Default case if no known form was submitted
        return "Invalid form submission", 400

    # Run the model with the prompt
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input={"prompt": prompt}
    )
    
    # Directly print the output to debug
    print(output)

    # Assuming the output contains a direct link to the generated image
    generated_image_url = output[0] if isinstance(output, list) else None

    return render_template('result.html', image=generated_image_url)

if __name__ == '__main__':
    # Use the PORT environment variable if available, otherwise use 5000 as a fallback
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
