function center_popup_window() {
   // TODO
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
   center_popup_window();
   document.body.style.overflowY = 'hidden'; // Disable scrolling
   populate_dependent_subjects(program_plan_id, subject_id);
   document.getElementById('remove_course_field').value = subject_id;
   document.getElementById('remove_course_popup_container').style.display = 'block';
}
