% rebase('base.tpl')

<header>
  <nav>
    <div class="container">
      <div class="nav-wrapper">
        <a href="/moderator/feed" class="brand-logo">Лента</a>
        <ul id="nav-mobile" class="right side-nav">
          <li><a href="/moderator/feed"><i class="mdi-action-thumbs-up-down left"></i>Лента</a></li>
          <li><a href="/moderator/users"><i class="mdi-social-people left"></i>Люди</a></li>
          <li><a href="/moderator/perks"><i class="mdi-action-assignment left"></i>Задания</a></li>
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
          % if selfie:
          <div class="card">
            <div class="card-image">
              <img src="{{selfie.photo_url}}">
              <span class="card-title">
                {{selfie.author.name}}
                % if selfie.victim.name != selfie.author.name:
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
            <div class="card-action valign-wrapper">
              <form action="/moderator/approve_selfie" method="POST" class="no-margin">
                <input type="hidden" name="selfie_id" value="{{selfie.id}}">
                <button class="btn waves-effect waves-light no-margin green darken-2" type="submit" name="decision" value="approve">
                  <i class="mdi-action-thumb-up left"></i>
                  ОК
                </button>
                <button class="btn waves-effect waves-light no-margin red darken-2" type="submit" name="decision" value="reject">
                  <i class="mdi-action-thumb-down left"></i>
                  Плохо
                </button>
              </form>
            </div>
          </div>
          % else:
          <p>Пока ничего нет.</p>
          % end
        </div>
      </div>
    </div>
  </div>
</main>
