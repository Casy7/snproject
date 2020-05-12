

function rs(res) {
    cropper.replace(res);
}

function delete_avatar() {
    document.getElementById("default_img").style.display = 'block';
    byId('cropper_div').style.display = 'none';
    clearInputFile(document.getElementById("myfile"));
    del_avatar_button();
    document.getElementsByClassName('img-container')[0].style.height = 'initial';
    // 
}

function save_hike() {
    document.getElementById("del_users").value = users_del;
}



function update_ptc_list() {
    ptc_list = []
    Object.values(document.getElementsByClassName('user_card')).forEach(ptc => {
        ptc_list.push(ptc.id.substring(0, ptc.id.length - 5));
    })
    byId('list-usrs').value = ptc_list;
}


function readURL() {
    var myimg = document.getElementById("myimg");
    var input = document.getElementById("myfile");
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            myimg.src = e.target.result;

            cropper.replace(byId('myimg').src);
        }


        reader.readAsDataURL(input.files[0]);

        // byId('res_img').value = reader['result'];

        create_del_button();


    }
}


function create_del_button() {

    button = document.createElement("button");
    button.type = "button";
    button.className = "form-control";
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
    byId('cropper_div').style.display = 'block';
    byId('myimg').style.display = 'block';
    byId('default_img').style.display = 'none';
    document.getElementsByClassName('img-container')[0].style.height = '500px';

    readURL();
    cropper.destroy();
    cropper.replace(byId('myimg').src);

    del_avatar_button();
    create_del_button();


    // cropper.reset();
});


function add_user() {

    username = byId('select_ptc').value;
    if (byId(username + '_user') == null) {
        add_ptc();
        // update_ptc_list();
    }
}



function del_user(user) {
    byId(user + '_user').parentNode.removeChild(byId(user + '_user'));
    byId(user + '_user').parentNode.removeChild(byId(user + '_user'));
    // Два раза, сначала удаляются только дочерние элементы карточки
    ptc_list = []
    Object.values(document.getElementsByClassName('user_card')).forEach(ptc => {
        ptc_list.push(ptc.id.substring(0, ptc.id.length - 5));
    })
    byId('list-usrs').value = ptc_list;
}

