$(function () {

    /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
    $("#id_file").change(function () {
      if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
          $("#target").attr("src", e.target.result);
          //$("#modalCrop").modal("show");
        }
        reader.readAsDataURL(this.files[0]);
      }
    });
});
