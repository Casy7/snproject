var x = document.createElement("INPUT");
x.setAttribute("type", "image");
var days = document.getElementsByName("day");
var i = 1;

function del_user(user) {
    $('#' + user).remove();
}

function str_to_list(str_el) {
    str_el = str_el.replace('[', '');
    str_el = str_el.replace(']', '');
    list = str_el.split(", ");
    return list
}


function del_pot_user(username, user_id){
    hike_id = byId('hike_id').value;
    byId('user_'+username).parentNode.removeChild(byId('user_'+username));
    send_data = {}
    send_data['code'] = user_id.toString()+'-'+hike_id.toString()+'-'+'invite_to_hike';
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
                str_of_users = str_of_users+','+user;
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


function add_new_day(){
    new_option = document.createElement('option');
    id = byId('day').childNodes.length-1
    new_option.id = 'day'+id;
    new_option.value = id;
    new_option.innerHTML = id;
    byId('day').appendChild(new_option);
    new_option.selected = 'selected'

    day_card = document.createElement('div');
    day_card.className = "day_card";
    day_card.id = "day_"+id+"_card";

    day_header = document.createElement('h3');
    day_header.innerHTML = "День "+id;

    day_name_label = document.createElement('label');
    day_name_label.innerHTML = "Заголовок дня";

    day_input_name = document.createElement('input');
    day_input_name.type = 'text';
    day_input_name.className = "form-control";
    day_input_name.name = "day_"+id+"_name";
    day_input_name.placeholder = "Заголовок дня";

    day_desc_label = document.createElement('label');
    day_desc_label.innerHTML = "Описание дня";

    day_desc = document.createElement('textarea');
    day_desc.className = "form-control";
    day_desc.name = "day_"+id+"_description";
    day_desc.placeholder = "Описание дня";
    day_desc.style = "font-size: 13px;";

    
    day_card.appendChild(day_header);
    day_card.appendChild(day_name_label);
    day_card.appendChild(day_input_name);
    day_card.appendChild(day_desc_label);
    day_card.appendChild(day_desc);








    byId('days_list').appendChild(day_card);



    // day_card = document.createElement('div');
    // day_card.className = "day_card";
    // day_card.id = "day_"+id+"_card";

    // day_card = document.createElement('div');
    // day_card.className = "day_card";
    // day_card.id = "day_"+id+"_card";

}

function del_lmk(){
    id = byId('lmk_id').innerHTML;
    $.ajax({
        url: "/change_map/",
        type: 'POST',
        data: { 'lmk_id': id, 'opreation': 'delete_landmark'},
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
                alert('deleted');


            }
        }

    });
}