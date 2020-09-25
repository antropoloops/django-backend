/**
 *    Creates a thumbnail from a html file input using HTML5 File API
 */

+(function(){
    widgets = document.querySelectorAll('div.field__widget--picture-preview');
    widgets.forEach( function(widget)
    {
        var placeholder = widget.querySelector('.placeholder');
        var input = widget.querySelector('input[type=file]');
        var current = widget.querySelector('.widget-wrapper a');
        if(current){
              placeholder.innerHTML = "<img src='" + current.href + "' />";
        }
        console.log(placeholder.innerHTML);
        input.addEventListener(
            'change',
            function(e) {
                if (input.files && input.files[0])
                {
                  var reader = new FileReader();
                    reader.onload = function(e) {
                        placeholder.innerHTML = "<img src='" + e.target.result + "' />";
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            },
        false);
    });
})();
