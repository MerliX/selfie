% rebase('base.tpl')

% include('user_menu.tpl')

<main>
    <div class="container">
        <div class="section">
            <div class="row">
                <div class="col s12 m9 l6">

                    % if not generated:
                        <div class="card orange darken-1">
                            <div class="card-content white-text">
                                <p>Похоже, у нас кончились задания. Загляни сюда еще раз через десять минут.</p>
                            </div>
                        </div>
                    % end

                    % for task in active_tasks:

                        % if not task.is_complete:

                            <div class="card {{'red darken-2' if task.is_rejected else 'blue-grey darken-1'}}">
                                % if task.partner:
                                    <div class="card-image">
                                        <img src="{{task.partner.photo_url}}">
                                        <span class="card-title">{{task.get_participants_for_user(user)}}</span>
                                    </div>
                                    <div class="card-content white-text">
                                        <p>{{task.description}}</p>
                                    </div>
                                %else:
                                    <div class="card-content white-text">
                                        <span class="card-title">Первое задание!</span>
                                        <p>{{task.description}}</p>
                                    </div>
                                %end

                                % if task.is_rejected:
                                    <div class="card-content white-text">
                                        <p>Модератор отклонил фотографию, потому что она не соответствует заданию. Попробуте ещё раз.</p>
                                    </div>
                                % end

                                <div class="card-action valign-wrapper">
                                    <form action="/user/upload_photo" method="POST" enctype="multipart/form-data" class="no-margin">
                                        <input type="hidden" name="task_id" value="{{task.id}}">
                                        <label class="btn waves-effect waves-light no-margin">
                                            <i class="mdi-file-cloud-upload left"></i>
                                            Загрузить
                                            <input type="file" name="photo_file">
                                        </label>
                                    </form>
                                </div>
                            </div>

                        % else:

                            <div class="card blue-grey darken-1">
                                <div class="card-image">
                                    <img src="{{task.photo_url}}">
                                    <span class="card-title">{{task.get_participants_for_user(user)}}</span>
                                </div>
                                <div class="card-content white-text">
                                    <p>{{task.description}}</p>
                                </div>
                                <div class="card-action valign-wrapper">
                                    <a href="/" class="btn orange darken-2 white-text no-margin">
                                        <i class="mdi-action-schedule left"></i>
                                        Проверяем
                                    </a>
                                </div>
                            </div>

                        % end
                    % end

                    % for task in approved_tasks:
                        <div class="card">
                            <div class="card-image">
                                <img src="{{task.photo_url}}">
                                <span class="card-title">{{task.get_participants_for_user(user)}}</span>
                            </div>
                            <div class="card-content">
                                <p>{{task.description}}</p>
                            </div>
                        </div>
                    % end
                </div>
            </div>
        </div>
    </div>
</main>
