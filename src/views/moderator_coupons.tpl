% rebase('base.tpl')

% include('moderator_menu.tpl', logo=u'Купоны')

<main>
  <div class="container">
    <div class="section">
      % if created_coupon:
      <div class="row">
        <div class="col s12">
          <blockquote>
            {{created_coupon}}
            <br>Вознаграждение: {{created_reward}}
            <br>Лимит активаций на одного пользователя: {{created_limit}}
            <br>Количество сгенерированных купонов: {{created_count}}
          </blockquote>
        </div>
      </div>
      % end
      <div class="row">
        <form class="col s12" method="POST" action="/moderator/add_coupon">
          <div class="row">
            <div class="input-field col s12">
              <input id="add_coupon_description" name="add_coupon_description" type="text">
              <label for="add_coupon_description">Описание</label>
            </div>
            <div class="input-field col s4">
              <input id="add_coupon_count" name="add_coupon_count" type="text">
              <label for="add_coupon_count">Количество кодов</label> 
            </div>
            <div class="input-field col s4">
              <input id="add_coupon_limit" name="add_coupon_limit" type="text">
              <label for="add_coupon_limit">Лимит активаций</label> 
            </div>
            <div class="input-field col s4">
              <input id="add_coupon_reward" name="add_coupon_reward" type="text">
              <label for="add_coupon_reward">Вознаграждение</label> 
            </div>
            <div class="col s12">
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
                  <th>Описание</th>
                  <th>Вознаграждение</th>
                  <th>Лимит активаций на человека</th>
                  <th>Коды</th>
                  <th></th>
              </tr>
            </thead>

            <tbody>
              % for kind, coupon in coupons.items():
              <tr>
                <td>{{coupon['description']}}</td>
                <td>{{coupon['reward']}}</td>
                <td>{{coupon['limit']}}</td>
                <td>
                  % for code, active in coupon['codes']:
                  <span class="">{{code}}</span><br>
                  % end
                </td>
                <td>
                  <form method="POST" action="/moderator/delete_coupon" class="no-margin">
                    <input type="hidden" name="coupon_kind" value="{{kind}}">
                    <button type="submit" class="waves-effect waves-red btn-flat red-text no-margin"><i class="mdi-action-delete"></i></button>
                  </form>
                </td>
              </tr>
              % end
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</main>
