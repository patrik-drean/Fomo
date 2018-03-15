$(function(context) {
   return function() {
   var thumbnails = $('.thumbnail_img')
   var main_img = $('#main_img')

   thumbnails.mouseenter(function(event) {

      main_img.attr('src', this.src);
   });

}
}(DMP_CONTEXT.get()))

// function changeFunction() {
//
// }
