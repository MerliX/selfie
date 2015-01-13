% rebase('base.tpl')

<header>
  <nav>
    <div class="container">
      <div class="nav-wrapper">
        <a href="/moderator/feed" class="brand-logo">Задания</a>
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
      % if created_perk:
      <div class="row">
        <div class="col s12">
          <blockquote>
            Уровень: {{created_level}}<br>
            Задание: {{created_perk}}
          </blockquote>
        </div>
      </div>
      % end
      <div class="row">
        <form class="col s12" method="POST" action="/moderator/add_perk">
          <div class="row">
            <div class="input-field col s12 l7">
              <input id="add_perk_text" name="add_perk_text" type="text">
              <label for="add_perk_text">Задание</label>
            </div>
            <div class="input-field col s3 l2">
              <input id="add_perk_level" name="add_perk_level" type="text">
              <label for="add_perk_level">Уровень</label> 
            </div>
            <div class="col s9 l3">
              <button class="btn waves-effect waves-light" type="submit"><i class="mdi-action-note-add left"></i>
                Добавить
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <div class="section">
      <div class="row">
        <div class="col s12">
          <table class="striped">
            <thead>
              <tr>
                  <th>Задание</th>
                  <th>Уровень</th>
              </tr>
            </thead>

            <tbody>
              % for perk in perks:
              <tr>
                <td>{{perk.text}}</td>
                <td>{{perk.level}}</td>
              </tr>
              % end
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</main>
