function px_to_num(px_string) {
   return Number(px_string.replace(/px$/, ''));
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
