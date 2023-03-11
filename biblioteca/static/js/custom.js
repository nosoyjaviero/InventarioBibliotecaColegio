// $(document).ready(function(){
//     $("#cambiar-color").click(function(){
//         $("body").css("background-color", "red");
//     });
// });

$(document).ready(function(){
    $(".dateinput").datepicker({
        changeYear: true,
        changeMonth: true,
        dateFormat: 'dd/mm/yy'
    });
});