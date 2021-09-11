$(document).ready(function(){






$("#submit_video_ditales").on("submit",function(event){
  event.preventDefault();
 $(".se-pre-con").css("display","block");
  $("#show_error_message").text('');
 if($("#video_id_set").val() !="")
{
  
  if($("#set_videos_thumbnail").val() !="")
  {

    $.ajax({
   method:"POST",
   url:$("#video_info_submit_update_form_url").val(),
   data:$('#submit_video_ditales').serializeArray(),
   dataType:"html",
   success:function(data){
      $(".stap_2_tab").addClass('hidden'); 
       $(".stap_2").removeClass('active'); 

       $(".stap_3_tab").attr('class','active'); 
       $(".stap_3").addClass('active');
       $(".se-pre-con").css("display","none");
   }
 });   
  }
  else
  {
    $(".se-pre-con").css("display","none");
    document.getElementById("get_videos_thumbnail").value = null;
    $("#show_error_message").text("crop image is not selected.");
  }
 
 
}
else
{
  alert("Plese upload video first.");
  $(".se-pre-con").css("display","none");
}
 

});


$("#select_category").change(function(){

var get_cate_id = $(this).val();

if(get_cate_id)
  {
     $.ajax({
      method:"POST",
      url:$(this).data("url"),
      data:{"get_cate_id":get_cate_id},
      dataType:"html",
      success:function(data){
        
      if(data=="")
      {
         $("#show_sub_cate").css('display','none');
      }
      else
      {
          $("#show_sub_cate").css('display','block');
      }

      $("#select_sub_category").html(data); 
        
      }
     });
  }
  else
  {
     
  }

});


$("#submit_videos").on("submit",function(event){
	event.preventDefault();

$(".set_status_for_submit_btn").prop("disabled", true);
   var submit_url  = $("#submit_url").val();



const fi = document.getElementById('videos_data_upload'); 


 if (fi.files.length > 0) { 
            for (const i = 0; i <= fi.files.length - 1; i++) { 
  
                const fsize = fi.files.item(i).size; 
                const file = Math.round((fsize / 1024)); 

                if (file > 102400) { 
                     
                    swal("Video file is too Big, please select a video file less than 100MB size.", {
                  icon: "error",
                    });

$(".set_status_for_submit_btn").prop("disabled", false);

                } else { 

                   var formdata = new FormData($("#submit_videos")[0]);
 $('#myModal_upload_videos_progress').modal({
        backdrop: 'static',
        keyboard: false
    });

$("#myModal_upload_videos_progress").modal('show');
 


   $.ajax({
     xhr:function(){
      var xhr = new window.XMLHttpRequest();
      xhr.upload.addEventListener('progress',function(e){
       if(e.lengthComputable)
       {
        console.log('Byte loaded :'+e.loaded);
        console.log('Total_size :'+e.total);
        console.log('Persentage Uploaded :'+(e.loaded/e.total));

        var percentage = Math.round((e.loaded/e.total)*100);
        $("#progressBar").attr('aria-valuenow',percentage).css("width",percentage+"%").text(percentage+"%");
       }  
      });
      return xhr;
     },
     method:"POST",
     url:submit_url,
     data:formdata,
     timeout: 100000000,
     processData:false,
     contentType:false,
     success:function(data)
     {
      console.log(data);
      if(data.status == "0")
      {
        
        $("#myModal_upload_videos_progress").modal('hide');
      $(".set_status_for_submit_btn").prop("disabled", false);

       $("#video_id_set").val(data.video_id);

''

       $(".show_videos_data").html('<video style="width:100%; height:300px;" controls><source src="'+data.videos+'" type="video/mp4"><source src="'+data.videos+'" type="video/ogg">Your browser does not support the video tag.</video>');

       $(".stap_1_tab").removeClass('active'); 
       $(".stap_1").removeClass('active'); 

       $(".stap_2_tab").attr('class','active stap_2_tab'); 
       $(".stap_2").addClass('active'); 
      }
      else
      {

         alert(data.message); 
      }
     

     }
   });

                }
              }
            }




});

});