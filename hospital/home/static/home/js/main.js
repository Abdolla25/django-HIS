window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
    document.getElementById("logo").style.maxHeight = "50px";
    document.getElementById("nav-collapse").style.top = "75px";
  } else {
    document.getElementById("logo").style.maxHeight = "100px";
    document.getElementById("nav-collapse").style.top = "125px";
  }
}