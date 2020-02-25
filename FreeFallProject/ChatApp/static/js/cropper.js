// import Cropper from 'cropperjs'

const image = document.getElementById('myimg');
const cropper = new Cropper(image, {
    aspectRatio: 16 / 9,
    viewMode: 1,
    crop(event) {
        document.getElementById('resize_photo').value = event.detail.x + ' ' + event.detail.y + ' ' + event.detail.width + ' ' + event.detail.height;


        // console.log(event.detail.x);
        // console.log(event.detail.y);
        // console.log(event.detail.width);
        // console.log(event.detail.height);
        // console.log(event.detail.rotate);
        // console.log(event.detail.scaleX);
        // console.log(event.detail.scaleY);
    },
    cropend(event) {
        // document.getElementById('cropped_img').value = cropper.getCroppedCanvas().toDataURL();
        document.getElementById('crimage').value = cropper.getCroppedCanvas().toDataURL();
    }

});