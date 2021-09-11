 $(document).ready(function(){


  $image_crop = $('#image_demo_edit').croppie({

    enableExif: true,

    viewport: {

      width:508,

      height:318,

      type:'square' 

    },

    boundary:{

      width:600,

      height:400

    }

  });


  $('#id_Grape_Image').on('change', function(){

var set_status = true;
    var reader = new FileReader();

    reader.onload = function (event) {
      
        var image = new Image();
         image.src = event.target.result;
         //Validate the File Height and Width.
         image.onload = function () {
           var height = this.height;
           var width = this.width;

            if(height >= 318 && width >= 508)
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
            alert("Please select image grater that 508*318px");
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
         $("#Grape_Image").val(response);
           $("#show_croped_image").html('<img src="'+response+'">');

          $('#uploadimageModal_edit').modal('hide');

    })

  });



});
