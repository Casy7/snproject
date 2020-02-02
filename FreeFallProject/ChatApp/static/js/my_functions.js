function byId(id){
    // Сокращение для удобства написания кода
    return document.getElementById(id);
}

function log(value){
    console.log(value);
}

Date.prototype.toDateInputValue = (function () {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0, 10);
});
function addDays(date, days) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

function setMinEndDate(){
    byId('end_day').min = byId('start_day').value;
}