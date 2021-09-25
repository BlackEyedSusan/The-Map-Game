var h1Elements = document.getElementsByTagName("a");
for(var i = 6; i < h1Elements.length; i++) {
   h1Elements[i].style.color = "black";
   console.log('done this tick of the for loop')
}
document.getElementsByName("game_list").style.color = "black"