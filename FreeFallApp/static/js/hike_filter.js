function validate_max_category() {

    lt = ['I', 'II', 'III', 'IV', 'V', 'VI'];
    var min_selector = byId("min_category");
    var min = min_selector.options[min_selector.selectedIndex].value;
    var max_selector = byId("max_category");
    var max = max_selector.options[max_selector.selectedIndex].value;

    if (lt.indexOf(min) > lt.indexOf(max)) {
        max_selector.value = min;
    }
}

function validate_min_category() {

    lt = ['I', 'II', 'III', 'IV', 'V', 'VI'];
    var min_selector = byId("min_category");
    var min = min_selector.options[min_selector.selectedIndex].value;
    var max_selector = byId("max_category");
    var max = max_selector.options[max_selector.selectedIndex].value;

    if (lt.indexOf(min) > lt.indexOf(max)) {
        min_selector.value = max;
    }
}

function find_all() {
    alert('Подгрузка походов');

    send_data = {};
    send_data['name'] = $('hike_name').value;
    send_data['name'] = $('hike_name').value;

    $.ajax({
        url: "/send_notification_choice/",
        type: 'POST',
        data: send_data,
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        success: function a(json) {
            if (json.exist === "True") {

            } else {
                var user_exists = false;
            }
        }

    });
}