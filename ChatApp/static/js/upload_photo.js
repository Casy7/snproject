function readURL() {
    var myimg = document.getElementById("myimg");
    var input = document.getElementById("myfile");
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {

            // console.log("changed");
            myimg.src = e.target.result;
            //paste code here
        }
        create_del_button();
        // document.getElementById("del_photo").style.display = "visible";
        reader.readAsDataURL(input.files[0]);
    }
}


function create_del_button() {

    button = document.createElement("button");
    button.type = "button";
    button.className = "upload-btn";
    button.value = "Удалить";
    button.innerText = "Удалить";
    //button.style.height = "30px";
    //button.style.width = "50px";
    button.onclick = function a() {
        delete_avatar();

    }
    document.getElementById("del_button").appendChild(button);
}


function del_avatar_button() {
    del_div = document.getElementById("del_button");
    while (document.getElementById("del_button").childNodes.length > 0) {

        document.getElementById("del_button").removeChild(document.getElementById("del_button").childNodes[0]);
    }
}


function clearInputFile(f) {
    if (f.value) {
        try {
            f.value = ''; //for IE11, latest Chrome/Firefox/Opera...
        } catch (err) { }
        if (f.value) { //for IE5 ~ IE10
            var form = document.createElement('form'),
                parentNode = f.parentNode, ref = f.nextSibling;
            form.appendChild(f);
            form.reset();
            parentNode.insertBefore(f, ref);
        }
    }
}


document.querySelector('#myfile').addEventListener('change', function () {
    readURL();
    del_avatar_button();
    create_del_button();
});
