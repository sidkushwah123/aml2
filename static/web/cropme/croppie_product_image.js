 $(document).ready(function(){


  $image_crop = $('#image_demo_edit').croppie({

    enableExif: true,

    viewport: {

      width:253,

      height:328,

      type:'square' 

    },

    boundary:{

      width:350,

      height:450

    }

  });


  $('#add_product_image').on('change', function(){

var set_status = true;
    var reader = new FileReader();

    reader.onload = function (event) {
      
        var image = new Image();
         image.src = event.target.result;
         //Validate the File Height and Width.
         image.onload = function () {
           var height = this.height;
           var width = this.width;

            if(height >= 328 && width >= 253)
          {
             $image_crop.croppie('bind', {

              url: event.target.result
       
              }).then(function(){

                console.log('jQuery bind complete');

              });
              $('#uploadimageModal_edit').modal('show');
          }
          else
          {
            set_status = false;
            alert("Please select image grater that 253*328px");
          }
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

           $("#show_images").append('<div class="col-md-2 remove_this_div"><div class="form-group"><div class="three3d"><div class="delectimg"><span><i class="icon-close2 remove_div"></i></span><input type="hidden" name="product_images[]" value="'+response+'"><img src="'+response+'"></div></div></div></div>');

          $('#uploadimageModal_edit').modal('hide');

    })

  });


// ===============================CODE START FOR BANNER ================

  $image_crop_banner = $('#image_demo_edit_banner').croppie({

    enableExif: true,

    viewport: {

      width:500,

      height:300,

      type:'square' 

    },

    boundary:{

      width:600,

      height:400

    }

  });



  $('#add_product_banner').on('change', function(){

var set_status = true;
    var reader = new FileReader();

    reader.onload = function (event) {
      
        var image = new Image();
         image.src = event.target.result;
         //Validate the File Height and Width.
         image.onload = function () {
           var height = this.height;
           var width = this.width;

            if(height >= 300 && width >= 500)
          {
             $image_crop_banner.croppie('bind', {

              url: event.target.result
       
              }).then(function(){

                console.log('jQuery bind complete');

              });
              $('#uploadimageModal_edit_banner').modal('show');
          }
          else
          {
            set_status = false;
            alert("Please select image grater that 500*300px");
          }
         }

     

    }


  if(set_status)
  {
    reader.readAsDataURL(this.files[0]);

    
  }
    

  });


 $('.crop_image_edit_banner').click(function(event){

$('.crop_image_edit_banner').html('Image Uploading');
$('.crop_image_edit_banner').attr("disabled", true);

    $image_crop_banner.croppie('result', {

      type: 'canvas',

      size: 'viewport'

    }).then(function(response){

$('.crop_image_edit_banner').html('Image Upload');
$('.crop_image_edit_banner').attr("disabled", false);
 
           $("#product_banner_image").val(response);
           $("#show_images_banner").html('<img src="'+response+'">');
          $('#uploadimageModal_edit_banner').modal('hide');

    })

  });


// ===============================CODE END FOR BANNER ================


});
