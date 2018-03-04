$(function(context) {
   return function() {
      var container = $('#catalog_container')
      container.load('/catalog/index.products')

}
}(DMP_CONTEXT.get()))
