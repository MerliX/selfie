% rebase('base.tpl')

% include('moderator_menu.tpl', logo=u'Покупки')

<main>
  <div class="container">
    <div class="section">
      <div class="row">
        % for item in items:
        <div class="col s12 m6 l4">
          <div class="card">
            <div class="card-image">
              <img src="{{item.user.photo_url}}">
              <span class="card-title">
                {{item.user.name}}
              </span>
            </div>
            <div class="card-content">
              <p>{{item.item.description}}</p>
            </div>
            <div class="card-action valign-wrapper">
              <form action="/moderator/deliver_item" method="POST" class="no-margin">
                <input type="hidden" name="item_id" value="{{item.id}}">
                <button class="btn waves-effect waves-light no-margin green darken-2" type="submit">
                  <i class="mdi-action-done left"></i>
                  Выдали
                </button>
              </form>
            </div>
          </div>
        </div>
        % end
      </div>
    </div>
  </div>
</main>
