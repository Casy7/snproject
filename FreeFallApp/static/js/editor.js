var x = document.createElement("INPUT");
x.setAttribute("type", "image");
var days = document.getElementsByName("day");
var i = 1;

var image = document.querySelector('#image_to_crop');
var cropper = new Cropper(image, {
    aspectRatio: 16 / 9,
    viewMode: 1,

    minContainerWidth: 500,
    minContainerHeight: 500,
    // ready: function () {

    // },

    // crop: function (event) {

    // },
});

document.querySelector('#myfile').addEventListener('change', function () {

    $('#cropper_photo').modal();
    read_image_URL();

});


function get_cropper_data() {
    $('#result_image_show').remove();
    img_canvas = cropper.getCroppedCanvas({ width: 480, height: 270 });
    img_canvas.id = 'result_image_show';
    jQuery(img_canvas).appendTo($('#place_for_image'));
    
    var url = img_canvas.toDataURL();
    var blobBin = atob(url.split(',')[1]);
    var array = [];
    for (var i = 0; i < blobBin.length; i++) {
        array.push(blobBin.charCodeAt(i));
    }
    var file = new Blob([new Uint8Array(array)], { type: 'image/png' });


    var formdata = {"myNewFileName": file};
    base64 = url.substr(url.indexOf(',')+1)
    // base64 = url;
    $.ajax({
        url: "upload_hike_image/",
        type: "POST",
        data: {'base64img':base64},
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

            

            
        }
    });

}


function each(arr, callback) {
    var length = arr.length;
    var i;

    for (i = 0; i < length; i++) {
        callback.call(arr, arr[i], i, arr);
    }

    return arr;
}


function read_image_URL() {
    var myimg = document.getElementById("image_to_crop");
    var input = document.getElementById("myfile");
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            src = e.target.result;
            byId('test_rs').src = src;

            myimg.src = src;
            cropper.replace(src);
            return e.target.result;
        }


        reader.readAsDataURL(input.files[0]);
        create_del_button();


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


function del_pot_user(username, user_id) {
    hike_id = byId('hike_id').value;
    byId('user_' + username).parentNode.removeChild(byId('user_' + username));
    send_data = {}
    send_data['code'] = user_id.toString() + '-' + hike_id.toString() + '-' + 'invite_to_hike';
    send_data['result'] = 'delete';
    console.log(send_data);


    $.ajax({
        url: "/send_notification_choice/",
        type: 'POST',
        data: send_data,
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
            if (json.exist === "True") {
                var user_exists = true;
                str_of_users = str_of_users + ',' + user;
                //alert(list);
                document.getElementById('list-usrs').value = str_of_users;
                // alert(document.getElementById('list-usrs').value);

                user_card = document.createElement("li");
                user_card.className = "card";
                if (user_exists) {
                    user_card.style = "width:70px; border: .6px solid rgb(221, 221, 221);background-color:#fcfcfc";
                }
                else {
                    user_card.style = "width:70px; border: .6px solid rgb(221, 221, 221);background-color:#fffffc";
                }
                img = document.createElement("img");
                img.className = "card-img-top";
                img.style = "width: 100%;height:70px";
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
                button.onclick = function add_this_user() { del_user(user) };
                button.style = "height:20px; border: none;";
                button.innerHTML = "-";

                user_card.appendChild(img);
                user_card.appendChild(span);
                user_card.appendChild(button);

                li = document.createElement("li");
                li.className = "list-inline-item";
                li.name = user;
                li.id = user;

                li.appendChild(user_card);
                document.getElementById('inline-userlist').insertBefore(li, document.getElementById("add-user"));


            }
            else {
                var user_exists = false;
            }
        }

    });


}


function add_new_day() {
    new_option = document.createElement('option');
    id = byId('day').childNodes.length - 1
    new_option.id = 'day' + id;
    new_option.value = id;
    new_option.innerHTML = id;
    byId('day').appendChild(new_option);
    new_option.selected = 'selected'

    day_card = document.createElement('div');
    day_card.className = "day_card";
    day_card.id = "day_" + id + "_card";

    day_header = document.createElement('h3');
    day_header.innerHTML = "День " + id;

    day_name_label = document.createElement('label');
    day_name_label.innerHTML = "Заголовок дня";

    day_input_name = document.createElement('input');
    day_input_name.type = 'text';
    day_input_name.className = "form-control";
    day_input_name.name = "day_" + id + "_name";
    day_input_name.placeholder = "Заголовок дня";

    day_desc_label = document.createElement('label');
    day_desc_label.innerHTML = "Описание дня";

    day_desc = document.createElement('textarea');
    day_desc.className = "form-control";
    day_desc.name = "day_" + id + "_description";
    day_desc.placeholder = "Описание дня";
    day_desc.style = "font-size: 13px;";


    day_card.appendChild(day_header);
    day_card.appendChild(day_name_label);
    day_card.appendChild(day_input_name);
    day_card.appendChild(day_desc_label);
    day_card.appendChild(day_desc);

    byId('days_list').appendChild(day_card);



}


function del_lmk() {
    id = byId('lmk_id').innerHTML;
    $.ajax({
        url: "/change_map/",
        type: 'POST',
        data: { 'lmk_id': id, 'operation': 'delete_landmark' },
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
            if (json.result === "success") {
                osm_map.setLayoutProperty('lk_' + id, 'visibility', 'none');
                // alert('deleted');
                byId('del_lmk').style.display = 'none';

            }
        }

    });
}


function add_lmk(id, name, desc, coords) {
    id = byId('lmk_id').innerHTML;

    $.ajax({
        url: "/change_map/",
        type: 'POST',
        data: { 'lmk_id': id, 'lmk_name': name, 'lmk_desc': desc, 'lat': coords[0], 'lon': coords[1], 'operation': 'add_landmark' },
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
            if (json.result === "success") {
                osm_map.setLayoutProperty('lk_' + id, 'visibility', 'none');
                // alert('created');


            }
        }

    });
}


function create_del_button() {
    jQuery(`<a type="button" id="del_button" onclick="delete_avatar()"><i class="far fa-trash-alt"></i></a>`).appendTo($('#photo_edit_menu'));
}

function del_avatar_button() {
    $('#del_button').remove();
}