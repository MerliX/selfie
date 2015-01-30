% rebase('base.tpl')

% include('moderator_menu.tpl', logo=u'Магазин')

<main>
  <div class="container">
    <div class="section">
      % if created_item:
      <div class="row">
        <div class="col s12">
          <blockquote>
            Товар: {{created_item}}
            <br>
            Стоимость: {{created_price}}
          </blockquote>
        </div>
      </div>
      % end
      <div class="row">
        <form class="col s12" method="POST" action="/moderator/add_store_item">
          <div class="row">
            <div class="input-field col s12">
              <input id="add_store_item_description" name="add_store_item_description" type="text">
              <label for="add_store_item_description">Товар</label>
            </div>
            <div class="input-field col s6">
              <input id="add_store_item_price" name="add_store_item_price" type="text">
              <label for="add_store_item_price">Стоимость</label> 
            </div>
            <div class="col s6">
              <button class="btn waves-effect waves-light" type="submit"><i class="mdi-action-content-add left"></i>
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
                  <th>Товар</th>
                  <th>Стоимость</th>
                  <th></th>
              </tr>
            </thead>

            <tbody>
              % for item in items:
              <tr>
                <td>{{item.description}}</td>
                <td>{{item.price}}</td>
                <td>
                  <form method="POST" action="/moderator/delete_store_item" class="no-margin">
                    <input type="hidden" name="store_item_id" value="{{item.id}}">
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
