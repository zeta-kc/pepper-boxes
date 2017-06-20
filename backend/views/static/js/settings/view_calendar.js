function showData(jsonfile) {
  $.getJSON(jsonfile, function (data) {
    var
      ulObj = $("#panel"),
      event = data.events,
      len = event.length;
    if (len == 0) {
      ulObj.append($("<dt>予定はありません</dt>").attr({ "id": 1 }));
    }
    for (var i = 0; i < len; i++) {
      ulObj.append($("<dt>" + (event[i].start + '~' + event[i].end) + "</dt>").attr({ "id": 1 + i }));
      ulObj.append("<dd>" + (event[i].summary) + "</dd>");
    }
  });
};

$(function () {

  showData("/schedule");
});