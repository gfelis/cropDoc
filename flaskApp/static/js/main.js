// Tabbed Menu
function openMenu(evt, action) {
    var i, x, tablinks;
    x = document.getElementsByClassName("action");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" w3-dark-grey", "");
    }
    document.getElementById(action).style.display = "block";
    evt.currentTarget.firstElementChild.className += " w3-dark-grey";
  }

function submitClick(event){
  event.preventDefault();
  var form = document.getElementById("captureForm");
  if (document.getElementsByName("photo_name")[0].value){
    form.submit();
    return false;
  }
}
/*
function checkFileExist(urlToFile) {
    var xhr = new XMLHttpRequest();
    xhr.open('HEAD', urlToFile, false);
    console.log(xhr.value)
    xhr.send();
     
    if (xhr.status == "404") {
        return false;
    } else {
        return true;
    }
}

var photo_name = document.getElementsByName("photo_name")[0].value
if (photo_name){
  console.log(photo_name.value)
  if(checkFileExist("file://home/gfelis/GSOC/shots/" + photo_name + ".png")){
    // Get the modal
    var modal = document.getElementById("myModal");
    
    // Get the button that opens the modal
    var btn = document.getElementById("captureButton");
    
    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];
    
    // When the user clicks the button, open the modal 
    btn.onclick = function() {
      if (validateForm() == true){
        modal.style.display = "block";
      }
    }
    
    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    }
    
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
  }
}  

  
}
*/