/* ══════════════════════════════════════════════
   StudyCircle — script.js (jQuery)
══════════════════════════════════════════════ */
$(function(){

  /* 1 ── Auto-dismiss flash alerts ──────────── */
  setTimeout(function(){
    $(".sc-alert").fadeTo(400, 0).slideUp(300, function(){ $(this).remove(); });
  }, 6000);

  /* 2 ── Bootstrap tooltips ──────────────────── */
  $('[data-bs-toggle="tooltip"]').each(function(){
    new bootstrap.Tooltip(this);
  });

  /* 3 ── Live search filter (index page) ─────── */
  var $cols = $(".sc-card-col");
  if ($cols.length) {
    var timer;
    $("#liveSearch").on("input", function(){
      clearTimeout(timer);
      var q = $.trim($(this).val()).toLowerCase();
      timer = setTimeout(function(){
        if (!q) { $cols.show(); return; }
        var shown = 0;
        $cols.each(function(){
          var match = $(this).text().toLowerCase().indexOf(q) > -1;
          $(this).toggle(match);
          if (match) shown++;
        });
        // update count badge
        var label = shown + " group" + (shown !== 1 ? "s" : "");
        $("#cardGrid").closest("section").find(".sc-cnt-badge").text(label);
      }, 220);
    });

    // Clear live search when form is submitted
    $("#filterForm").on("submit", function(){
      $("#liveSearch").off("input"); // let server handle it
    });
  }

  /* 4 ── Reject/remove confirm dialogs ───────── */
  $(document).on("submit", ".sc-reject-form", function(e){
    var name = $(this).closest(".sc-req-row").find(".fw-600").first().text().trim();
    if (!confirm("Reject request from " + name + "?\nThis cannot be undone.")){
      e.preventDefault();
    }
  });

  $(document).on("submit", ".sc-remove-form", function(e){
    var name = $(this).closest(".sc-hist-row").find(".fw-500").first().text().trim();
    if (!confirm("Remove " + name + " from this group?")) {
      e.preventDefault();
    }
  });

  /* 5 ── Announce form validation ────────────── */
  $("#annForm").on("submit", function(e){
    var t = $.trim($(this).find("[name=title]").val());
    var b = $.trim($(this).find("[name=body]").val());
    if (!t || !b) {
      e.preventDefault();
      alert("Both title and message are required.");
    }
  });

  /* 6 ── Discussion form basic check ─────────── */
  $("#discussForm").on("submit", function(e){
    var a = $.trim($(this).find("[name=author]").val());
    var m = $.trim($(this).find("[name=message]").val());
    if (a.length < 2 || m.length < 5) {
      e.preventDefault();
      alert("Please enter your name and a message (min 5 characters).");
    }
  });

  /* 7 ── Dashboard email form ─────────────────── */
  $("#dashForm").on("submit", function(e){
    var em = $.trim($("#dashEmail").val());
    var rx = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    if (!rx.test(em)) {
      e.preventDefault();
      $("#dashEmail").addClass("is-invalid");
      if (!$("#dashErrMsg").length) {
        $('<div class="sc-err" id="dashErrMsg">Enter a valid email address.</div>')
          .insertAfter("#dashEmail");
      }
    }
  });
  $("#dashEmail").on("input", function(){
    $(this).removeClass("is-invalid");
    $("#dashErrMsg").remove();
  });

  /* 8 ── Smooth scroll to #discuss anchor ─────── */
  if (window.location.hash === "#discuss") {
    var $t = $("#discuss");
    if ($t.length) {
      setTimeout(function(){
        $("html,body").animate({ scrollTop: $t.offset().top - 80 }, 400);
      }, 200);
    }
  }

});
