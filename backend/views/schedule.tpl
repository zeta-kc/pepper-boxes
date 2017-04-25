<!DOCTYPE html>
<html lang=ja>
  <head>
    <meta charset="UTF-8">
    <title>{{date}}のスケジュール</title>
  </head>

  <body>
    <h1>{{date}}のスケジュール</h1>
    <ul>
    % for item in schedule:
        <li>{{item}}</li>
    % end
    </ul>
  </body>
</html>