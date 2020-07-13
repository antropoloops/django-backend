/**
 *   Common JS scripts
 */

/**
 *  toggle
 *  shows/hide an element pointed by a data-toggle attribute in the
 *  trigger element
 */

function wb_toggle(trigger)
{
  document.querySelectorAll(trigger.dataset.toggle).forEach(function(t){
      if(t.classList.contains('collapsed'))
          t.classList.remove('collapsed');
      else
          t.classList.add('collapsed');
  });
  if('inactivate' in trigger.dataset)
      document.querySelectorAll(trigger.dataset.inactivate).forEach(function(t){
          t.classList.remove('active')
      });
  trigger.classList.add('active');
}

/**
 *  show
 *  shows an element pointed by a data-toggle attribute in the
 *  trigger element
 */
function wb_show(trigger)
{
  document.querySelectorAll(trigger.dataset.show).forEach(function(t){
      if(t.classList.contains('collapsed'))
          t.classList.remove('collapsed');
  });
  if('inactivate' in trigger.dataset)
      document.querySelectorAll(trigger.dataset.inactivate).forEach(function(t){
          t.classList.remove('active')
      });
  trigger.classList.add('active');
}

/**
 *  hide
 *  hides an element pointed by a data-toggle attribute in the
 *  trigger element
 */
function wb_hide(trigger)
{
  document.querySelectorAll(trigger.dataset.hide).forEach(function(t){
    if(!t.classList.contains('collapsed'))
        t.classList.add('collapsed');
  });
  if('inactivate' in trigger.dataset)
      document.querySelectorAll(trigger.dataset.inactivate).forEach(function(t){
          t.classList.remove('active')
      });
  trigger.classList.add('active');
}

/**
 *  calls
 *  Makes an asynchornous GET call to an url
 */
function wb_get(url)
{
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(response){
      console.log(response)
  };
  xhr.open('GET', url);
  xhr.send()
}



/**
 *  Add event listeners when DOM is completely loaded
 *  equivalent to $(document).ready()
 */
document.addEventListener("DOMContentLoaded", function()
{
    document.querySelectorAll('[data-toggle]').forEach(function(t){
        t.addEventListener('click', function(){
            wb_toggle(t)
        });
    });
    document.querySelectorAll('[data-hide]').forEach(function(t){
        t.addEventListener('click', function(){
            wb_hide(t)
        });
    });
    document.querySelectorAll('[data-show]').forEach(function(t){
        t.addEventListener('click', function(){
            wb_show(t)
        });
    });
    document.querySelectorAll('[data-get]').forEach(function(t){
        t.addEventListener('click', function(e){
            e.preventDefault();
            var url = e.target.dataset.get;
            wb_get(url)
        });
    });
});
