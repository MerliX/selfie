% rebase('base.tpl')

<main>
  <div class="container">
    <div class="section">
      <div class="row">
        <div class="col s12 m9 l6">
          % for task in tasks:
          <div class="card">
            <div class="card-image">
              <img src="{{task.photo_url}}">
            </div>
            <div class="card-content">
              <p>{{task.difficulty}}</p>
              <p>{{task.assignee.name}} &amp; {{task.partner.name if task.partner else ''}}</p>
              <p>{{task.description}}</p>
            </div>
          </div>
          % end
        </div>
      </div>
    </div>
  </div>
</main>
