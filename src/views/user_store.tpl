% rebase('base.tpl')

% include('user_menu.tpl')

<main>
  <div class="container">
    <div class="section">
      <div class="row">
        <div class="col s12">
          <table class="striped">
            <tbody>
              % for item in items:
              <tr>
                <td>{{item.description}}</td>
                % if user.has_active_store_item(item):
                <td colspan="2">Жди свой приз!</td>
                % else:
                <td><i class="mdi-editor-attach-money user-money-icon"></i>{{item.price}}</td>
                <td>
                  <form method="POST" action="/user/buy_store_item" class="no-margin">
                    <input type="hidden" name="store_item_id" value="{{item.id}}">
                    <button type="submit" class="waves-effect waves-blue btn-flat blue-text no-margin"><i class="mdi-action-add-shopping-cart"></i></button>
                  </form>
                </td>
                % end
              </tr>
              % end
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</main>
