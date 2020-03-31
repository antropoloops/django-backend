/**
 *  Dashboard scripts
 *  Tracklist screen
 */

 // Endpoints for Ajax calls
 var endpoints =
 {
     'track' : {
         'get'    : '/api/1.0/track/',
         'create' : '/api/1.0/track/crea',
         'update' : '/api/1.0/track/edita',
         'delete' : '/api/1.0/track/borra',
         'sort'   : '/api/1.0/track/ordena',
     },
     'clip' : {
         'get'    : '/api/1.0/clip/',
         'create' : '/api/1.0/clip/crea',
         'update' : '/api/1.0/clip/edita',
         'delete' : '/api/1.0/clip/borra',
         'sort'   : '/api/1.0/clip/ordena',
     },
 }

// Container node to hold forms in the view
var form_container  = document.querySelector('#form-tracklist-container');

function clean(){
    while(form_container.firstChild)
        form_container.removeChild(form_container.firstChild);
}


jQuery(document).ready( function()
{
    // Forms
    document.querySelectorAll("[data-show-template]").forEach( function(button)
    {
        // Add action to build related template
        button.addEventListener("click", function(e)
        {
            // Prevent 'bubbling'
            e.stopPropagation();

            // Get dataset attributes from the 'builder'
            var d           = button.dataset;
            var template_id = '#' + d.showTemplate;
            var model       = d.model;
            var action      = d.action;
            var track       = d.track;
            var id          = d.id;

            // Build template
            var template_markup = document.querySelector(template_id);
            var form_node       = template_markup.content.cloneNode(true);
            var form            = form_node.querySelector('form');
            if(track)
                form.querySelector('[name="track"]').value = track;
            if(id)
                form.querySelector('[name="pk"]').value = id;
            if(action)
                form.setAttribute('data-action', action);

            // Populate form with proper data
            switch(action)
            {
                case 'update':
                    jQuery.ajax({
                        type : 'GET',
                        url  : endpoints[model]['get'] + '?pk=' + id,
                        success : function(response)
                        {
                            var data = JSON.parse(response)[0];
                            Object.keys(data.fields).forEach(function(field){
                                var widget = form.querySelector('[name='+field+']');
                                // Image and color field values cannot be set directly
                                if(field != 'image'){
                                    widget.value = data.fields[field];
                                }
                                form.querySelector('[name=pk]').value = data.pk;
                            });
                        },
                        error : function(req){
                            console.log('Error: ', req);
                        },
                    });
                break;
            }

            // Update submit
            form.addEventListener('submit', function(e){
                e.preventDefault();
                var endpoint = endpoints[model][action];
                // Serialize form data but delete pks to
                // avoid breaking creation forms
                var data = jQuery(form).serialize();
                if(action=='create')
                    delete data['pk']
                jQuery.ajax({
                    type : 'POST',
                    url  : endpoint,
                    data : data,
                    success : function(req)
                    {
                        // TODO: catch form errors here
                        location.reload();
                    },
                    error : function(req)
                    {
                        console.log('Error: ', req);
                    },
                });
            });

            // Remove previous content and add new one
            clean();
            form_container.appendChild(form_node);
        });
    });


    // Fieldsets
    document.querySelectorAll(".collapsible .fieldset__name").forEach(function(el){
        el.addEventListener("click", function(e){
            e.target.parentNode.classList.toggle("collapsed");
        })
    });


    // Drag and drop

    var containerSelector = '.tracklist';
    var containers = document.querySelectorAll(containerSelector);

    if (containers.length === 0) {
        return false;
    }

    jQuery( function(){
        jQuery('.tracklist').sortable({
            stop : order_tracks,
        });
        jQuery('.track__clips').sortable({
            stop : function(e){
                order_clips(e.target);
            },
        });
    });

    function order_tracks()
    {
        var tracks   = document.querySelectorAll('.tracklist__item');
        var audioset = document.querySelector('.tracklist').dataset.audioset;
        var csrf     = document.querySelector('.tracklist').dataset.csrf;
        var data   = {
            'csrfmiddlewaretoken' : csrf,
            'audioset' : audioset
        };
        tracks.forEach( function(track, new_ordinal){
            data['track_' + track.dataset.id ] = new_ordinal + 1;
        });
        jQuery.ajax({
            type : 'POST',
            url  : endpoints['track']['sort'],
            data : jQuery.param(data),
            success : function(response)
            {
                location.reload();
            },
            error : function(response){
                console.log('Error: ', response);
            },
        });
    }

    function order_clips(list){
        var clips    = list.querySelectorAll('.clip');
        var track    = list.dataset.track;
        var csrf     = document.querySelector('.tracklist').dataset.csrf;
        var data   = {
            'csrfmiddlewaretoken' : csrf,
            'track' : track
        };
        clips.forEach( function(clip, new_ordinal){
            data['clip_' + clip.dataset.id ] = new_ordinal + 1;
        });
        jQuery.ajax({
            type : 'POST',
            url  : endpoints['clip']['sort'],
            data : jQuery.param(data),
            success : function(response)
            {
                // pass
            },
            error : function(response){
                console.log('Error: ', response);
            },
        });
    }
});
