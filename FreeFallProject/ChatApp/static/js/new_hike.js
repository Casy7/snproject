cropper.start(document.getElementById("testCanvas"), 0.6);

function readURL() {
    // document.getElementById("testCanvas").style.height = "400px";
    var myimg = document.getElementById("myimg");
    var input = document.getElementById("myfile");
    var field = document.createElement("canvas");
    // field.id = 'testCanvas';
    // field.name = 'image';
    
    // field.width = '600';
    // field.height = '300';
    // field.style.cursor = 'move';
    // document.getElementById.appendChild(field);
    document.getElementById("image_crop").style.display = "block";
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            console.log("changed");
            var data = e.target.result;
            myimg.src = e.target.result;
            document.getElementById("send_img").value = data;
            cropper.showImage(data);
        }
        reader.readAsDataURL(input.files[0]);
        document.getElementById("myimg").style.display = "none";
    }
}

document.querySelector('#myfile').addEventListener('change', function () {
    readURL()
});