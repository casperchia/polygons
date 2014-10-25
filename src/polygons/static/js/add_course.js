var filter_form_height = '0px';

function toggle_filter_display() {
   window.scrollTo(0, 0);   
   var filter_form = document.getElementById('filter_form');
   var height = filter_form.currentStyle ? filter_form.currentStyle.height :
                                           getComputedStyle(filter_form, null).height;
   if (height == '0px') {
      filter_form.style.height = filter_form_height + 'px';
   } else {
      filter_form.style.overflow = 'hidden';
      filter_form.style.height = '0';
   }
}

function capture_filter_height() {
   var filter_form = document.getElementById('filter_form');
   filter_form_height = filter_form.clientHeight;
   filter_form.style.height = '0';
   filter_form.style.position = 'static';
   filter_form.style.visibility = 'visible';
   filter_form.style.overflow = 'hidden';
   filter_form.className += ' filter_form_transition';
}

window.addEventListener("load", capture_filter_height, false);
