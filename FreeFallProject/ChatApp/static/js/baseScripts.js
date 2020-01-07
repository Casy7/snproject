// $('#sidebar').toggleClass('active');
// $('#sidebarCollapse').toggleClass('active');

$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
    });
});

function byId(id){
    // Сокращение для удобства написания кода
    return document.getElementById(id);
}

function log(value){
    console.log(value);
}