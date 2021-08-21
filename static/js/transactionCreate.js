// Functional code, not the prettiest one
document.getElementById('div_id_member_value_1').style.display = 'none'
document.getElementById('div_id_member_value_2').style.display = 'none'

document.getElementById('id_particular_sharing').addEventListener('change', (e) => {
    if (e.currentTarget.checked) {
        document.getElementById('div_id_member_value_1').style.display = 'block'
        document.getElementById('div_id_member_value_2').style.display = 'block'
    } else {
        document.getElementById('div_id_member_value_1').style.display = 'none'
        document.getElementById('div_id_member_value_2').style.display = 'none'
    }
});
