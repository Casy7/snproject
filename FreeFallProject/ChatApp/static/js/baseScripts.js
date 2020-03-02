// $('#sidebar').toggleClass('active');
// $('#sidebarCollapse').toggleClass('active');

$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
    });
});

document.addEventListener("click", function () {
    // string = byId('notification_menu').className;
    // if (string.indexOf('show')!==-1){
    //     string = string.replace(' show','');
    //     byId('notification_menu').className = string;
    // }
    // byId('notification_menu').toggleClass('show');
    // document.getElementById("demo").innerHTML = "Hello World";
});

if (byId('notification_menu') != undefined) {
    byId('notification_menu').addEventListener("click", function () {
        show_notifications();
    });
}
function show_notifications() {

    string = byId('notification_menu').className;
    if (string.indexOf('show') === -1) {
        string = string.replace(' show', '');
        byId('notification_menu').className = string;
    }
    else {
        string = string + " show";
        byId('notification_menu').className = string;
    }

}

function show_notification(notification) {

}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}