function change_fields(productChoice, time = 0) {
   if (productChoice == 'BulkProduct')
   {
      $('#id_ItemID').closest('p').hide(time);
      $('#id_MaxRental').closest('p').hide(time);
      $('#id_RetireDate').closest('p').hide(time);

      $('#id_Quantity').closest('p').show(time);
      $('#id_ReorderTrigger').closest('p').show(time);
      $('#id_ReorderQuantity').closest('p').show(time);
   }

   else if (productChoice == 'IndividualProduct')
   {
      $('#id_MaxRental').closest('p').hide(time);
      $('#id_RetireDate').closest('p').hide(time);
      $('#id_Quantity').closest('p').hide(time);
      $('#id_ReorderTrigger').closest('p').hide(time);
      $('#id_ReorderQuantity').closest('p').hide(time);

      $('#id_ItemID').closest('p').show(time);
   }

   else if (productChoice == 'RentalProduct')
   {
      $('#id_Quantity').closest('p').hide(time);
      $('#id_ReorderTrigger').closest('p').hide(time);
      $('#id_ReorderQuantity').closest('p').hide(time);

      $('#id_ItemID').closest('p').show(time);
      $('#id_MaxRental').closest('p').show(time);
      $('#id_RetireDate').closest('p').show(time);
   }
   else
   {
      $('#id_ItemID').closest('p').hide(time);
      $('#id_MaxRental').closest('p').hide(time);
      $('#id_RetireDate').closest('p').hide(time);

   }
}

// delayed
// closure (for scope)
$(function() {

   // Hide initial Fields
   var productChoice= $('#id_Type');
   change_fields(productChoice.val())


   // Hide fields based on product type
   productChoice.on('change', function() {
      change_fields(productChoice.val(), 800)
   })

}
)
