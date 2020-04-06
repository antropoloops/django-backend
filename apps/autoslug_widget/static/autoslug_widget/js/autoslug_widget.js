/**
 *    Autocompletes slug field from another field
 */

 function slugify(text)
 {
   var slug = text.toString().toLowerCase()
     .replace(/\s+/g, '-')           // Replace spaces with -
     .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
     .replace(/\-\-+/g, '-')         // Replace multiple - with single -
     .replace(/^-+/, '')             // Trim - from start of text
     .replace(/-+$/, '');            // Trim - from end of text
   return slug.substring(0, 50);
 }

document.addEventListener('DOMContentLoaded', function(){
    widgets = document.querySelectorAll('[data-autoslug-src]');
    widgets.forEach( function(widget)
    {
        var src = document.querySelector('input[name=' + widget.dataset.autoslugSrc + ']');
        src.addEventListener('blur', function(e){
            widget.value = slugify(e.target.value);
        })
    });
});
