import os
import uuid
from application import app
from imageai.Detection import ObjectDetection
from flask import render_template, request, url_for, redirect
from application.constant import getColorAPIData, rrmdir
from application.decode_image import maxColorInImage
import requests

detector = ObjectDetection()

execution_path = os.getcwd()

@app.route('/')
def index():
    detector.useCPU()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(os.path.join(execution_path, r"application\aimodel\tiny-yolov3.pt"))
    detector.loadModel()
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        input_file = request.files['image_uploader']
        id = uuid.uuid4()
        final_file_name = f"image_{id}.jpg"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], final_file_name)
        input_file.save(image_path)
        return redirect(url_for('image_route', image_id=id))

@app.route('/<image_id>')
def image_route(image_id):
    final_file_name = f"image_{image_id}.jpg"
    url = url_for('static', filename=f'images/{final_file_name}')
    
    color_details = []
    image_path = os.path.join(execution_path, r"application\static\images", final_file_name)

    imagenew_extracted_folder_path = os.path.join(execution_path , "imagenew-extracted")
    if os.path.exists(imagenew_extracted_folder_path):
        rrmdir(imagenew_extracted_folder_path)

    detections, extracted_images = detector.detectObjectsFromImage(
        input_image=image_path, 
        output_image_path=os.path.join(execution_path , "imagenew.jpg"), 
        extract_detected_objects=True, 
        minimum_percentage_probability=30,
        display_box=True,
    )

    person_image_path = ""
    for eachObject, eachImage in zip(detections, extracted_images):
        print(eachObject["name"])
        if eachObject["name"] == "person":
            person_image_path = eachImage
            break
    
    scan_image_path = ""

    if person_image_path:
        scan_image_path = person_image_path
    else:
        scan_image_path = image_path
    
    print(f"INFO  :: Finding dominant color in {scan_image_path}")

    colors = maxColorInImage(scan_image_path)
    for color in colors:
        try:
            api_url = f"https://www.thecolorapi.com/id?rgb=rgb({color[0]},{color[1]},{color[2]})"
            response = getColorAPIData(api_url)
        except Exception as e:
            print(f'ERROR : {e}')
            return render_template("error_view.html", url = url)
        color_details.append(response.json())
    return render_template("image_view.html", url = url, image_id=image_id, color_details = color_details)

@app.route('/<image_id>/<dominant_color_code>')
def dominant_color_route(image_id, dominant_color_code):
    final_file_name = f"image_{image_id}.jpg"
    url = url_for('static', filename=f'images/{final_file_name}')
    schemes = ['complement', 'quad']
    # Choices: monochrome monochrome-dark monochrome-light analogic complement analogic-complement triad quad
    
    # getting more data on choosen color
    dominant_color = ''
    try:
        api_url = f"https://www.thecolorapi.com/id?hex={dominant_color_code}"
        response = getColorAPIData(api_url)
    except Exception as e:
        print(f'ERROR : {e}')
        return render_template("error_view.html", url = url)
    dominant_color = response.json()
    
    # adding once more monochrome scheme to schemes based on constract
    contrast = dominant_color['contrast']['value']
    if contrast == "#000000":
        schemes.append('monochrome-light')
    else:
        schemes.append('monochrome-dark')
    

    # color_data dict for store scheme color data
    color_data = {}

    # getting more data on constract
    try:
        contrast = contrast.replace('#', "")
        api_url = f"https://www.thecolorapi.com/id?hex={contrast}"
        response = getColorAPIData(api_url)
    except Exception as e:
        print(f'ERROR : {e}')
        return render_template("error_view.html", url = url)
    
    contrast_color = response.json()
    color_data[contrast_color['hex']['value']] = contrast_color
    
    # finding all color schemes and adding to color_data
    for scheme in schemes:
        try:
            api_url = f"https://www.thecolorapi.com/scheme?hex={dominant_color_code}&mode={scheme}"
            response = getColorAPIData(api_url)
        except Exception as e:
            print(f'ERROR : {e}')
            return render_template("error_view.html", url = url)
        data = response.json()
        
        # avoiding dupilicate color stored in color_data dict
        for each_color in data['colors']:
            if (each_color['name']['value'] not in color_data) and (each_color['name']['value'] != dominant_color['name']['value']):
                color_data[each_color['name']['value']] = each_color
    return render_template("dominant_color_view.html", url = url, image_id=image_id, dominant_color = dominant_color, color_data = color_data)

@app.route('/<image_id>/<dominant_color_code>/<chose_color_code>')
def chose_color_route(image_id, dominant_color_code, chose_color_code):
    final_file_name = f"image_{image_id}.jpg"
    url = url_for('static', filename=f'images/{final_file_name}')

    # getting more data on choosen color
    dominant_color = ''
    try:
        api_url = f"https://www.thecolorapi.com/id?hex={dominant_color_code}"
        response = getColorAPIData(api_url)
    except Exception as e:
        print(f'ERROR : {e}')
        return render_template("error_view.html", url = url)
    dominant_color = response.json()

    # getting more data on choosen color
    chose_color = ''
    try:
        api_url = f"https://www.thecolorapi.com/id?hex={chose_color_code}"
        response = getColorAPIData(api_url)
    except Exception as e:
        print(f'ERROR : {e}')
        return render_template("error_view.html", url = url)
    chose_color = response.json()

    return render_template("chose_color_view.html", url = url, image_id=image_id, dominant_color = dominant_color, chose_color = chose_color)