// delayed
// closure (for scope)

$(function() {
   // Hide initial Fields
   $('#id_ItemID').closest('p').hide()
   $('#id_MaxRental').closest('p').hide()
   $('#id_RetireDate').closest('p').hide()

   // Hide fields based on product type
   var productChoice = $('#id_Type');
   productChoice.on('change', function() {
      console.log(productChoice.val())
      if (productChoice.val() == 'BulkProduct')
      {
         $('#id_ItemID').closest('p').hide(1000)
         $('#id_MaxRental').closest('p').hide(1000)
         $('#id_RetireDate').closest('p').hide(1000)

         $('#id_Quantity').closest('p').show(1000)
         $('#id_ReorderTrigger').closest('p').show(1000)
         $('#id_ReorderQuantity').closest('p').show(1000)
      }

      else if (productChoice.val() == 'IndividualProduct')
      {
         $('#id_MaxRental').closest('p').hide(1000)
         $('#id_RetireDate').closest('p').hide(1000)
         $('#id_Quantity').closest('p').hide(1000)
         $('#id_ReorderTrigger').closest('p').hide(1000)
         $('#id_ReorderQuantity').closest('p').hide(1000)

         $('#id_ItemID').closest('p').show(1000)
      }

      else if (productChoice.val() == 'RentalProduct')
      {
         $('#id_Quantity').closest('p').hide(1000)
         $('#id_ReorderTrigger').closest('p').hide(1000)
         $('#id_ReorderQuantity').closest('p').hide(1000)

         $('#id_ItemID').closest('p').show(1000)
         $('#id_MaxRental').closest('p').show(1000)
         $('#id_RetireDate').closest('p').show(1000)
      }
   })

}
)
