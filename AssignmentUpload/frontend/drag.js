$(function() {
    $("#submit").click(function() {
      $.ajax({
            url: 'http://127.0.0.1:5000/uploader',
            data: $('#upload'),
            type: 'POST',
            success: function(data) {
                document.getElementById("error-register").innerHTML="Account Successfully Created!";
                //document.getElementById("error-register").style.color="blue";
            },
            error: function(data) {
              document.getElementById("error-register").innerHTML=data.responseText;
              //document.getElementById("error-register").style.color="red";
            }
        });
        return false;
    });
});
$(document).ready(function(){
  $('form input').change(function () {
    $('form p').text(this.files.length + " file(s) selected");
  });
});