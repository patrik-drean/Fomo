var categoryid
var pageid
var totalPageCount

$(function(context) {
   return function() {
      // Load the 'catalog' div with 6 product tiles
      var catalog = $('#catalog')
      categoryid = context.categoryid
      pageid = 1
      totalPageCount = context.totalPageCount
      catalog.load('/catalog/index.products/' + categoryid + '/' + pageid)

}

}(DMP_CONTEXT.get('catalog/index')))

function changeFunction(pageIncrement = 1) {
      // Grab the current page number from div and increment
      var currentPageNumber = parseInt($('#currentPageNumber').text())
      var pageid = currentPageNumber + pageIncrement

      // Load the 'catalog' div with 6 product tiles
      if (pageid > 0 && pageid <= totalPageCount)
      {
         var catalog = $('#catalog')
         catalog.load('/catalog/index.products/' + categoryid + '/' + pageid)
         console.log(pageid)
      }

}
