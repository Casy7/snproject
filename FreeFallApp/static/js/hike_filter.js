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

