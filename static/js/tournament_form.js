
function set_max_members_visible() {
    if ($('#id_tourn_type').val() === 'T'){
        $('#id_max_team_members').removeClass('d-none');
        $('label').eq(3).removeClass('d-none')
    } else {
        $('#id_max_team_members').addClass('d-none');
        $('label').eq(3).addClass('d-none')
    }
}

set_max_members_visible();

$('#id_tourn_type').change(set_max_members_visible);