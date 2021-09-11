 $(document).ready(function(){


  $image_crop = $('#image_demo_edit').croppie({

    enableExif: true,

    viewport: {

      width:850,

      height:476,

      type:'square' 

    },

    boundary:{

      width:1000,

      height:600

    }

  });


  $('#get_videos_thumbnail').on('change', function(){

var set_status = true;
    var reader = new FileReader();

    reader.onload = function (event) {
      
        var image = new Image();
         image.src = event.target.result;
         //Validate the File Height and Width.
         image.onload = function () {
           var height = this.height;
           var width = this.width;

            $image_crop.croppie('bind', {

              url: event.target.result
       
              }).then(function(){

                console.log('jQuery bind complete');

              });
              $('#uploadimageModal_edit').modal('show');
          //   if(height >= 476 && width >= 850)
          // {
          //    $image_crop.croppie('bind', {

          //     url: event.target.result
       
          //     }).then(function(){

          //       console.log('jQuery bind complete');

          //     });
          //     $('#uploadimageModal_edit').modal('show');
          // }
          // else
          // {
          //   set_status = false;
          //   swal("The image size is too small to be chosen as thumbnail, Please select a bigger 850*476px image", {
          //   icon: "error",
          // });
          // }
         }

     

    }


  if(set_status)
  {
    reader.readAsDataURL(this.files[0]);

    
  }
    

  });



  $('.crop_image_edit').click(function(event){

$('.crop_image_edit').html('Image Uploading');
$('.crop_image_edit').attr("disabled", true);

    $image_crop.croppie('result', {

      type: 'canvas',

      size: 'viewport'

    }).then(function(response){

$('.crop_image_edit').html('Image Upload');
$('.crop_image_edit').attr("disabled", false);
         $("#set_videos_thumbnail").val(response);
           $("#set_crope_image_data").html('<img style="border: 2px solid; width:100%; height: 95px;"  src="'+response+'">');
        // $("#uploadimageModal_edit #show_crop_image_dsp").html('<div class="product_box"><div class="cat_box"><span class="count_in btn" data-dismiss="modal" >OK</span><img src="'+response+'" style="height: 281px; width: 100%"></div></div>');
          $('#uploadimageModal_edit').modal('hide');

    })

  });



});
