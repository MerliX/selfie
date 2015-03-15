% rebase('base.tpl')

% include('moderator_menu.tpl', logo=u'Люди')

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

      <div class="row">
        <div class="col s12">
          <table class="striped">
            <thead>
              <tr>
                <th>Имя</th>
                <th>Код доступа</th>
                <th>Баллы</th>
              </tr>
            </thead>

            <tbody>
              % for user in users:
              <tr>
                <td>
                    <a href="/user/feed?user={{user.id}}">{{user.name}}</a>
                </td>
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
