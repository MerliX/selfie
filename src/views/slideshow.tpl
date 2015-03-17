<html>
  <head>
    <link type="text/css" rel="stylesheet" href="/static/css/jquery.kenburnsy.css" media="screen,projection">
    <title>#селфидамп</title>
  </head>

  <body>
    <div class="wrapper">
      % for task in tasks:
      <img src="{{task.photo_url}}">
      % end
    </div>
    <script type="text/javascript" src="/static/js/jquery-2.1.3.min.js"></script>
    <script type="text/javascript" src="/static/js/jquery.velocity.min.js"></script>
    <script type="text/javascript" src="/static/js/jquery.kenburnsy.min.js"></script>
    <script type="text/javascript" src="/static/js/slideshow.js"></script>
  </body>
</html>
