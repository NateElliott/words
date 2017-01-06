function updateUpload() {

    var output = document.getElementById('filename');
    var input = document.getElementById('upload');

    var filename = upload.value;
    var lastIndex = filename.lastIndexOf("\\");
    if (lastIndex >= 0) {
        filename = filename.substring(lastIndex + 1);
    }

    output.innerHTML = filename;
}