/**
 *  Adds JS to Audioset's modeladmin
 */
document.addEventListener("DOMContentLoaded", function()
{
    /**
     *   Conditional fields
     */

    var mode_display_widget = document.querySelector('#id_mode_display');

    function show_related_fields(display_mode)
    {
        // Maps fields to be *hidden* by the display mode select
        var fieldnames = {
            '1' : [
                'map_url',
                'map_lambda',
                'map_shift_vertical',
                'map_scale',
                'map_center_x',
                'map_center_y'
            ],
            '2' : [
                'panel_background'
            ],
        };

        // Show every field in the fieldset
        var candidates = '.fieldset--display [class*="field-"]:not(.field-mode_display)';
        var fields = document.querySelectorAll(candidates);
        fields.forEach( function(field){
            field.classList.remove('hidden');
        });

        // Hide fields unrelated to current selection
        fieldnames[display_mode].forEach( function(fieldname){
            var field = document.querySelector('.field-' + fieldname);
            field.classList.add('hidden');
        });
    };

    // Add listener to display mode select
    mode_display_widget.addEventListener('change', function(e){
          show_related_fields(e.target.value);
      });

    // Do it on the initial value
    show_related_fields(mode_display_widget.value);
});
