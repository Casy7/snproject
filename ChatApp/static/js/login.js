
function show_password() {
    type_of_input = document.getElementsByClassName("form-control")[1].type
    if (type_of_input == 'password') {
        document.getElementsByClassName("form-control")[1].type = "text";
    }
    else {
        document.getElementsByClassName("form-control")[1].type = "password";
    }
}