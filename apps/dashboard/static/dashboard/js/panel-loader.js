/**
 *  Tracklist section panel
 *  Configuration screen
 */

document.addEventListener('DOMContentLoaded', function(){

    var panel_parent = document.querySelector('.layout-form-audioset__right');
    var panel    = document.querySelector('.audioset-background');
    var audioset = document.querySelector('.tracklist--audioset').dataset.audioset;

    var source_w = panel.getAttribute('width');
    var source_h = panel.getAttribute('height');
    var source_fw = source_w / panel.width;
    var source_fh = source_h / panel.height;
    panel.addEventListener('click', function(e){
        var clip_is_active = document.querySelector('.layout-form-audioset').dataset.active == 'clip';
        if(clip_is_active){
            var origin = e.target.getBoundingClientRect();
            var x = e.clientX - origin.left;
            var y = e.clientY - origin.top;

            var new_x = x * source_fw;
            var new_y = y * source_fh;
            document.querySelector('#id_pos_x').value = parseInt(new_x);
            document.querySelector('#id_pos_y').value = parseInt(new_y);
        }
    });
    jQuery.get('/api/1.0/track/clips/'+audioset, function(data){
        data.forEach( function(item){
            var pos_x = item.pos_x;
            var pos_y = item.pos_y;
            var marker = document.createElement('div');
            marker.classList.add('clip-marker');
            marker.classList.add('clip-marker--panel');
            marker.style.left = (pos_x / source_fw - 20) + "px";
            marker.style.top  = (pos_y / source_fh - 20) + "px";
            marker.style.backgroundColor = item.track[0].color;
            marker.dataset.id = item.pk;
            marker.addEventListener('click', function(){
              document.querySelector('.clip-actions__edit[data-id="'+item.pk+'"]').click();
            })
            panel_parent.appendChild(marker);
        });
    });
});
