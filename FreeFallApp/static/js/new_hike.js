

function rs(res) {
    cropper.replace(res);
}

function delete_avatar() {
    document.getElementById("myimg").src = "{% static 'icons/default.jpg' %}";
    clearInputFile(document.getElementById("myfile"));
    del_avatar_button();
    // 
}

function save_hike() {
    document.getElementById("del_users").value = users_del;
}

function add_ptc() {
    str_of_users = byId('list-usrs').value.split(',');
    user = byId('select_ptc').value;

    //СЮДЫТЬ ВСТАВИТЬ AJAX-ЗАПРОС
    $.ajax({
        url: "/does_user_exist/",
        type: 'POST',
        data: { 'username': user },
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        success: function a(json) {
            // alert(json);
            // alert(json.exist);
            if (json.exist === "True") {
                var user_exists = true;
                //alert(list);
                str_of_users = str_of_users + ',' + user;
                document.getElementById('list-usrs').value = str_of_users;
                // alert(document.getElementById('list-usrs').value);

                user_card = document.createElement("li");
                user_card.id = user;
                user_card.className = "card";
                user_card.style = "width:90px; border: .6px solid rgb(221, 221, 221);background-color:#fcfcfc; margin-bottom: 7px;";


                img = document.createElement("img");
                img.className = "card-img-top";
                img.style = "width: 100%;height:90px";
                if (json.exist_image) {
                    data = json.image
                    img.src = 'data:image/gif;base64,' + data;
                }
                else {
                    img.src = "{%static 'icons/logo_grey.png'%}"
                }
                span = document.createElement("span");
                span.style = "text-align:center";
                span.value = user;
                span.text = user;
                span.appendChild(document.createTextNode(user));
                button = document.createElement("button");
                button.className = "form-control";
                button.type = "button";
                button.onclick = function delete_user() {

                    userlist = byId('list-usrs').value.split(',');
                    userlist.splice(userlist.indexOf(user), 1);

                    byId('list-usrs').value = userlist;
                    element = byId(this.parentNode.id);
                    element.parentNode.removeChild(element)
                };
                button.style = "height:40px; border: none;";
                button.innerHTML = "Удалить";

                user_card.appendChild(img);
                user_card.appendChild(span);
                user_card.appendChild(button);

                li = document.createElement("li");
                li.className = "list-inline-item";
                li.name = user;
                li.id = user;

                li.appendChild(user_card);
                document.getElementById('inline-userlist').insertBefore(li, byId("add-user"));

            }
            else {
                var user_exists = false;
            }
        }

    });
}


// function readURL() {
//     var myimg = document.getElementById("myimg");
//     var input = document.getElementById("myfile");
//     if (input.files && input.files[0]) {
//         var reader = new FileReader();
//         reader.onload = function (e) {

//             // console.log("changed");
//             myimg.src = e.target.result;
//             //paste code here
//         }
//         create_del_button();
//         // document.getElementById("del_photo").style.display = "visible";
//         reader.readAsDataURL(input.files[0]);
//     }
// }


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
    users = byId('list-usrs').value;
    if (users.indexOf(byId('select_ptc').value) === -1) {
        add_ptc();
    }
}

function clearInputFile(f){
    if(f.value){
        try{
            f.value = ''; //for IE11, latest Chrome/Firefox/Opera...
        }catch(err){ }
        if(f.value){ //for IE5 ~ IE10
            var form = document.createElement('form'),
                parentNode = f.parentNode, ref = f.nextSibling;
            form.appendChild(f);
            form.reset();
            parentNode.insertBefore(f,ref);
        }
    }
}

function del_user(user) {
    $('#' + user).remove();
}

function str_to_list(str_el) {
    str_el = str_el.replace('[', '');
    str_el = str_el.replace(']', '');
    list = str_el.split(", ");
    return list
}
