$(document).ready(function () {
  const $input = $("#wcaInput");
  let info = null;

  $input.on("input", function () {

    const wcaid = $input.val().trim();
    if (wcaid.length === 10) {
      // 發送 API 請求
      $.get(`https://www.worldcubeassociation.org/api/v0/persons/${wcaid}`)
        .done(function (data) {
          $input.removeClass("is-invalid").addClass("is-valid");

          const person = data.person;
          const fullName = person.name;
          const match = fullName.match(/\(([^)]+)\)/);

          info = {
            englishName: fullName,
            gender: person.gender,
            country: person.country_iso2,
            chineseName: match ? match[1] : "",  // 只取出括號內的中文
            wcaId: person.wca_id
          };

          console.log(info);

          // 存入 localStorage
          localStorage.setItem("wcaPerson", JSON.stringify(info));
        })
        .fail(function () {
          $input.removeClass("is-valid").addClass("is-invalid");
          localStorage.removeItem("wcaPerson");
        });
    } else {
      $input.removeClass("is-valid is-invalid");
      localStorage.removeItem("wcaPerson");
    }
  });

  $("#WCAID_Button").on("click", function () {
    if (info) {
      window.location.href = "registration_form copy.html";
    } else {
      $input.removeClass("is-valid").addClass("is-invalid");
    }
  });

  $("#NoneWcaId").on("click", function () {
    window.location.href = "registration_form copy.html"
  });

});
