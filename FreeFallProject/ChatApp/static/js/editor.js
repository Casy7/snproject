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