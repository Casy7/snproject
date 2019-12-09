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

function add_day (){
    alert(document.getElementsByName("day")[0]);
    a_new_day = document.getElementsByName("day")[0].cloneNode(true);
    alert(document.getElementsByName("day"));
    document.getElementById("track").appendChild(a_new_day);
}