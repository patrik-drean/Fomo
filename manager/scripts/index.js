(function(context) {

    // utc_epoch comes from index.py
    console.log('Current epoch in UTC is ' + context.utc_epoch);

})(DMP_CONTEXT.get());

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
  window.location.href = "/catalog/search/"+ category_name +
    "/"+ product_name +
    "/" + price +
    "/" + page + '/?format=json';
}
