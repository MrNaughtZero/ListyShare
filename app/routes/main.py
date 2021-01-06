from flask import Flask, Blueprint, render_template, flash, get_flashed_messages, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.forms import CreateListForm, EditListName, AddAdditionalListItems, AddManyListItems
from app.models import List, Item, User

main_bp = Blueprint("main", __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html')

@main_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('/main/profile.html', lists=List().return_all_lists(current_user.get_username()))

@main_bp.route('/u/<username>', methods=['GET'])
def public_profile(username):
    if not User().custom_query('username', username):
        return redirect(url_for('main.index'))
    return render_template('/main/public-profile.html', lists=List().explore_lists(), user=username)

@main_bp.route('/explore', methods=['GET'])
def explore():
    return render_template('/main/explore.html', lists=List().explore_lists())


@main_bp.route('/create-list', methods=['GET'])
def create_list():
    return render_template('/main/create-list.html', form=CreateListForm(), message=get_flashed_messages())

@main_bp.route('/add/list', methods=['POST'])
def add_list():
    form = CreateListForm()
    if not form.validate_on_submit():
        flash(list(form.errors.values())[0])
        return redirect(url_for('main.create_list'))
    

    add = List(name=request.form.get('list_name'), user=current_user.get_username(), explore=request.form.get('exploreable'), link_code=List.generate_link_code()).add_list(request.form.get('list_items'))
    
    return redirect(url_for('main.list_page', user=current_user.get_username(), link_code=add))

@main_bp.route('/u/<user>/<link_code>', methods=['GET'])
def list_page(user, link_code):
    query = List().query_list(user, link_code)
    if not query:
        return abort(404)
    return render_template('/main/view-list.html', user=user, list=query, edit=EditListName(), add=AddAdditionalListItems(), many=AddManyListItems())

@main_bp.route('/edit/list/name/<code>', methods=['POST'])
def edit_list_title(code):
    if not current_user.is_authenticated:
        return abort(404)
    if not List().update_list_title(current_user.get_username(), code, request.form.get('list_name')):
        return abort(404)
    
    return redirect(url_for('main.list_page', user=current_user.get_username(), link_code=code))

@main_bp.route('/edit/list/add/item/<code>/<id>', methods=['POST'])
def add_list_item(code, id):
    if (not current_user.is_authenticated) or (not List().check_correct_user(current_user.get_username(), code)):
        return abort(404)
    if not Item(item=request.form.get('list_item'), list_id=id).add_item():
        return 'Something went wrong'

    return redirect(url_for('main.list_page', user=current_user.get_username(), link_code=code))

@main_bp.route('/edit/list/add/many/items/<code>/<id>', methods=['POST'])
def add_many_list_items(code, id):
    if (not current_user.is_authenticated) or (not List().check_correct_user(current_user.get_username(), code)):
        return abort(404)

    Item(list_id=id).add_many(request.form.get('list_items'))

    return redirect(url_for('main.list_page', user=current_user.get_username(), link_code=code))

@main_bp.route('/edit/list/delete/item/<code>/<list_id>/<item>', methods=['GET'])
def delete_list_item(code, list_id, item):
    if (not current_user.is_authenticated) or (not List().check_correct_user(current_user.get_username(), code)):
        return abort(404)
    if not Item().delete_item(list_id, item):
        return ('', 400)
    return ('', 204)
    
    
@main_bp.route('/add/starred/list', methods=['GET'])
def add_star():
    pass

@main_bp.route('/remove/starred/list', methods=['GET'])
def remove_star():
    pass
    
