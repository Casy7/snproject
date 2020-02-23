// Avoid `console` errors in browsers that lack a console.
// (function() {
//     var method;
//     var noop = function () {};
//     var methods = [
//         'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
//         'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
//         'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
//         'timeStamp', 'trace', 'warn'
//     ];
//     var length = methods.length;
//     var console = (window.console = window.console || {});

//     while (length--) {
//         method = methods[length];

//         // Only stub undefined methods.
//         if (!console[method]) {
//             console[method] = noop;
//         }
//     }
// }());



function rs(res) {
    cropper.replace(res);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
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

        byId('res_img').value = reader['result'];

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
    readURL();

    // $().cropper("reset");
    del_avatar_button();
    create_del_button();

});


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
// function add_day (){
//     // alert(document.getElementsByName("day")[0]);
//     a_new_day = document.getElementsByName("day")[0].cloneNode(false);
//     day = document.createElement("input");
//     //alert("start_day"+i.toString());
//     day.name = "start_day"+i.toString();
//     day.className = "form-control";
//     day.placeholder = "День "+i.toString();

//     row1 = document.createElement("div");
//     row1.className = "col-sm";
//     row2 = document.createElement("div");
//     row2.className = "col-sm";    
//     row3 = document.createElement("div");
//     row3.className = "col-sm";   
//     row_btn = document.createElement("div");
//     row_btn.className = "col-sm-1";


//     start = document.createElement("input");
//     //alert("start_day"+i.toString());
//     start.name = "start_day"+i.toString();
//     start.className = "form-control";

//     end = document.createElement("input");
//     //alert("start_day"+i.toString());
//     end.name = "end_day"+i.toString();
//     end.className = "form-control";

//     btn = document.createElement("input");
//     //alert("start_day"+i.toString());

//     btn.type = "button";
//     btn.value = "+";

//     btn.onclick = function add_a_day(){
//         add_day();
//     };

//     btn.className = "form-control";

//     row1.appendChild(day);
//     row2.appendChild(start);
//     row3.appendChild(end);
//     row_btn.appendChild(btn)

//     a_new_day.appendChild(row1);
//     a_new_day.appendChild(row2);
//     a_new_day.appendChild(row3);
//     a_new_day.appendChild(row_btn);

//     // a_new_day.appendChild(document.createElement("br"));

//     document.getElementById("track").appendChild(a_new_day);
//     document.getElementById("track").appendChild(document.createElement("br"));

//     // a_new_day.childNodes[0].setAttribute("name", "start_day"+i);
//     i+=1;
//     // alert(document.getElementsByName("day"));
//     ;
// }

function del_user(user) {
    $('#' + user).remove();
}

function str_to_list(str_el) {
    str_el = str_el.replace('[', '');
    str_el = str_el.replace(']', '');
    list = str_el.split(", ");
    return list
}
