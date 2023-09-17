from flask import Flask, render_template, request, g, redirect, url_for, flash, jsonify
import image_macro_generator, image_macros_ocr, llm_api
from PIL import Image
import io, base64, json

app = Flask(__name__)

def pil_to_base64(image):
    buffer = io.BytesIO()
    image.save(buffer, "PNG")
    return str(base64.b64encode(buffer.getvalue()), 'UTF-8')

def base64_to_uri(encrypted):
    return r"data:image/png;base64," + encrypted

@app.post('/ocr-text')
def api_ocr_text():
    template = Image.open(request.files['template-image'].stream)
    images_streams = request.files.getlist('example-images')

    response = []
    for stream in images_streams:
        image = Image.open(stream)
        processed = image_macros_ocr.isolate_image_text(image, template)
        text = image_macros_ocr.extract_top_bottom_text(processed)

        response.append({
            'original': base64_to_uri(pil_to_base64(image)),
            'processed': base64_to_uri(pil_to_base64(processed)),
            'text': text
        })

    return jsonify(response)

@app.post('/generate-macros')
def api_generate_macros():
    template = Image.open(request.files['template-image'].stream)
    topic = request.form['topic']
    top_text = request.form['top-text']
    examples = json.loads(request.form['examples'])

    bottom_texts = llm_api.generate_text(examples, topic, top_text, num_gens=5)
    macros = []
    for bottom_text in bottom_texts:
        macros.append(image_macro_generator.generate_macro(template, top_text, bottom_text))
    
    response = [base64_to_uri(pil_to_base64(image)) for image in macros]
    return response

@app.get('/')
def page_index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
