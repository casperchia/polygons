function document_height() {
   var result = Math.max(
      document.documentElement.clientHeight,
      document.body.scrollHeight,
      document.documentElement.scrollHeight,
      document.body.offsetHeight,
      document.documentElement.offsetHeight
   );
   return px_to_num(result);
}

function center_popup_window() {
   var popup = document.getElementById('remove_course_popup');
   var popup_height = popup.currentStyle ? popup.currentStyle.height :
                                           getComputedValue(popup, null).height;
   popup_height = px_to_num(popup_height);
   var total_height = document_height();

   popup.style.marginTop = (total_height - popup_height) / 2 + 'px';
}

function populate_dependent_subjects(program_plan_id, subject_id) {
   // TODO
   /*
      * Make AJAX call to get list of dependent subjects
      * If list is not empty, unhide the dependent_subjects div
      * if the list is not empty, insert <li> into the dependent_subjects list
   */
}

function display_remove_course_popup(program_plan_id, subject_id) {
   document.body.style.overflowY = 'hidden'; // Disable scrolling
   center_popup_window();
   populate_dependent_subjects(program_plan_id, subject_id);
   document.getElementById('remove_course_field').value = subject_id;
   document.getElementById('remove_course_popup_container').style.display = 'block';
}
