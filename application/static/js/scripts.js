var drag_area = document.getElementById("drag_area");
var drag_text = document.getElementById("drag_text");
var dropped_image = document.getElementById("dropped_image");
var image_uploader = document.getElementById('image_uploader');
var submit_btn = document.getElementById('submit_btn');

function nav_to_dominant_color_route(ele, url) {
    ele.children[0].innerText = "Generating";
    window.location.href = url;
};

function nav_to_chose_color_route(ele, url) {
    ele.children[0].innerText = "Generating";
    window.location.href = url;
};

function search_input_auto_fill(text) {
    var search_input = document.getElementById('search_input');
    if (search_input) {
        search_input.value = text.trim();
    }
}

function nav_to_online_search(ele, d_color, c_color) {
    var search_input = document.getElementById('search_input');
    if (search_input) {
        var value = search_input.value;
        value = value.trim();
        if (value == "") {
            alert("Please provide input value");
        } else {
            if (ele == "amazon") {
                var url = "https://www.amazon.in/s?k=" + c_color + " color " + value;
                window.open(url, '_blank');
            }
            else if (ele == "flipkart") {
                var url = "https://www.flipkart.com/search?q=" + c_color + " color " + value;
                window.open(url, '_blank');
            } else if (ele == "myntra") {
                var url = "https://www.myntra.com/" + c_color + " color " + value;
                window.open(url, '_blank');
            } else if (ele == "meesho") {
                var url = "https://www.meesho.com/search?q=" + c_color + " color " + value;
                window.open(url, '_blank');
            } else if (ele == "ajio") {
                var url = "https://www.ajio.com/search/?text=" + c_color + " color " + value;
                window.open(url, '_blank');
            }
        }
    }
};

function previewImage(files) {
    if (files.length > 1) {
        alert("Please select one image");
        drag_text.textContent = "Drag & Drop the image here";
    } else if (!files[0].type.startsWith("image")) {
        alert("Please select valid image file");
        drag_text.textContent = "Drag & Drop the image here";
    } else {
        let fileReader = new FileReader();
        fileReader.onload = () => {
            let fileURL = fileReader.result;
            drag_text.hidden = true;
            dropped_image.setAttribute('src', fileURL);
            dropped_image.hidden = false;
            submit_btn.hidden = false;
        };
        fileReader.readAsDataURL(files[0]);
    }
}

if (submit_btn) {
    submit_btn.addEventListener("click", () => {
        submit_btn.innerText = "Generating";
        submit_btn.style.backgroundColor = "var(--text)";
    });
}


if (image_uploader) {
    image_uploader.addEventListener("change", function () {
        previewImage(this.files);
    });
}


if (drag_area) {
    if (drag_text) {

        drag_area.addEventListener("click", () => {
            image_uploader.click();
        });

        // If user drag the video over the drag area
        drag_area.addEventListener("dragover", (event) => {
            event.preventDefault();
            drag_text.textContent = "Release to upload the video";
            drag_area.style.border = "2px solid #000";
        });

        // If user leave the video from drag area
        drag_area.addEventListener("dragleave", (event) => {
            event.preventDefault();
            drag_text.textContent = "Drag & Drop the video here";
            drag_area.style.border = "2px dashed #000";
        });

        // If video is drop on drag area
        drag_area.addEventListener("drop", (event) => {
            event.preventDefault();
            previewImage(event.dataTransfer.files);
            image_uploader.files = event.dataTransfer.files;
        });
    }
}

