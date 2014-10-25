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

function populate_dependent_subjects(ajax_url) {
   document.getElementById('loading_animation').style.display = 'block';   

   var ajax = new XMLHttpRequest();
   ajax.onreadystatechange=function()
   {
      if (ajax.readyState==4 && ajax.status==200) {
         var data = JSON.parse(ajax.responseText);
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
         
         document.getElementById('loading_animation').style.display = 'none';
         document.getElementById('remove_course_confirmation').style.display = 'block';
      }
   };
   ajax.open("GET", ajax_url, true);
   ajax.send();
}

function display_remove_course_popup(ajax_url, subject_id) {
   document.getElementById('remove_course_popup_container').style.display = 'block';
   document.body.style.overflowY = 'hidden'; // Disable scrolling
   populate_dependent_subjects(ajax_url);
   center_popup_window();
   document.getElementById('remove_course_popup').style.visibility = 'visible';
   document.getElementById('remove_course_field').value = subject_id;
}
