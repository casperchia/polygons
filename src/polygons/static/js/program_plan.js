function document_height() {
   var result = Math.min(
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
   var popup_height = px_to_num(popup.clientHeight);
   var total_height = document_height();

   popup.style.marginTop = (total_height - popup_height) / 2 + 'px';
}

function populate_dependent_subjects(sjax_url) {
   var sjax = new XMLHttpRequest();
   sjax.onreadystatechange=function()
   {
      if (sjax.readyState==4 && sjax.status==200) {
         var data = JSON.parse(sjax.responseText);
         var subject_list = document.getElementById('dependent_subjects');
         
         var num_subjects = data.subjects.length;
         if (num_subjects > 0) {
            subject_list.style.display = 'block';

            for (var i = 0; i < num_subjects; i++) {
               var subject_item = document.createElement("li");
               subject_item.appendChild(document.createTextNode(data.subjects[i]));
               subject_list.appendChild(subject_item);
            }
         }
      }
   };
   sjax.open("GET", sjax_url, false);
   sjax.send();
}

function display_remove_course_popup(sjax_url, subject_id) {
   document.body.style.overflowY = 'hidden'; // Disable scrolling
   document.getElementById('remove_course_popup_container').style.display = 'block';
   center_popup_window();
   populate_dependent_subjects(sjax_url);
   document.getElementById('remove_course_field').value = subject_id;
}
