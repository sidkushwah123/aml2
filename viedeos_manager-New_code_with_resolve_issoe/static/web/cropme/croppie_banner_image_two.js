 $(document).ready(function(){


  $image_crop = $('#image_demo_edit').croppie({

    enableExif: true,

    viewport: {

      width:1360,

      height:567,

      type:'square' 

    },

    boundary:{

      width:1500,

      height:700

    }

  });


  $('#id_Banner_Image').on('change', function(){

var set_status = true;
    var reader = new FileReader();

    reader.onload = function (event) {
      
        var image = new Image();
         image.src = event.target.result;
         //Validate the File Height and Width.
         image.onload = function () {
           var height = this.height;
           var width = this.width;

            if(height >= 567 && width >= 1360)
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
            alert("Please select image grater that 1360*567px.");
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
         $("#banner_image").val(response);
           $("#show_croped_image").html('<img src="'+response+'">');

          $('#uploadimageModal_edit').modal('hide');

    })

  });



});
