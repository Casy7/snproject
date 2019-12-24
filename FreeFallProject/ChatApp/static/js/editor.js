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
}
function del_user(user) {
    $('#' + user).remove();
}
function add_ptc() {
    list = str_to_list(document.getElementById('list-usrs').value);
    //alert(typeof(list));
    //alert(list);
    user = document.getElementById('new-user').value;
    //alert(user);
    list.push(user);
    //alert(list);
    document.getElementById('list-usrs').value = list;
    // alert(document.getElementById('list-usrs').value);

    user_card = document.createElement("li");
    user_card.className = "card";
    user_card.style = "width:70px; border: .6px solid rgb(221, 221, 221);";

    img = document.createElement("img");
    img.className = "card-img-top";
    img.style = "width: 100%;";
    img.src = "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fdragene.no%2Fwp-content%2Fuploads%2F2016%2F06%2Fdefault1.jpg&f=1&nofb=1"

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


    //document.getElementById('inline-userlist').appendChild(li);

}
function str_to_list(str_el) {
    str_el = str_el.replace('[', '');
    str_el = str_el.replace(']', '');
    list = str_el.split(", ");
    return list
}
// function send_landmark() {
//   var name = document.getElementById('landmark_name').value.toString();
//   var desc = document.getElementById('landmark_desc').value.toString();
//   alert("work: "+name+desc);
//   $.ajax({
//     url: "add_landmark/",
//     type: 'POST',
//     data: { 
//       'name': name,
//       'desc': desc
    
//     },
//     success: function (json) {
//       // if (json.result) {
//       //   // $('#notify_icon').addClass("notification");
//       //   // var doc = $.parseHTML(json.notifications_list);
//       //   // $('#notifications-list').html(doc);
//       // }
//       console.log("succes");
//     },
//     error: function(){
//       alert("ERROR!ERROR!")
//     }
//   });
// };
// <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>