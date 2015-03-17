% rebase('base.tpl')

% include('user_menu.tpl')

<main>
  <div class="container">
    <div class="section">
      % if reject_coupon:
      <div class="row">
        <div class="col s12">
          <blockquote>
            % if reject_coupon == 'limit':
            Хватит уже с тебя баллов за это достижение!
            % elif reject_coupon == 'doesnotexist':
            Такого кода нет, или его уже кто-то активировал.
            % end
          </blockquote>
        </div>
      </div>
      % end
      <div class="row">
        <form class="col s12" method="POST" action="/user/activate_coupon">
          <div class="row">
            <div class="input-field col s8 m6 l3">
              <input id="coupon_code" name="coupon_code" type="text">
              <label for="coupon_code">Код</label> 
            </div>
            <div class="col s4">
              <button class="btn waves-effect waves-light" type="submit">Ура!</button>
            </div>
          </div>
        </form>
      </div>

      <div class="row">
        <div class="col s12 m9 l6">
          % for achievement in achievements: 
          <div class="card-panel {{'teal lighten-1 white-text' if achievement.code == activate_coupon else 'teal lighten-4'}}">
            <span class="achievement-reward">
              <i class="mdi-editor-attach-money user-money-icon"></i>{{achievement.reward}}
            </span>
            {{achievement.description}}
          </div>
          % end
        </div>
      </div>
    </div>
  </div>
</main>