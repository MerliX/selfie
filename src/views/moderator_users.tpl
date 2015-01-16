% rebase('base.tpl')

<header>
  <nav>
    <div class="container">
      <div class="nav-wrapper">
        <a href="/moderator/feed" class="brand-logo">Люди</a>
        <ul id="nav-mobile" class="right side-nav">
          <li><a href="/moderator/feed"><i class="mdi-action-thumbs-up-down left"></i>Лента</a></li>
          <li><a href="/moderator/users"><i class="mdi-social-people left"></i>Люди</a></li>
          <li><a href="/moderator/requirements"><i class="mdi-action-assignment left"></i>Требования</a></li>
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
      % if created_name:
      <div class="row">
        <div class="col s12">
          <blockquote>
            Имя: {{created_name}}<br>
            Код доступа: {{created_access_code}}
          </blockquote>
        </div>
      </div>
      % end
      <div class="row">
        <form class="col s12" method="POST" action="/moderator/add_user">
          <div class="row">
            <div class="input-field col s12 m6 l8">
              <input id="add_user_name" name="add_user_name" type="text">
              <label for="add_user_name">Имя пользователя</label> 
            </div>
            <div class="col s12 m6 l4">
              <button class="btn waves-effect waves-light" type="submit"><i class="mdi-social-person-add left"></i>
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
                <th>Имя</th>
                <th>Код доступа</th>
                <th>Очки</th>
              </tr>
            </thead>

            <tbody>
              % for user in users:
              <tr>
                <td>{{user.name}}</td>
                <td>{{user.access_code}}</td>
                <td>{{user.score}}</td>
              </tr>
              % end
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</main>
