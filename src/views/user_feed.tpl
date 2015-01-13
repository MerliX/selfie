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
          <ul class="collapsible">
          % selfies = user.get_ordered_selfies()
          % open_level = max(selfies.keys())
          % for level in sorted(selfies.keys()):
            <li>
              <div class="collapsible-header{{' open-level' if level == open_level else ''}}">Уровень {{level}}</div>
              <div class="collapsible-body">
                % for selfie in selfies[level]:
                % if selfie.is_uploaded:
                <div class="card">
                  <div class="card-image">
                    <img src="{{selfie.photo_url}}">
                    <span class="card-title">
                      Ты
                      % if selfie.victim.name != user.name:
                      и {{selfie.victim.name}}
                      %end
                    </span>
                  </div>
                  <div class="card-content">
                    <ul>
                      % for perk in selfie.combined_perks():
                      <li>{{perk}}</li> 
                      % end
                    </ul>
                  </div>
                  % if not selfie.is_approved:
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
                      % if selfie.victim.name != user.name:
                      и {{selfie.victim.name}}
                      %end
                    </span>
                    <ul>
                      % for perk in selfie.combined_perks():
                      <li>{{perk}}</li> 
                      % end
                    </ul>
                  </div>
                  <div class="card-action valign-wrapper">
                    <form action="/user/upload_selfie" method="POST" enctype="multipart/form-data" class="no-margin">
                      <input type="hidden" name="selfie_id" value="{{selfie.id}}">
                      <label class="btn waves-effect waves-light no-margin"><i class="mdi-file-cloud-upload left"></i>
                        Загрузить
                        <input type="file" name="selfie_file">
                      </label>
                    </form>
                  </div>
                </div>
                % end
                % end
              </div>
            </li>
          % end
          </ul>
        </div>
      </div>
    </div>
  </div>
</main>
