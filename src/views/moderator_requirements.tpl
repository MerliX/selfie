% rebase('base.tpl')

% include('moderator_menu.tpl', logo=u'Требования')

<main>
  <div class="container">
    <div class="section">
      % if created_requirement:
      <div class="row">
        <div class="col s12">
          <blockquote>
            Требование
            % if created_is_basic == 'True':
            (основное):
            % else:
            (дополнительное):
            % end
            {{created_requirement}}
            <br>
            Сложность: {{created_difficulty}}
          </blockquote>
        </div>
      </div>
      % end
      <div class="row">
        <form class="col s12" method="POST" action="/moderator/add_requirement">
          <div class="row">
            <div class="input-field col s12">
              <input id="add_requirement_description" name="add_requirement_description" type="text">
              <label for="add_requirement_description">Требование</label>
            </div>
            <div class="input-field col s6">
              <input id="add_requirement_difficulty" name="add_requirement_difficulty" type="text">
              <label for="add_requirement_difficulty">Сложность</label> 
            </div>
            <div class="input-field col s6">
              <input type="checkbox" id="add_requirement_is_basic" name="add_requirement_is_basic" checked="checked">
              <label for="add_requirement_is_basic" class="black-text">Основное</label>
            </div>
            <div class="col s12">
              <button class="btn waves-effect waves-light" type="submit"><i class="mdi-action-note-add left"></i>
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
                  <th>Требование</th>
                  <th>Сл<span class="hide-on-small-only">ожность</span></th>
                  <th>Осн<span class="hide-on-small-only">овное</span></th>
              </tr>
            </thead>

            <tbody>
              % for requirement in requirements:
              <tr class="requirement-row" data-id="{{requirement.id}}">
                <td class="requirement-description">{{requirement.description}}</td>
                <td class="requirement-difficulty">{{requirement.difficulty}}</td>
                <td class="requirement-is-basic">
                  <a name="requirement-{{requirement.id}}"></a>
                  % if requirement.is_basic:
                  <i class="mdi-action-done"></i>
                  % end
                </td>
              </tr>
              % end
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <div id="editmodal" class="modal">
    <form class="col s12" method="POST" action="/moderator/edit_requirement">
      <input type="hidden" name="edit_requirement_id" id="edit_requirement_id" value="">
      <div class="row">
        <div class="input-field col s12">
          <input id="edit_requirement_description" name="edit_requirement_description" type="text">
          <label for="edit_requirement_description">Требование</label>
        </div>
        <div class="input-field col s6">
          <input id="edit_requirement_difficulty" name="edit_requirement_difficulty" type="text">
          <label for="edit_requirement_difficulty">Сложность</label> 
        </div>
        <div class="input-field col s6">
          <input type="checkbox" id="edit_requirement_is_basic" name="edit_requirement_is_basic">
          <label for="edit_requirement_is_basic" class="black-text">Основное</label>
        </div>
      </div>
      <div class="action-bar">
        <button class="waves-effect waves-green btn-flat modal-action" type="submit" name="action" value="save">
          <i class="mdi-action-note-add left"></i>
          Сохранить
        </button>
        <button class="waves-effect waves-red btn-flat modal-action" type="submit" name="action" value="delete">
          <i class="mdi-action-delete left"></i>
          Удалить
        </button>
      </div>
    </form>
  </div>
</main>
