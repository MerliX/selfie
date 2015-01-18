% rebase('base.tpl')

% include('moderator_menu.tpl', logo=u'Лента')

<main>
  <div class="container">
    <div class="section">
      % if task:
      <div class="row">
        <div class="col s12 m9 l6">
          <div class="card">
            <div class="card-image">
              <img src="{{task.photo_url}}">
              <span class="card-title">
                {{task.assignee.name}}
                % if task.partner:
                и {{task.partner.name}}
                % end
              </span>
            </div>
            <div class="card-content">
              <p>{{task.description}}</p>
            </div>
            <div class="card-action valign-wrapper">
              <form action="/moderator/approve_task" method="POST" class="no-margin">
                <input type="hidden" name="task_id" value="{{task.id}}">
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
        </div>
      </div>
      % if task.partner:
      <div class="row">
        <div class="col s6 m4 l3">
          <div class="card">
            <div class="card-image">
              <img src="{{task.assignee.photo_url}}">
              <span class="card-title">{{task.assignee.name}}</span>
            </div>
          </div>
        </div>
        <div class="col s6 m4 l3">
          <div class="card">
            <div class="card-image">
              <img src="{{task.partner.photo_url}}">
              <span class="card-title">{{task.partner.name}}</span>
            </div>
          </div>
        </div>
      </div>
      % end
      % else:
      <div class="row">
        <div class="col s12 m9 l6">
          <p>Пока ничего нет.</p>
        </div>
      </div>
      % end
    </div>
  </div>
</main>
