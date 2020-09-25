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
var form_container   = document.querySelector('#form-tracklist-container');
var background_field = document.querySelector('.background-field');
function clean(){
    while(form_container.firstChild)
        form_container.removeChild(form_container.firstChild);
}

function closePopup(){
    clean();
    document.querySelector('.layout-form-audioset').dataset.active = '';
    if(background_field){
        background_field.classList.add('hidden');
        var input = document.querySelector('.background-field__input');
        if(input) input.value = '';
    }
    var placeholder = document.querySelector('.clip-marker--placeholder');
    if(placeholder)
        placeholder.remove();
    var marker_active = document.querySelector('.clip-marker.active');
    if(marker_active)
        marker_active.classList.remove('active');
}


jQuery(document).ready( function()
{
    // Forms
    document.querySelectorAll("[data-show-template]").forEach( function(button)
    {
        // Add action to build related template
        var show_template = function(e, dataset)
        {
            // Prevent 'bubbling'
            e.stopPropagation();

            // Get dataset attributes from the 'builder'
            var d           = dataset ? dataset : button.dataset;
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
                case 'delete':
                    var name = form_node.querySelector('.delete-text__name');
                    if(name) name.innerHTML = dataset['name'];
                    break;
                case 'update':
                    jQuery.ajax({
                        type : 'GET',
                        url  : endpoints[model]['get'] + id,
                        success : function(data)
                        {
                            Object.keys(data).forEach(function(field)
                            {
                                var widget = form.querySelector('[name='+field+']');
                                var audio_fields = [ 'audio_wav' ];
                                var image_fields = [ 'image' ];
                                // Image and color field values cannot be set directly
                                if( field != 'image' && field != 'image_alt' && field != 'order' && audio_fields.indexOf(field) == -1){
                                    widget.value = data[field];
                                }
                                // Create a proper image field
                                if( image_fields.includes(field) && data[field] )
                                {
                                    // As we cannot set image src via ajax we mock the image input
                                    // using JS

                                    var widget_container = document.querySelector('.field--' + field);
                                    // Placeholder
                                    var thumbnail = document.createElement('img');
                                    thumbnail.src = data[field];
                                    thumbnail.classList.add('form-field--'+field+'-preview');
                                    widget_container.appendChild(thumbnail);
                                    // Checkbox to delete the image
                                    var delete_input = document.createElement('input');
                                    delete_input.type = 'checkbox';
                                    delete_input.name = field + '_delete';
                                    delete_input.classList.add('form-field--'+field+'-delete');
                                    var delete_input_label = document.createElement('label');
                                    delete_input_label.innerHTML = 'Borrar la imagen';
                                    widget_container.appendChild(delete_input);
                                    widget_container.appendChild(delete_input_label);
                                }
                                // Create proper audio fields
                                audio_fields.forEach(function(audio_field)
                                {
                                    if( field == audio_field && data[field] )
                                    {
                                        // As we cannot set audio src via ajax we mock the image input
                                        // using JS
                                        var widget_container = document.querySelector('.field--' + audio_field);
                                        // Placeholder
                                        var placeholder = document.createElement('a');
                                        var input = widget_container.querySelector('input[type=file]');
                                        placeholder.href= data[field];
                                        placeholder.target = '_blank';
                                        placeholder.innerHTML = data[field];
                                        placeholder.classList.add('form-field__placeholder--audio');
                                        widget_container.insertBefore(placeholder, input);

                                        // Checkbox to delete the image
                                        var delete_div = document.createElement('div');
                                        delete_div.classList.add('form-field__delete--audio');
                                        var delete_input = document.createElement('input');
                                        delete_input.type = 'checkbox';
                                        delete_input.name = audio_field + '_delete';
                                        var delete_input_label = document.createElement('label');
                                        delete_input_label.innerHTML = 'Borrar el audio';
                                        delete_div.appendChild(delete_input);
                                        delete_div.appendChild(delete_input_label);
                                        widget_container.insertBefore(delete_div, input);
                                    }
                                });
                                form.querySelector('[name=pk]').value = data.pk;
                            });
                            // Create delete button
                            var delete_link = document.querySelector('[data-action=delete]');
                            delete_link.dataset.id = id;
                            delete_link.dataset.name = data['name'];
                            delete_link.addEventListener("click", (e)=>{  show_template(e, delete_link.dataset) });
                            delete_link.classList.add('visible');
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
                document.querySelector('.layout-form-audioset').classList.add('saving');
                var endpoint = endpoints[model][action];
                // If clip replace explicitly the value of the CKEDITOR field
                // to prevent from not updating it at all
                if(model=='clip'){
                    var readme_text = CKEDITOR.instances['id_readme'].getData();
                    document.querySelector('#id_readme').value = readme_text;
                }
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
                                  var field = document.querySelector('.form-field--' + fieldname);
                                  field.classList.add('not-validated');
                                  field.dataset.error = errors_msg[fieldname][0].message;
                            });
                            document.querySelector('.layout-form-audioset').classList.remove('saving');
                        }
                    },
                });
            });

            if(d.model == 'clip'){
                var active = document.querySelector('.clip-marker.active');
                if(active)
                  active.classList.remove('active');
                document.querySelector('.layout-form-audioset').dataset.active='clip';
                if(background_field){
                    document.querySelector('.background-field').classList.remove('hidden');
                }
                var placeholder = document.querySelector('.clip-marker--placeholder');
                if(placeholder){
                    placeholder.remove();
                }
                var active_marker = document.querySelector('.clip-marker[data-id="'+id+'"]');
                if(active_marker)
                    active_marker.classList.add('active');

            } else if(d.model == 'track'){
                document.querySelector('.layout-form-audioset').dataset.active='track';
            }


            // Remove previous content and add new one
            clean();
            form_container.appendChild(form_node);
            // Apply CKEditor widget to readme field
            if(model=='clip') {
                // alert();
                CKEDITOR.replace('id_readme', {
                    'toolbar' : 'Custom',
                    'width'   : '100%',
                    'extraPlugins': 'videodetector,',
                    'toolbar_Custom': [
                        ['Bold', 'Italic', 'Underline'],
                        ['NumberedList', 'BulletedList'],
                        ['Link', 'Unlink', 'Image', 'VideoDetector'],
                        ['RemoveFormat', 'Source'],
                    ],
                    'allowedContent' : true,
                });
            }
            form_container.scrollTo(0,0);
        };
        button.addEventListener("click", show_template);
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
