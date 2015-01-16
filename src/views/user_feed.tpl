% rebase('base.tpl')

<header>
  <nav>
    <div class="container">
      <div class="nav-wrapper">
        <a href="/" class="brand-logo">Лента</a>
        <ul id="nav-mobile" class="right side-nav">
          <li><a href="/"><i class="mdi-image-portrait left"></i>Лента</a></li>
          <li><a href="/logout"><i class="mdi-action-exit-to-app left"></i>Выход</a></li>
        </ul>
        <a class="button-collapse" href="#" data-activates="nav-mobile"><i class="mdi-navigation-menu"></i></a>
      </div>
    </div>
  </nav>
</header>

<main>
  <div class="container">
    <div class="section">
      <div class="row">
        <div class="col s12 m9 l6">
        % for task in tasks:
          % if task.is_photo_required:
            % if task.is_complete:
            <div class="card">
              <div class="card-image">
                <img src="{{task.photo_url}}">
                <span class="card-title">
                  Ты
                  % if task.partner:
                  и {{task.partner.name}}
                  % end
                </span>
              </div>
              <div class="card-content">
                <p>{{task.description}}</p>
              </div>
              % if not task.is_approved:
              <div class="card-action valign-wrapper">
                <a href="/" class="btn orange darken-2 white-text no-margin"><i class="mdi-action-schedule left"></i>
                  Проверяем
                </a>
              </div>
              % end
            </div>
            % else:
            <div class="card blue-grey darken-1">
              <div class="card-content white-text">
                <span class="card-title">
                  Ты
                  % if task.partner:
                  и {{task.partner.name}}
                  % end
                </span>
                <p>{{task.description}}</p>
              </div>
              <div class="card-action valign-wrapper">
                <form action="/user/upload_photo" method="POST" enctype="multipart/form-data" class="no-margin">
                  <input type="hidden" name="task_id" value="{{task.id}}">
                  <label class="btn waves-effect waves-light no-margin"><i class="mdi-file-cloud-upload left"></i>
                    Загрузить
                    <input type="file" name="photo_file">
                  </label>
                </form>
              </div>
            </div>
            % end
          % end
        % end
        </div>
      </div>
    </div>
  </div>
</main>
