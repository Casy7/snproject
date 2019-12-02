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

function add_landmark (){
    
}