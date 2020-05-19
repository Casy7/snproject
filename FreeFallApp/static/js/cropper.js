

    const image = document.getElementById('image_to_crop');
    const cropper = new Cropper(image, {
        aspectRatio: 16 / 9,
        viewMode: 1,
        crop(event) {
            document.getElementById('resize_photo').value = event.detail.x + ' ' + event.detail.y + ' ' + event.detail.width + ' ' + event.detail.height;
            console.log(event.detail.x + ' ' + event.detail.y + ' ' + event.detail.width + ' ' + event.detail.height);


        },
        cropend(event) {
            console.log(event);

        }

    });
