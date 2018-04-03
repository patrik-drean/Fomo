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

      // <a href="/catalog/index.products/${ category.id }/${ int(pageid) - 1  }"><i class="fas fa-angle-double-left"></i></a>
      // <p class="">Page ${ int(pageid) + 1 } of ${ productCount }</p>
      // <a href="/catalog/index.products/${ category.id }/${ int(pageid) + 1  }"><i class="fas fa-angle-double-right"></i></a>
}
function search() {
  var category_name = $('#category_name').val()
  var product_name = $('#product_name').val()
  var price = $('#price').val()
  var page = $('#page').val()

  if(category_name == '') {
    category_name = 'na'
  }
  if(product_name == '') {
    product_name = 'na'
  }
  if(price == '') {
    price = 999999
  }
  if(page == '') {
    page = 1
  }

  // Redirect to search.py
  window.location.href = "http://localhost:8000/catalog/search/"+ category_name +
    "/"+ product_name +
    "/" + price +
    "/" + page + '/?format=json';

}
