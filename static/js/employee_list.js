
$(function(){
    $('.check input').on("change", function () {
      if ($(this).is(":checked")) {
        $(this).closest(".unit").addClass("selected");
      } else {
        $(this).closest(".unit").removeClass("selected");
      }
    });

    $('.head .check input').on("change", function () {
      if ($(this).is(":checked")) {
        $('.unit .check input:checkbox').not(this).trigger("click");
      } else {
        $('.unit .check input:checkbox').not(this).trigger("click");
      }
    });

})