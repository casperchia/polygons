function px_to_num(px_string) {
   return Number(String(px_string).replace(/px$/, ''));
}

function which_transition_event(){
    var t;
    var el = document.createElement('fakeelement');
    var transitions = {
      'transition':'transitionend',
      'OTransition':'oTransitionEnd',
      'MozTransition':'transitionend',
      'WebkitTransition':'webkitTransitionEnd'
    }

    for(t in transitions){
        if( el.style[t] !== undefined ){
            return transitions[t];
        }
    }
}

var can_message_expand = true;

function delete_message() {
   var messages = document.getElementById("messages");
   messages.removeChild(messages.children[0]);
   if (messages.children.length == 0) {
      messages.style.display = "none";
   }
   can_message_expand = true;
}

function hide_message() {
   var message = document.getElementById("messages").children[0];
   var transition_end = which_transition_event();
   message.addEventListener(transition_end, delete_message, false);
   can_message_expand = false;
   message.style.height = "0";
}

function expand_messages() {
   if (can_message_expand) {
      var message_container = document.getElementById("messages").children[0];
      var message = message_container.children[0];
      var message_container_height = px_to_num(window.getComputedStyle(message_container).getPropertyValue('height'));
      if (message_container_height < message.offsetHeight) {
         message_container.style.height = message.offsetHeight + 'px';
      }
   }
}

function contract_messages() {
   if (can_message_expand) {
      var message_container = document.getElementById("messages").children[0];
      message_container.style.height = null;
   }
}

function get_position(element) {
    var x_coor = 0;
    var y_coor = 0;
  
    while(element) {
        x_coor += (element.offsetLeft - element.scrollLeft + element.clientLeft);
        y_coor += (element.offsetTop - element.scrollTop + element.clientTop);
        element = element.offsetParent;
    }

    return { x: x_coor, y: y_coor };
}

var nav_bar_height = 0;

function set_nav_bar_height() {
   nav_bar_height = get_position(nav_bar).y;
}

function position_nav_bar() {
   var nav_bar = document.getElementById('nav_bar');
   var scroll_amount = window.pageYOffset || document.documentElement.scrollTop;

   if (scroll_amount >= nav_bar_height) {
      nav_bar.style.position = 'fixed';
      nav_bar.style.top = '0';
      nav_bar.style.marginLeft = 'auto';
      nav_bar.style.marginRight = 'auto';
      nav_bar.style.width = document.getElementById('mainFrame').clientWidth + 'px';
      nav_bar.style.borderTopStyle = 'none';
   } else {
      nav_bar.style.position = 'static';
      nav_bar.style.top = 'auto';
      nav_bar.style.marginLeft = '0';
      nav_bar.style.marginRight = '0';
      nav_bar.style.width = 'auto';
      nav_bar.style.borderTopStyle = 'solid';
   }
}

window.addEventListener("load", set_nav_bar_height, false);
window.addEventListener("scroll", position_nav_bar, false);
