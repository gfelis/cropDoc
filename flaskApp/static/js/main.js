$('#captureForm').submit(function(e){
  e.preventDefault();
  $.ajax({
    url: '/api/take_photo',
    type: 'post',
    data:$('#captureForm').serialize(),
    success:function(){
      alert("worked");
    }
  });
});

document.getElementById("captureForm").onsubmit = function () {
  window.location.href = "/predict";
};