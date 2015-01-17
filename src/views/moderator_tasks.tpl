% rebase('base.tpl')

% include('moderator_menu.tpl', logo=u'Задания')

<main>
  <div class="container">
    <div class="section">
      <div class="row">
        <div class="col s12">
          <table class="striped">
            <thead>
              <tr>
                  <th></th>
                  <th>Задание</th>
                  <th>Сложность</th>
                  <th></th>
              </tr>
            </thead>

            <tbody>
              % for selfie in selfies:
              <tr>
                <td>
                  % if selfie.is_complete:
                  <i class="mdi-action-done"></i>
                  % end
                </td>
                <td>
                  <p>
                    {{selfie.assignee.name}}
                    % if selfie.partner:
                    &rarr; {{selfie.partner.name}}
                    % end
                  </p>
                  <p>
                    {{selfie.description}}
                  </p>
                </td>
                <td>{{selfie.difficulty}}</td>
                <td>
                  <form method="POST" action="/moderator/regenerate_selfie" class="no-margin">
                    <input type="hidden" name="selfie_id" value="{{selfie.id}}">
                    <button type="submit" class="waves-effect waves-light btn-flat no-margin"><i class="mdi-action-autorenew"></i></button>
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
