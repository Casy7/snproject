ClassicEditor
    .create(document.querySelector('#editor'))
    .then(editor => {
        console.log(editor);
    })
    .catch(error => {
        console.error(error);
    });

var x = document.createElement("INPUT");
x.setAttribute("type", "image");
var days = document.getElementsByName("day");
var i = 1;
function add_day() {
    // alert(document.getElementsByName("day")[0]);
    a_new_day = document.getElementsByName("day")[0].cloneNode(false);
    day = document.createElement("input");
    //alert("start_day"+i.toString());
    day.name = "start_day" + i.toString();
    day.className = "form-control";
    day.placeholder = "День " + i.toString();

    row1 = document.createElement("div");
    row1.className = "col-sm";
    row2 = document.createElement("div");
    row2.className = "col-sm";
    row3 = document.createElement("div");
    row3.className = "col-sm";
    row_btn = document.createElement("div");
    row_btn.className = "col-sm-1";


    start = document.createElement("input");
    //alert("start_day"+i.toString());
    start.name = "start_day" + i.toString();
    start.className = "form-control";

    end = document.createElement("input");
    //alert("start_day"+i.toString());
    end.name = "end_day" + i.toString();
    end.className = "form-control";

    btn = document.createElement("input");
    //alert("start_day"+i.toString());

    btn.type = "button";
    btn.value = "+";

    btn.onclick = function add_a_day() {
        add_day();
    };

    btn.className = "form-control";

    row1.appendChild(day);
    row2.appendChild(start);
    row3.appendChild(end);
    row_btn.appendChild(btn)

    a_new_day.appendChild(row1);
    a_new_day.appendChild(row2);
    a_new_day.appendChild(row3);
    a_new_day.appendChild(row_btn);

    // a_new_day.appendChild(document.createElement("br"));

    document.getElementById("track").appendChild(a_new_day);
    document.getElementById("track").appendChild(document.createElement("br"));

    // a_new_day.childNodes[0].setAttribute("name", "start_day"+i);
    i += 1;
    // alert(document.getElementsByName("day"));
    ;
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
