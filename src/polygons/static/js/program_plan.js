function delete_program_plan(button) {
   var confirmed = confirm('Are you sure you want to permanently delete this plan?');
   if (confirmed) {
      button.form.submit();
   }
}
