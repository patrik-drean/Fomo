$(function(context) {
   return function() {
      var catalog = $('#catalog')
      catalog.load('/catalog/index.products/')
      console.log(context)

}
}(DMP_CONTEXT.get()))
