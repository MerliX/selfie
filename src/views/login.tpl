% rebase('base.tpl')

<header>
  <nav>
    <div class="container">
      <div class="nav-wrapper">
        <a href="/" class="brand-logo">Селфи КонфУР</a>
      </div>
    </div>
  </nav>
</header>

<main>
  <div class="container">
    <div class="section">
      % if wrong_code:
      <div class="row">
        <div class="col s12">
          <blockquote>
            Похоже, у тебя неправильный код. Попробуй ввести еще раз или обратись к организаторам.
          </blockquote>
        </div>
      </div>
      % else:
      <div class="card cyan lighten-2">
        <div class="card-content white-text">
          <p>Игра состоит из фотозаданий. Чем дальше, тем сложнее. В каждом задании указан второй
            человек, которого нужно найти и уговорить сфотографироваться. На фотографии должны быть
            вы оба. А еще смешные задания. Их нужно выполнить.</p>
          <p>Итоги подводим в 21:00. Кто сдал больше всех фоток — тот и победил.</p>
        </div>
      </div>
      % end
      <div class="row">
        <form class="col s12" method="POST">
          <div class="row">
            <div class="input-field col s8 m6 l3">
              <input id="access_code" name="access_code" type="password">
              <label for="access_code">Код доступа</label>
            </div>
            <div class="col s4">
              <button class="btn waves-effect waves-light" type="submit">Войти</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</main>
