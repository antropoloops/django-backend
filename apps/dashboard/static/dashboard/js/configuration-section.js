/**
 *  Dashboard scripts
 *  Configuration screen
 */

document.addEventListener("DOMContentLoaded", function()
{
    // Add listeners
    var mode_selector = document.querySelector('.mode-selector');
    document.querySelectorAll("[name='mode_display']").forEach(function(selector){
        selector.addEventListener('change', function(e){
            var value = e.target.value;
            mode_selector.dataset.currentState = value;
        });
    });

    document.querySelector('.form-audioset-configure__fieldset-label').addEventListener('click', function(e){
        document.querySelector('.form-audioset-configure__fieldset-fields').classList.toggle('hidden');
    })
});
