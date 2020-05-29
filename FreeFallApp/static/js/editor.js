var x = document.createElement("INPUT");
x.setAttribute("type", "image");
var days = document.getElementsByName("day");
var i = 1;

var image = document.querySelector('#image_to_crop');
var cropper = new Cropper(image, {
    aspectRatio: 16 / 9,
    viewMode: 1,

    minContainerWidth: 300,
    minContainerHeight: 300,

});

document.querySelector('#myfile').addEventListener('change', function () {
    
    show_cropper();
});

async function show_cropper(){
    read_image_URL();
    
    // sleep(2000);

    $('#cropper_photo').modal();
    $('.modal-backdrop').appendTo("#content");
}

byId('cropper_photo').addEventListener('ready', function () {
    // console.log(this.cropper === cropper);
    // > true
  });
  


$(function () {
    $("#join_ptc").mCustomScrollbar({
        theme: "dark-thin"
    });
});
$(function () {
    $("#users_select_col").mCustomScrollbar({
        theme: "dark-thin"
    });
});







// $('#cropper_photo').appendTo("body").modal('show');


function select_user(username) {
    card = byId('join_user_' + username)
    if (card.className.indexOf('selected_user') == -1) {
        $('#join_user_' + username).addClass('selected_user');
    }
    else {
        $('#join_user_' + username).removeClass('selected_user');
    }
    byId('send_invite_button').innerHTML = 'Отправить приглашения (' + document.getElementsByClassName('selected_user').length + ')'
}


function get_cropper_data() {
    $('#result_image_show').remove();
    img_canvas = cropper.getCroppedCanvas({ width: 444, height: 250 });
    img_canvas.id = 'result_image_show';
    jQuery(img_canvas).appendTo($('#place_for_image'));
    byId('is_photo_deleted').value = 'false';
}


function send_croped_photo() {
    delete_photo = (byId('is_photo_deleted').value == 'true')
    if (!delete_photo) {
        var url = cropper.getCroppedCanvas({ width: 800, height: 450 }).toDataURL();
        var blobBin = atob(url.split(',')[1]);
        var array = [];
        for (var i = 0; i < blobBin.length; i++) {
            array.push(blobBin.charCodeAt(i));
        }
        var file = new Blob([new Uint8Array(array)], { type: 'image/png' });


        var formdata = { "myNewFileName": file };
        base64 = url.substr(url.indexOf(',') + 1)
    }

    else{
        base64 = ''
    }
    $.ajax({
        url: "upload_hike_image/",
        type: "POST",
        data: { 'base64img': base64, 'delete_photo': delete_photo },
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
            coordinates = [];

            markers.forEach(function (item, index) {
                var day = item.day;
                var lngLat = item.marker.getLngLat();
                var lng = lngLat.lng;
                var lat = lngLat.lat;
                var id = item.id;

                coordinates.push(id, day, lng, lat);

            });
            debugger;
            document.getElementById("coords").value = coordinates;
            document.getElementById("del_coords").value = cord_del;
            byId('editor_form').submit();
        },
        error: function err(json) {
            alert('Server Error');
        },
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
            cropper.replace(src);
            create_del_button();
            return e.target.result;
        }

        reader.readAsDataURL(input.files[0]);

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
    if (byId('del_button') == undefined) {
        jQuery(`<a type="button" id="del_button" onclick="delete_avatar()"><i class="far fa-trash-alt"></i></a>`).appendTo($('#photo_edit_menu'));
    }
}

function del_avatar_button() {
    for (i = 0; i < 3; i++) {
        byId('#del_button').parentNode.removeChild(byId('del_button'));
    }
}