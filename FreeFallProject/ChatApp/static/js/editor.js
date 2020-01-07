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

function del_user(user) {
    $('#' + user).remove();
}

function str_to_list(str_el) {
    str_el = str_el.replace('[', '');
    str_el = str_el.replace(']', '');
    list = str_el.split(", ");
    return list
}
