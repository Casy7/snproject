function readURL() {
    var myimg = document.getElementById("myimg");
    var input = document.getElementById("myfile");
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            console.log("changed");
            myimg.src = e.target.result;
            //paste code here
        }
        reader.readAsDataURL(input.files[0]);
    }
}

document.querySelector('#myfile').addEventListener('change', function () {
    readURL()
});