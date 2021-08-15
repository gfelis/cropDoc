$('#captureForm').submit(function(e){
  e.preventDefault();
  $.ajax({
    url: '/api/take_photo',
    type: 'post',
    data:$('#captureForm').serialize(),
    success:function(){
      alert("Photo taken, close this tab to visualize the results...");
    }
  });
});

$('#playDemoButton').click(function(e){
  e.preventDefault();
  var action = $(this).attr('value');
  $.ajax({
      url: '/api/demo',
      type: 'post',
      data: '&do=' + action,
      success:function(){
      alert("Playing demo on Liquid Galaxy...");
      }
  });
});

document.getElementById("captureForm").onsubmit = function () {
  window.location.href = "/predict";
};