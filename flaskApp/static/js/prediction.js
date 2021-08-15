$('#classifyForm').submit(function(e){
    e.preventDefault();
    $.ajax({
      url: '/api/classify',
      type: 'post',
      data:$('#classifyForm').serialize(),
      success:function(){
        alert("Classification has been corrected!");
      }
    });
  });

$('#approveButton').click(function(e){
    e.preventDefault();
    var labels = $(this).attr('value');
    $.ajax({
        url: '/api/classify',
        type: 'post',
        data: '&approvedLabels=' + labels,
        success:function(){
        alert("Classification has been approved!");
        }
    });
});

$("input:checkbox").click(function() {
  var bol = $("input:checkbox:checked").length >= 3;     
  $("input:checkbox").not(":checked").attr("disabled",bol);
  });