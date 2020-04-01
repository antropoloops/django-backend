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

function closePopup(){
    clean();
    document.querySelector('#map').classList.remove('show_finder');
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
                            Object.keys(data.fields).forEach(function(field)
                            {
                                var widget = form.querySelector('[name='+field+']');
                                // Image and color field values cannot be set directly
                                if(field != 'image' && field != 'order'){
                                    widget.value = data.fields[field];
                                }
                                if( field == 'image' && data.fields[field] )
                                {
                                    // As we cannot set image src via ajax we mock the image input
                                    // using JS
                                    var widget_container = document.querySelector('.form-field--image');
                                    // Placeholder
                                    var thumbnail = document.createElement('img');
                                    thumbnail.src = '/media/' + data.fields['image'];
                                    thumbnail.classList.add('form-field--image-preview');
                                    widget_container.appendChild(thumbnail);
                                    // Checkbox to delete the image
                                    var delete_input = document.createElement('input');
                                    delete_input.type = 'checkbox';
                                    delete_input.name = 'image_delete';
                                    delete_input.classList.add('form-field--image-delete');
                                    var delete_input_label = document.createElement('label');
                                    delete_input_label.innerHTML = 'Borrar la imagen';
                                    widget_container.appendChild(delete_input);
                                    widget_container.appendChild(delete_input_label);
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
                // TODO: not rely on FormData to prevent old browsers from not working at all
                var data = new FormData(form);
                if(action=='create')
                    delete data['pk']
                jQuery.ajax({
                    type : 'POST',
                    url  : endpoint,
                    data : data,
                    processData: false,
                    contentType: false,
                    success : function(response)
                    {
                        location.reload();
                    },
                    error : function(response)
                    {
                        // Validation failed
                        if(response.status==400)
                        {
                            var form_errors = document.querySelector('.form-errors');
                            form_errors.classList.remove('hidden');
                            var errors_msg = JSON.parse(response.responseText);
                            Object.keys(errors_msg).forEach( function(fieldname) {
                                  console.log(fieldname);
                                  var field = document.querySelector('.form-field--' + fieldname);
                                  field.classList.add('not-validated');
                                  field.dataset.error = errors_msg[fieldname][0].message;
                            });
                        }
                    },
                });
            });

            if(d.model == 'clip'){
                document.querySelector('#map').classList.add('show_finder');
            }


            // Remove previous content and add new one
            clean();
            form_container.appendChild(form_node);
            form_container.scrollTo(0,0);
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
            error : function(response){
                console.log('Error: ', response);
            },
        });
    }
});
