// delayed
// closure (for scope)

$(function() {
   var productChoice = $('#id_Type');
   productChoice.on('change', function() {
      console.log(productChoice.val())
      $('#id_Quantity').closest('p').hide(1000)
   })

}
)
