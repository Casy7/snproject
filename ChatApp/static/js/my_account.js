var list_of_all_ids = []

function add_contact_field (){
    //Создание строки
    row = document.createElement("div");
    row.className = "row";
    row.style = "padding-top:20px;"
    last_id = byId("contacts").lastChild.id;
    ids = byId("contacts").getElementsByClassName("row");
    
    // Выбор ID
    new_id = ids.length;
    while (byId("contact_"+new_id) != null){
        new_id+=1;
    }
    row.id = "contact_"+new_id;
    id = new_id;
    log(row.id);

    // Создание блока контакта
    type_of_contact = document.createElement("div");
    type_of_contact.className="col-sm";
    type_of_contact.id = "contact_name_"+id;
    
    select_type = document.createElement("select");
    select_type.className="form-control";
    select_type.name="contact_name_"+id;
    select_type.style="height: 40px;font-size: 14px;";

    
    opt1 = document.createElement("option");
    opt2 = document.createElement("option");
    opt3 = document.createElement("option");
    opt4 = document.createElement("option");

    list_of_ops = [opt1, opt2, opt3, opt4];
    list_of_values = ["email", "phone", "telegram", "other"]
    list_of_ihtml = ["Email", "Телефон", "Telegram", "Другое"]


    for (i=0;i<list_of_ops.length;i++){
        list_of_ops[i].value = list_of_values[i];
        list_of_ops[i].innerHTML = list_of_ihtml[i];
    }
    opt4.onclick = function(){
        other_contact_type(this.parentNode.parentNode.parentNode.id);
    }

    for (i=0;i<list_of_ops.length;i++){
        select_type.appendChild(list_of_ops[i]);
    }
    type_of_contact.appendChild(select_type);
    row.appendChild(type_of_contact);
    // Создание поля значения контакта
    contact_value_div = document.createElement("div");
    contact_value_div.className = "col-sm";

    contact_value_field = document.createElement("input");
    contact_value_field.type = "text";
    contact_value_field.name = "contact_value_"+id;
    contact_value_field.className = "form-control";
    contact_value_field.id = "contact_value_"+id;
    contact_value_field.style = "height: 40px;font-size: 14px;";

    contact_value_div.appendChild(contact_value_field);

    row.appendChild(contact_value_div);
    
    // Создание блока выбора видимости
    visible_for_div = document.createElement("div");
    visible_for_div.className="col-sm";
    visible_for_div.id = "contact_visibility_"+id;
    
    select_visibility = document.createElement("select");
    select_visibility.className="form-control";
    select_visibility.name="contact_visibility_"+id;
    select_visibility.style="height: 40px;font-size: 14px;";

    
    opt1 = document.createElement("option");
    opt2 = document.createElement("option");
    opt3 = document.createElement("option");

    list_of_ops = [opt1, opt2, opt3];
    list_of_values = ["noone", "friends", "all"]
    list_of_ihtml = ["Виден только мне", "Виден друзьям", "Виден всем"]


    for (i=0;i<list_of_ops.length;i++){
        list_of_ops[i].value = list_of_values[i];
        list_of_ops[i].innerHTML = list_of_ihtml[i];
    }
    opt4.onclick = function(){
        other_contact_type(this.parentNode.parentNode.parentNode.id);
    }

    for (i=0;i<list_of_ops.length;i++){
        select_visibility.appendChild(list_of_ops[i]);
    }
    visible_for_div.appendChild(select_visibility);
    row.appendChild(visible_for_div);

    // Создание кнопки "убрать блок"

    del_button_div = document.createElement("div");
    del_button_div.className="col-sm-1";
    
    button = document.createElement("button");
    button.className = "form-control";
    button.style="height: 40px;font-size: 14px;";
    list_of_all_ids.push(id)
    button.onclick = function(){
        del_contact_field(this.parentNode.parentNode.id);
    }
    button.innerHTML = "-"

    del_button_div.appendChild(button);
    row.appendChild(del_button_div);
    
    // Добавление строки
    //byId("contacts").appendChild(document.createElement("br"));
    byId("contacts").appendChild(row);

}





function del_contact_field(id)
{
    byId(id).parentNode.removeChild(byId(id));
}


function other_contact_type(contact_id)
{
    //log(contact_id);
    number = contact_id.replace( /^\D+/g, '');
    log(number);
    contact_name_field = document.createElement("input");
    contact_name_field.type = "text";
    contact_name_field.name = "contact_name_"+number;
    contact_name_field.className = "form-control";
    contact_name_field.placeholder = "Тип контакта";
    contact_name_field.style = "height: 40px;font-size: 14px;";
    nameId = "contact_name_"+number;
    while (byId(nameId).childNodes.length > 0) {
        byId(nameId).removeChild(byId(nameId).childNodes[0]);
    }
    byId("contact_name_"+number).appendChild(contact_name_field);
}
