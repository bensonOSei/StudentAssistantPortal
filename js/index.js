$(document).ready(function () {
  $("#openComp").click(() => {
    $("#complaint").toggle("slow", () => {
      $("#openComp").toggleClass("active");
      $("#openAccess").toggleClass("active", () => {
        $("#openComp").css("background-color", "red");
      });

      $("#access_module").toggle();
    });

  });

  $("#openAccess").click(() => {
    $("#access_module").toggle("slow", () => {
      $("#openAccess").toggleClass("active");
      $("#openComp").toggleClass("active");

      $("#complaint").toggle();
    });

  });
});
